import pandas as pd
import os

def generate_reference_data():
    """Generates reference dataset for Churn Prediction from QVI_data.csv"""
    data_path = "../../QVI_data.csv"
    output_path = "reference_churn_data.csv"
    
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    print("Loading Raw Data...")
    df = pd.read_csv(data_path)
    df['DATE'] = pd.to_datetime(df['DATE'])

    print("Processing Features...")
    max_date = df['DATE'].max()
    cutoff_date = max_date - pd.DateOffset(months=3)
    pre_cutoff_data = df[df['DATE'] <= cutoff_date]

    # Aggregation (Same logic as Training)
    customer_features = pre_cutoff_data.groupby('LYLTY_CARD_NBR').agg(
        Recency=('DATE', lambda x: (cutoff_date - x.max()).days),
        Frequency=('TXN_ID', 'count'),
        Monetary=('TOT_SALES', 'sum'),
        LIFESTAGE=('LIFESTAGE', 'first'),
        PREMIUM_CUSTOMER=('PREMIUM_CUSTOMER', 'first')
    ).reset_index()
    
    # Note: We do NOT need the target variable (CHURN_FLAG) for Data Drift, only Input Features.
    # We drop LYLTY_CARD_NBR as it's an ID, not a feature.
    feature_df = customer_features.drop(columns=['LYLTY_CARD_NBR'])
    
    print(f"Saving Reference Data ({len(feature_df)} rows) to {output_path}...")
    feature_df.to_csv(output_path, index=False)
    print("Done.")

if __name__ == "__main__":
    generate_reference_data()
