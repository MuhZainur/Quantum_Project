---
title: Retail Analytics API
emoji: 🛒
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8000
pinned: false
---

# Retail Analytics AI - Backend API

This is the FastAPI backend for the Retail Analytics AI application, serving Sales Forecasting and Churn Prediction models.

## Models
- Sales Forecasting: Random Forest/XGBoost Regression
- Churn Prediction: Classification with SMOTE

## API Endpoints
- `GET /`: Health check
- `POST /predict/sales`: Sales forecasting
- `POST /predict/churn`: Customer churn prediction
- `GET /docs`: Interactive API documentation
