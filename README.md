# Quantum Retail Analytics AI 🚀

An End-to-End Retail Analytics solution transforming raw transaction data into actionable AI insights. Ideally suited for Retail Strategy Teams to optimize sales forecasting and customer retention.

## 🌐 Live Demo

**🎯 Try it out:**
- **Interactive Dashboard:** [quantum-project-fe-567427950134.asia-southeast2.run.app](https://quantum-project-fe-567427950134.asia-southeast2.run.app/)
- **API Documentation:** [quantum-project-567427950134.asia-southeast2.run.app/docs](https://quantum-project-567427950134.asia-southeast2.run.app/docs)

*Deployed on Google Cloud Run with automated CI/CD pipeline.*

---

## 🏗️ Architecture Overview

This project simulates a real-world enterprise workflow, divided into three professional phases:

### Phase 1: Data Analytics (DA) 📊
*   **Goal:** Exploratory Data Analysis (EDA) and Customer Segmentation.
*   **Key Insights:** Identified high-value "Mainstream Young Singles/Couples" segment and evaluated trial store performance using A/B testing metrics.
*   **Tools:** Python (Pandas, Matplotlib, Seaborn).

### Phase 2: Data Science (DS) 🧠
*   **Goal:** Build predictive models for business forecasting.
*   **Sales Forecasting:** Regression model (XGBoost/RandomForest) to predict future store sales.
*   **Churn Prediction:** Classification model to identify customers at risk of leaving.
*   **Techniques:** SMOTE (Imbalanced Data), Feature Engineering (Lag Features, Rolling Means), Hyperparameter Tuning.

### Phase 3: ML Engineering (MLE) ⚙️
*   **Goal:** Deploy models into a scalable, production-ready web application.
*   **Backend:** **FastAPI** serving Scikit-learn pipelines (`.pkl`).
*   **Frontend:** **React** (Vite + Tailwind CSS) for an interactive executive dashboard.
*   **MLOps:**
    *   **Docker:** Full containerization of Backend and Frontend.
    *   **CI/CD:** GitHub Actions for automated API testing (`pytest`).
    *   **Deployment:** Ready for GCP Cloud Run deployment.

---

## 💻 Tech Stack

| Component | Technologies |
| :--- | :--- |
| **Data Science** | Python 3.10, Scikit-Learn, Pandas, NumPy, XGBoost, Imbalanced-learn |
| **Backend API** | FastAPI, Uvicorn, Pydantic, Joblib |
| **Frontend UI** | React.js, Vite, Tailwind CSS, Axios |
| **MLOps** | Docker, Docker Compose, GitHub Actions |

---

## 🚀 How to Run (Docker)

The entire application can be launched with a single command using Docker Compose.

### Prequisites
*   Docker & Docker Compose installed.

### Steps
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/MuhZainur/quantum-retail-ai.git
    cd quantum-retail-ai
    ```

2.  **Launch Application**
    ```bash
    cd MLE
    docker-compose up --build
    ```

> **📦 Ready to Deploy?** See [DEPLOYMENT_CLOUD_RUN.md](DEPLOYMENT_CLOUD_RUN.md) for GCP Cloud Run deployment guide.

---

## 📂 Project Structure

```
├── DA/                   # Phase 1: Data Analytics Notebooks
├── DS/                   # Phase 2: Data Science Notebooks & Models
│   ├── DS_Retail_Forecast_and_Churn.ipynb
│   └── DS_Portfolio_Report.md
├── MLE/                  # Phase 3: Deployment & MLOps
│   ├── Backend/          # FastAPI App
│   ├── Frontend/         # React App
│   ├── docker-compose.yml
│   └── MLE_Portfolio_Report.md
└── README.md             # Project Documentation
```

---

## 🧪 Testing (CI/CD)

Automated tests are defined in `.github/workflows/ci_pipeline.yml`. To run manually locally:

```bash
cd MLE/Backend
pytest
```

---
*Created by [MuhZainur] - Data Scientist & ML Engineer*
