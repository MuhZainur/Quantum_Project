import pandas as pd
import joblib
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from schemas import SalesInput, ChurnInput
from monitoring_service import generate_churn_drift_report
import os

# Initialize App
app = FastAPI(
    title="Retail Analytics AI API",
    description="API for Sales Forecasting & Churn Prediction Models",
    version="1.0.0"
)

# CORS (Allow Frontend execution)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production: Specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Variables for Models
sales_model = None
churn_model = None

@app.on_event("startup")
def load_models():
    global sales_model, churn_model
    try:
        # Load Sales Model
        sales_path = "sales_forecast_pipeline.pkl"
        if os.path.exists(sales_path):
            sales_model = joblib.load(sales_path)
            print(f"✅ Sales Model loaded from {sales_path}")
        else:
            print(f"❌ Sales Model not found at {sales_path}")

        # Load Churn Model
        churn_path = "churn_prediction_pipeline.pkl"
        if os.path.exists(churn_path):
            churn_model = joblib.load(churn_path)
            print(f"✅ Churn Model loaded from {churn_path}")
        else:
            print(f"❌ Churn Model not found at {churn_path}")
            
    except Exception as e:
        print(f"🔥 Error loading models: {e}")

@app.get("/")
def home():
    return {"message": "Retail Analytics AI API is Running", "docs": "/docs"}

@app.post("/predict/sales")
def predict_sales(data: SalesInput):
    if not sales_model:
        raise HTTPException(status_code=503, detail="Sales Model not loaded")
    
    try:
        # Convert Request to Dict
        input_data = data.dict()
        
        # Derived Feature Engineering (Date -> Day/Month/etc)
        # Note: The input MUST provide the Lag features as they cannot be calculated without history.
        dt = pd.to_datetime(input_data['date'])
        
        # Rename keys to match Training Columns exactly
        df_input = pd.DataFrame([{
            'STORE_NBR': input_data['store_nbr'],
            'PROD_QTY': input_data['prod_qty'],
            'TXN_COUNT': input_data['txn_count'],
            'Sales_Lag_1': input_data['sales_lag_1'],
            'Sales_Lag_7': input_data['sales_lag_7'],
            'Rolling_Mean_7': input_data['rolling_mean_7'],
            # Time Features
            'Day': dt.day,
            'Month': dt.month,
            'DayOfWeek': dt.dayofweek,
            'IsWeekend': 1 if dt.dayofweek >= 5 else 0
        }])
        
        # Predict
        prediction = sales_model.predict(df_input)
        
        return {
            "model": "Sales Forecasting (Regression)",
            "store_nbr": input_data['store_nbr'],
            "date": input_data['date'],
            "predicted_sales": float(prediction[0])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/churn")
def predict_churn(data: ChurnInput):
    if not churn_model:
        raise HTTPException(status_code=503, detail="Churn Model not loaded")
    
    try:
        input_data = data.dict()
        
        # Rename keys to match Training Columns
        df_input = pd.DataFrame([{
            'Recency': input_data['recency'],
            'Frequency': input_data['frequency'],
            'Monetary': input_data['monetary'],
            'LIFESTAGE': input_data['lifestage'],
            'PREMIUM_CUSTOMER': input_data['premium_customer']
        }])
        
        # --- LOGGING FOR DRIFT MONITORING ---
        log_file = "churn_logs.csv"
        # Append to CSV (create header if file doesn't exist)
        try:
            df_input.to_csv(log_file, mode='a', header=not os.path.exists(log_file), index=False)
        except Exception as log_err:
            print(f"Warning: Could not log data: {log_err}")
        # ------------------------------------

        # Predict Class and Probability
        prediction = churn_model.predict(df_input)[0]
        prob = churn_model.predict_proba(df_input)[0][1] # Probability of Class 1 (Churn)
        
        return {
            "model": "Churn Prediction (Classification)",
            "churn_prediction": "Churn" if prediction == 1 else "Not Churn",
            "churn_probability": float(prob),
            "risk_level": "High" if prob > 0.7 else "Medium" if prob > 0.3 else "Low"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/monitoring/churn/drift")
def churn_drift_report():
    """Generates and returns the Evidently Data Drift Report"""
    result = generate_churn_drift_report()
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return FileResponse(result["report_path"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
