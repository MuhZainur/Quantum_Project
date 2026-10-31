import axios from 'axios';

const DEFAULT_BASE_URL = 'https://quantum-project.onrender.com';
const API_BASE_URL = import.meta.env.VITE_API_URL || import.meta.env.VITE_API_BASE_URL || DEFAULT_BASE_URL;

const API = axios.create({
    baseURL: API_BASE_URL.replace(/\/+$/, ''),
    timeout: 15000,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const predictSales = async (data) => {
    try {
        const response = await API.post('/predict/sales', data);
        return response.data;
    } catch (error) {
        console.warn("Backend sleeping or offline. Engaging client heuristic simulation for sales:", error);
        const est = Number(data.rolling_mean_7 || 140) * 0.55 + Number(data.sales_lag_1 || 140) * 0.25 + Number(data.prod_qty || 50) * 0.45;
        return {
            model: "Sales Forecasting (Regression)",
            store_nbr: data.store_nbr,
            date: data.date,
            predicted_sales: parseFloat(est.toFixed(2)),
            is_simulated: true
        };
    }
};

export const predictChurn = async (data) => {
    try {
        const response = await API.post('/predict/churn', data);
        return response.data;
    } catch (error) {
        console.warn("Backend sleeping or offline. Engaging client heuristic simulation for churn:", error);
        let prob = 0.22;
        if (Number(data.recency) > 20) prob += 0.36;
        if (Number(data.frequency) < 4) prob += 0.24;
        if (Number(data.monetary) < 80) prob += 0.12;
        prob = Math.min(Math.max(prob, 0.06), 0.94);
        const probFixed = parseFloat(prob.toFixed(2));
        return {
            model: "Churn Prediction (Classification)",
            churn_prediction: probFixed > 0.5 ? "Churn" : "Not Churn",
            churn_probability: probFixed,
            risk_level: probFixed > 0.7 ? "High" : probFixed > 0.3 ? "Medium" : "Low",
            is_simulated: true
        };
    }
};

export default API;
