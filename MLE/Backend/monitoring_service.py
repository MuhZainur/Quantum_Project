from evidently import Report
from evidently.presets import DataDriftPreset
import pandas as pd
import os

REFERENCE_PATH = "reference_churn_data.csv"
CURRENT_PATH = "churn_logs.csv"
REPORT_OUTPUT = "churn_drift_report.html"

def generate_churn_drift_report():
    """Generates an HTML Data Drift Report comparing Reference vs Current Logged Data"""
    
    if not os.path.exists(REFERENCE_PATH):
        return {"error": "Reference data not found. Run prepare_reference_data.py first."}
    
    if not os.path.exists(CURRENT_PATH):
        return {"error": "No current data logs found. Make some predictions first."}
    
    try:
        # Load Data
        reference_data = pd.read_csv(REFERENCE_PATH)
        current_data = pd.read_csv(CURRENT_PATH)
        
        # Ensure columns match
        common_cols = list(set(reference_data.columns) & set(current_data.columns))
        reference_data = reference_data[common_cols]
        current_data = current_data[common_cols]
        
        # Column Mapping
        column_mapping = {
            'target': None,
            'prediction': None,
            'id': None,
            'numerical_features': ['Recency', 'Frequency', 'Monetary'],
            'categorical_features': ['LIFESTAGE', 'PREMIUM_CUSTOMER']
        }
        
        # Generate Report
        report = Report(metrics=[
            DataDriftPreset(), 
        ])
        
        report.run(reference_data=reference_data, current_data=current_data, column_mapping=column_mapping)
        
        # Save Report
        report.save_html(REPORT_OUTPUT)
        
        return {"status": "success", "report_path": REPORT_OUTPUT}
        
    except Exception as e:
        return {"error": str(e)}
