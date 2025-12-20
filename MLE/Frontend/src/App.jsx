import { useState } from 'react';
import { predictSales, predictChurn } from './api';
import { STORE_NUMBERS } from './storeData';

function App() {
  const [activeTab, setActiveTab] = useState('sales');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  // Sales Form State
  const [salesData, setSalesData] = useState({
    date: '2019-06-30',
    store_nbr: 77,
    prod_qty: 50,
    txn_count: 20,
    sales_lag_1: 150.0,
    sales_lag_7: 140.0,
    rolling_mean_7: 145.0
  });

  // Churn Form State
  const [churnData, setChurnData] = useState({
    recency: 10,
    frequency: 5,
    monetary: 100.0,
    lifestage: 'YOUNG SINGLES/COUPLES',
    premium_customer: 'Mainstream'
  });

  const handleSalesSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      const res = await predictSales(salesData);
      setResult(res);
    } catch (err) {
      alert("Error predicting sales. Check backend connection.");
    }
    setLoading(false);
  };

  const handleChurnSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      const res = await predictChurn(churnData);
      setResult(res);
    } catch (err) {
      alert("Error predicting churn. Check backend connection.");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800 font-sans">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-700 to-indigo-800 text-white p-6 shadow-lg">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <h1 className="text-3xl font-bold tracking-tight">Retail Analytics AI</h1>
          <span className="text-sm bg-blue-600 px-3 py-1 rounded-full bg-opacity-50">v1.0.0</span>
        </div>
      </header>

      <main className="max-w-4xl mx-auto p-6 mt-8">
        {/* Tab Navigation */}
        <div className="flex border-b border-gray-200 mb-8">
          <button
            className={`py-3 px-6 text-lg font-medium transition-colors duration-200 ${activeTab === 'sales'
              ? 'border-b-4 border-blue-600 text-blue-800'
              : 'text-gray-500 hover:text-gray-700'
              }`}
            onClick={() => { setActiveTab('sales'); setResult(null); }}
          >
            Sales Forecasting
          </button>
          <button
            className={`py-3 px-6 text-lg font-medium transition-colors duration-200 ${activeTab === 'churn'
              ? 'border-b-4 border-purple-600 text-purple-800'
              : 'text-gray-500 hover:text-gray-700'
              }`}
            onClick={() => { setActiveTab('churn'); setResult(null); }}
          >
            Churn Prediction
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Input Form Column */}
          <div className="md:col-span-2 bg-white p-6 rounded-xl shadow-md border border-gray-100">
            <h2 className="text-xl font-semibold mb-6 flex items-center">
              <span className={`w-3 h-3 rounded-full mr-3 ${activeTab === 'sales' ? 'bg-blue-500' : 'bg-purple-500'}`}></span>
              Input Parameters
            </h2>

            {activeTab === 'sales' ? (
              <form onSubmit={handleSalesSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
                    <input type="date" value={salesData.date} onChange={(e) => setSalesData({ ...salesData, date: e.target.value })} className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" required />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Store Number</label>
                    <select value={salesData.store_nbr} onChange={(e) => setSalesData({ ...salesData, store_nbr: parseInt(e.target.value) })} className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none bg-white" required>
                      {STORE_NUMBERS.map(num => (
                        <option key={num} value={num}>Store {num}</option>
                      ))}
                    </select>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Product Qty</label>
                    <input type="number" value={salesData.prod_qty} onChange={(e) => setSalesData({ ...salesData, prod_qty: parseInt(e.target.value) })} className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" required />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Transaction Count</label>
                    <input type="number" value={salesData.txn_count} onChange={(e) => setSalesData({ ...salesData, txn_count: parseInt(e.target.value) })} className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" required />
                  </div>
                </div>

                <div className="pt-4 border-t border-gray-100">
                  <p className="text-xs text-gray-500 mb-3 uppercase font-bold tracking-wider">Lag Features (Historical)</p>
                  <div className="grid grid-cols-3 gap-3">
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">Lag 1 (Yesterday)</label>
                      <input type="number" step="0.1" value={salesData.sales_lag_1} onChange={(e) => setSalesData({ ...salesData, sales_lag_1: parseFloat(e.target.value) })} className="w-full p-2 border rounded-lg bg-gray-50" required />
                    </div>
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">Lag 7 (Last Week)</label>
                      <input type="number" step="0.1" value={salesData.sales_lag_7} onChange={(e) => setSalesData({ ...salesData, sales_lag_7: parseFloat(e.target.value) })} className="w-full p-2 border rounded-lg bg-gray-50" required />
                    </div>
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">Roll Mean 7</label>
                      <input type="number" step="0.1" value={salesData.rolling_mean_7} onChange={(e) => setSalesData({ ...salesData, rolling_mean_7: parseFloat(e.target.value) })} className="w-full p-2 border rounded-lg bg-gray-50" required />
                    </div>
                  </div>
                </div>

                <div className="pt-4">
                  <button type="submit" disabled={loading} className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-xl shadow-md transition-transform transform hover:scale-[1.02] disabled:opacity-50">
                    {loading ? 'Analyzing...' : 'Predict Sales Revenue'}
                  </button>
                </div>
              </form>
            ) : (
              <form onSubmit={handleChurnSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Recency (Days)</label>
                    <input type="number" value={churnData.recency} onChange={(e) => setChurnData({ ...churnData, recency: parseInt(e.target.value) })} className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" required />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Frequency</label>
                    <input type="number" value={churnData.frequency} onChange={(e) => setChurnData({ ...churnData, frequency: parseInt(e.target.value) })} className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" required />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Total Spend</label>
                    <input type="number" step="0.01" value={churnData.monetary} onChange={(e) => setChurnData({ ...churnData, monetary: parseFloat(e.target.value) })} className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" required />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Lifestage</label>
                    <select value={churnData.lifestage} onChange={(e) => setChurnData({ ...churnData, lifestage: e.target.value })} className="w-full p-2 border rounded-lg bg-white" required>
                      {['YOUNG SINGLES/COUPLES', 'MIDAGE SINGLES/COUPLES', 'OLDER SINGLES/COUPLES', 'YOUNG FAMILIES', 'MIDAGE FAMILIES', 'OLDER FAMILIES', 'RETIREES', 'NEW FAMILIES'].map(opt => (
                        <option key={opt} value={opt}>{opt}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Premium Status</label>
                    <select value={churnData.premium_customer} onChange={(e) => setChurnData({ ...churnData, premium_customer: e.target.value })} className="w-full p-2 border rounded-lg bg-white" required>
                      {['Budget', 'Mainstream', 'Premium'].map(opt => (
                        <option key={opt} value={opt}>{opt}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="pt-4">
                  <button type="submit" disabled={loading} className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-4 rounded-xl shadow-md transition-transform transform hover:scale-[1.02] disabled:opacity-50">
                    {loading ? 'Analyzing...' : 'Predict Churn Risk'}
                  </button>
                </div>
              </form>
            )}
          </div>

          {/* Results Column */}
          <div className="md:col-span-1 space-y-6">
            <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100 h-full flex flex-col items-center justify-center text-center">
              {result ? (
                <div className="animate-fade-in-up w-full">
                  <p className="text-gray-500 font-medium uppercase tracking-wide text-xs mb-2">Prediction Result</p>

                  {activeTab === 'sales' ? (
                    <div className="bg-blue-50 rounded-xl p-6 border border-blue-100">
                      <p className="text-3xl font-extrabold text-blue-700">${result.predicted_sales.toFixed(2)}</p>
                      <p className="text-sm text-blue-600 mt-1">Predicted Sales</p>
                      <div className="mt-4 text-xs text-gray-400">Store: {result.store_nbr} | Date: {result.date}</div>
                    </div>
                  ) : (
                    <div className={`rounded-xl p-6 border ${result.churn_prediction === 'Churn' ? 'bg-red-50 border-red-100' : 'bg-green-50 border-green-100'}`}>
                      <p className={`text-2xl font-bold ${result.churn_prediction === 'Churn' ? 'text-red-600' : 'text-green-600'}`}>
                        {result.churn_prediction}
                      </p>
                      <p className="text-sm text-gray-600 mt-2">Probability: {(result.churn_probability * 100).toFixed(1)}%</p>
                      <div className={`mt-3 inline-block px-3 py-1 rounded-full text-xs font-bold ${result.risk_level === 'High' ? 'bg-red-200 text-red-800' :
                        result.risk_level === 'Medium' ? 'bg-yellow-200 text-yellow-800' : 'bg-green-200 text-green-800'
                        }`}>
                        Risk Level: {result.risk_level}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-gray-400">
                  <div className="w-16 h-16 bg-gray-100 rounded-full mx-auto mb-4 flex items-center justify-center text-2xl">🔮</div>
                  <p>Enter parameters and hit predict to see results.</p>
                </div>
              )}
            </div>

            <div className="bg-gradient-to-br from-gray-800 to-gray-900 text-white p-6 rounded-xl shadow-lg">
              <h3 className="font-bold mb-2">💡 Quick Tips</h3>
              <ul className="text-sm space-y-2 text-gray-300">
                {activeTab === 'sales' ? (
                  <>
                    <li>• <strong>Lag 1</strong> refers to yesterday's sales figures.</li>
                    <li>• <strong>Rolling Mean</strong> helps smooth out daily fluctuations.</li>
                  </>
                ) : (
                  <>
                    <li>• <strong>Recency</strong> is the strongest predictor of churn.</li>
                    <li>• High risk customers should be targeted with retention offers immediately.</li>
                  </>
                )}
              </ul>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
