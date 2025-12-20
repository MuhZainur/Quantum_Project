# Phase 3: Machine Learning Engineering (MLE) - From Notebook to Production

**Objective:** Transform the static Data Science models (Sales Forecasting & Churn Prediction) into a scalable, interactive, and reliable Web Application.

---

## 1. System Architecture
We moved away from isolated Jupyter Notebooks to a modern Microservices-inspired architecture:

*   **Backend:** FastAPI (Python) - High-performance API for serving models.
*   **Frontend:** React (Vite + Tailwind CSS) - Interactive dashboard for business users.
*   **MLOps Pipeline:** Automated Testing (CI), Data Drift Monitoring (Evidently AI), and Containerization (Docker).

---

## 2. Backend API Development (FastAPI)
The core engine of the application. We wrapped the `scikit-learn` pipelines into RESTful API endpoints.

### Key Logic: `main.py`
We designed structured schemas using **Pydantic** to enforce data quality *before* it reaches the model.

```python
# H:\coding\Quantum_Virtual_Project\MLE\Backend\main.py

@app.post("/predict/churn")
def predict_churn(data: ChurnInput):
    # 1. Validate Input (Pydantic)
    input_data = data.dict()
    
    # 2. DataFrame Construction
    df_input = pd.DataFrame([{
        'Recency': input_data['recency'],
        'Frequency': input_data['frequency'],
        'Monetary': input_data['monetary'],
        'LIFESTAGE': input_data['lifestage'],
        'PREMIUM_CUSTOMER': input_data['premium_customer']
    }])
    
    # 3. Log Data for Drift Monitoring
    log_file = "churn_logs.csv"
    df_input.to_csv(log_file, mode='a', header=not os.path.exists(log_file), index=False)
    
    # 4. Predict
    prediction = churn_model.predict(df_input)[0]
    prob = churn_model.predict_proba(df_input)[0][1]
    
    return {
        "churn_prediction": "Churn" if prediction == 1 else "Not Churn",
        "churn_probability": float(prob),
        "risk_level": "High" if prob > 0.7 else "Medium" if prob > 0.3 else "Low"
    }
```

**Design Decision:**
We explicitly removed `LYLTY_CARD_NBR` (Customer ID) from the feature set. During development, we realized passing IDs to the model could lead to overfitting on specific customers rather than learning behavioral patterns.

---

## 3. Frontend Dashboard (React + Tailwind)
We built a professional-grade UI to allow Store Managers to interact with the complex models easily.

*   **Sales Forecasting Tab:** Visualizes historical trends and predicts future sales given specific lags.
*   **Churn Prediction Tab:** A form-based interface that assesses customer risk in real-time.

```jsx
// H:\coding\Quantum_Virtual_Project\MLE\Frontend\src\App.jsx

const handleChurnSubmit = async (e) => {
  e.preventDefault();
  try {
    const response = await api.post('/predict/churn', churnData);
    setChurnResult(response.data);
  } catch (err) {
    setError('Failed to predict churn');
  }
};
```

---

## 4. MLOps: Ensuring Reliability
A model in production is a living entity that can degrade. We implemented safeguards.

### A. Data Drift Monitoring (Evidently AI)
We integrated **Evidently AI** to automatically compare live production data (`churn_logs.csv`) against our training baseline (`reference_churn_data.csv`).

*   **Mechanism:** Every time `/predict/churn` is called, the input is logged.
*   **Report:** An endpoint `/monitoring/churn/drift` generates a visual HTML report detecting distributional shifts (Data Drift).

```python
# H:\coding\Quantum_Virtual_Project\MLE\Backend\monitoring_service.py

def generate_churn_drift_report():
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference_data, current_data=current_data)
    report.save_html("churn_drift_report.html")
```

### B. CI/CD Pipeline (GitHub Actions)
To prevent bad code from breaking production, we set up a Continuous Integration pipeline.
*   **Trigger:** Every `git push`.
*   **Action:** Installs Python environment -> Installs dependencies -> Runs `pytest`.

```yaml
# H:\coding\Quantum_Virtual_Project\MLE\.github\workflows\ci_pipeline.yml

    - name: Test with pytest
      run: |
        pytest test_api.py
```

### C. Containerization (Docker)
We "Dockerized" the entire stack to ensure it runs identically on any machine (Local, AWS, Azure).

*   **Backend:** `python:3.10-slim`
*   **Frontend:** Multi-stage build (Node.js -> Nginx) for optimal performance.
*   **Orchestration:** `docker-compose` to spin up both services with one command.

```yaml
# H:\coding\Quantum_Virtual_Project\MLE\docker-compose.yml

services:
  backend:
    build: ./Backend
    ports: ["8000:8000"]
  frontend:
    build: ./Frontend
    ports: ["3000:80"]
```

---

## Conclusion
This phase bridged the gap between theoretical Data Science and practical Software Engineering. We delivered not just a model file, but a **full-stack operational system** that is monitored, tested, and containerized.

---
*Created by [MuhZainur] - Data Scientist & ML Engineer*
