# Portfolio Project: Advanced Retail Prediction (Data Science)
**Forecasting Sales & Predicting Churn using Machine Learning**

## Project Overview
Building upon the analytics phase, this project deploys advanced Machine Learning models to predict future trends. We moved beyond historical analysis to descriptive and predictive modeling, creating a robust pipeline for **Sales Forecasting** (Regression) and **Customer Churn Prediction** (Classification).

---

## Part 1: Methodology (Custom AutoML)
**"Standardization over Complexity."** Instead of relying on heavy black-box AutoML libraries that are prone to deployment issues (DLL errors, dependency conflicts), we engineered a **Custom Scikit-Learn Wrapper**.

### 1. Robust Architecture
We built a unified pipeline function that automates the end-to-end ML workflow while maintaining full control over the code.
*   **Modular Design:** Separate functions for `setup`, `compare`, `tune`, and `evaluate`.
*   **Tech Stack:** `Scikit-Learn` (Core), `XGBoost` (Gradient Boosting), `Imbalanced-Learn` (SMOTE).

### 2. Automated Preprocessing
Data leakage is a common pitfall. To prevent this, we encapsulated all preprocessing steps within a `Pipeline` object.
*   **Numerical:** Median Imputation + Standard Scaling.
*   **Categorical:** Constant Imputation + One-Hot Encoding.

---

## Part 2: Sales Forecasting (Regression)
**Goal:** Predict daily `TOT_SALES` for specific stores to optimize inventory management.

### 1. Feature Engineering (Time-Series)
Since raw transactional data isn't ready for regression, we engineered lag features to capture temporal dependencies.
*   **Key Features Created:** `Sales_Lag_1` (Yesterday's sales), `Sales_Lag_7` (Last week's sales), and `Rolling_Mean_7` (Weekly trend).

### 2. Model Performance
We compared Linear Regression, Random Forest, and XGBoost.
*   **Top Performer:** **Random Forest / XGBoost** (depending on the run).
*   **Why?** Tree-based models effectively captured non-linear relationships and interactions between Day-of-Week and promotional periods.

### 3. Key Insights (Drivers of Sales)
We analyzed Feature Importance to understand what drives revenue.
*   **Insight:** **Historical Sales (Lag Features)** are the strongest predictors. If a store sold well yesterday/last week, it is highly likely to sell well today. `PROD_QTY` is also a massive factor (volume drives value).

> **[INSERT IMAGE 1]**
> *Please include the "Top 10 Feature Importances" plot from the Regression Evaluation section.*

---

## Part 3: Customer Churn Prediction (Classification)
**Goal:** Identify customers at risk of leaving (Churn) to target them with retention campaigns.

### 1. The Imbalance Problem
Real-world churn data is rarely balanced (most customers *don't* churn). Training on this directly leads to models that just guess "Not Churn" 100% of the time.
*   **Solution:** We implemented **SMOTE (Synthetic Minority Over-sampling Technique)**.
*   **How it works:** Instead of simply duplicating data, SMOTE creates "synthetic" examples of Churners based on their nearest neighbors, teaching the model to recognize the *characteristics* of churners rather than just their frequency.

### 2. Model Performance
*   **Metric Focus:** We prioritized **Recall** (Sensitivity) over Accuracy.
*   **Reasoning:** In retention, missing a churner (False Negative) is costlier than accidentally targeting a loyal customer (False Positive). We want to catch as many potential churners as possible.

### 3. Key Insights (Who is leaving?)
*   **Insight:** **Recency** (Days since last purchase) is the #1 predictor. As the gap between purchases widens, the probability of churn spikes exponentially.

> **[INSERT IMAGE 2]**
> *Please include the "Confusion Matrix" or "ROC-AUC Curve" to demonstrate the model's ability to distinguish between Churners and Active customers.*

---

## Conclusion & Business Impact
This Data Science pipeline provides actionable intelligence:
1.  **Inventory Optimization:** Accurate Daily Sales forecasts allow stores to stock up precisely for high-traffic days (Lag features).
2.  **Proactive Retention:** The Churn model identifies "At-Risk" customers *before* they leave, allowing the marketing team to trigger automated re-engagement emails based on `Recency` thresholds.

---
*Created by [MuhZainur] - Data Scientist & ML Engineer*
