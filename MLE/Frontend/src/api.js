import axios from 'axios';

const API = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'https://quantum-project-567427950134.asia-southeast2.run.app',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const predictSales = async (data) => {
    try {
        const response = await API.post('/predict/sales', data);
        return response.data;
    } catch (error) {
        console.error("Sales API Error:", error);
        throw error;
    }
};

export const predictChurn = async (data) => {
    try {
        const response = await API.post('/predict/churn', data);
        return response.data;
    } catch (error) {
        console.error("Churn API Error:", error);
        throw error;
    }
};

export default API;
