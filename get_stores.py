import pandas as pd
import json

try:
    df = pd.read_csv(r'H:\coding\Quantum_Virtual_Project\QVI_data.csv')
    stores = sorted(df['STORE_NBR'].unique().tolist())
    with open('stores_list.json', 'w') as f:
        json.dump(stores, f)
    print(f"Successfully saved {len(stores)} stores to stores_list.json")
except Exception as e:
    print(f"Error: {e}")
