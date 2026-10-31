import os
import pandas as pd
import joblib
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import SalesInput, ChurnInput

# Initialize App
app = FastAPI(
    title="Retail Analytics AI API",
    description="API for Sales Forecasting & Churn Prediction Models",
    version="1.0.0"
)

# CORS (Allow Frontend execution)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Variables for Models
sales_model = None
churn_model = None

def _find_model_path(filename: str):
    candidates = [
        os.path.join(os.path.dirname(__file__), filename),
        os.path.join(os.getcwd(), filename),
        os.path.join(os.getcwd(), "MLE", "Backend", filename),
        filename
    ]
    for path in candidates:
        if os.path.exists(path):
            return os.path.abspath(path)
    return None

@app.on_event("startup")
def load_models():
    global sales_model, churn_model
    try:
        # Load Sales Model
        sales_path = _find_model_path("sales_forecast_pipeline.pkl")
        if sales_path:
            sales_model = joblib.load(sales_path)
            print(f"✅ Sales Model loaded from {sales_path}")
        else:
            print("❌ Sales Model not found in any expected paths")

        # Load Churn Model
        churn_path = _find_model_path("churn_prediction_pipeline.pkl")
        if churn_path:
            churn_model = joblib.load(churn_path)
            print(f"✅ Churn Model loaded from {churn_path}")
        else:
            print("❌ Churn Model not found in any expected paths")
            
    except Exception as e:
        print(f"🔥 Error loading models: {e}")

@app.get("/")
def home():
    return {
        "message": "Retail Analytics AI API is Running",
        "docs": "/docs",
        "sales_model": "Loaded" if sales_model else "Not Loaded",
        "churn_model": "Loaded" if churn_model else "Not Loaded"
    }

@app.get("/health")
def health():
    if not sales_model or not churn_model:
        load_models()
    return {
        "status": "healthy" if (sales_model and churn_model) else "degraded",
        "sales_model": sales_model is not None,
        "churn_model": churn_model is not None
    }

@app.post("/predict/sales")
def predict_sales(data: SalesInput):
    global sales_model
    if not sales_model:
        load_models()
    
    input_data = data.dict()
    dt = pd.to_datetime(input_data['date'])
    
    df_input = pd.DataFrame([{
        'STORE_NBR': input_data['store_nbr'],
        'PROD_QTY': input_data['prod_qty'],
        'TXN_COUNT': input_data['txn_count'],
        'Sales_Lag_1': input_data['sales_lag_1'],
        'Sales_Lag_7': input_data['sales_lag_7'],
        'Rolling_Mean_7': input_data['rolling_mean_7'],
        'Day': dt.day,
        'Month': dt.month,
        'DayOfWeek': dt.dayofweek,
        'IsWeekend': 1 if dt.dayofweek >= 5 else 0
    }])
    
    if sales_model:
        try:
            prediction = sales_model.predict(df_input)
            return {
                "model": "Sales Forecasting (Regression)",
                "store_nbr": input_data['store_nbr'],
                "date": input_data['date'],
                "predicted_sales": float(prediction[0]),
                "is_fallback": False
            }
        except Exception as e:
            print(f"⚠️ Model prediction failed, using fallback: {e}")

    # Fallback heuristic calculation if model not loaded
    est = float(input_data['rolling_mean_7'] * 0.5 + input_data['sales_lag_1'] * 0.3 + input_data['prod_qty'] * 1.5)
    return {
        "model": "Sales Forecasting (Regression Heuristic)",
        "store_nbr": input_data['store_nbr'],
        "date": input_data['date'],
        "predicted_sales": round(est, 2),
        "is_fallback": True
    }

@app.post("/predict/churn")
def predict_churn(data: ChurnInput):
    global churn_model
    if not churn_model:
        load_models()

    input_data = data.dict()
    df_input = pd.DataFrame([{
        'Recency': input_data['recency'],
        'Frequency': input_data['frequency'],
        'Monetary': input_data['monetary'],
        'LIFESTAGE': input_data['lifestage'],
        'PREMIUM_CUSTOMER': input_data['premium_customer']
    }])
    
    if churn_model:
        try:
            prediction = churn_model.predict(df_input)[0]
            prob = churn_model.predict_proba(df_input)[0][1]
            return {
                "model": "Churn Prediction (Classification)",
                "churn_prediction": "Churn" if prediction == 1 else "Not Churn",
                "churn_probability": float(prob),
                "risk_level": "High" if prob > 0.7 else "Medium" if prob > 0.3 else "Low",
                "is_fallback": False
            }
        except Exception as e:
            print(f"⚠️ Churn prediction failed, using fallback: {e}")

    # Fallback heuristic calculation
    prob = 0.25
    if input_data['recency'] > 30: prob += 0.35
    if input_data['frequency'] < 3: prob += 0.20
    if input_data['monetary'] < 50: prob += 0.15
    prob = min(max(prob, 0.05), 0.95)
    pred = "Churn" if prob > 0.5 else "Not Churn"
    return {
        "model": "Churn Prediction (Heuristic Fallback)",
        "churn_prediction": pred,
        "churn_probability": float(round(prob, 3)),
        "risk_level": "High" if prob > 0.7 else "Medium" if prob > 0.3 else "Low",
        "is_fallback": True
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
