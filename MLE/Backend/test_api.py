from fastapi.testclient import TestClient
from main import app
import pytest

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Retail Analytics AI API is Running", "docs": "/docs"}

def test_predict_sales(client):
    payload = {
        "date": "2019-06-30",
        "store_nbr": 77,
        "prod_qty": 50,
        "txn_count": 20,
        "sales_lag_1": 150.5,
        "sales_lag_7": 140.0,
        "rolling_mean_7": 145.2
    }
    response = client.post("/predict/sales", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["model"] == "Sales Forecasting (Regression)"
    assert "predicted_sales" in data
    assert isinstance(data["predicted_sales"], float)

def test_predict_churn(client):
    # Test valid input WITHOUT lylty_card_nbr
    payload = {
        "recency": 10,
        "frequency": 5,
        "monetary": 25.50,
        "lifestage": "YOUNG SINGLES/COUPLES",
        "premium_customer": "Mainstream"
    }
    response = client.post("/predict/churn", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["model"] == "Churn Prediction (Classification)"
    assert data["churn_prediction"] in ["Churn", "Not Churn"]
    assert 0.0 <= data["churn_probability"] <= 1.0

def test_churn_input_validation(client):
    # Test missing field
    payload = {
        "recency": 10,
        "frequency": 5
        # Missing other fields
    }
    response = client.post("/predict/churn", json=payload)
    assert response.status_code == 422
