import { useState, useEffect } from 'react';
import Sidebar from '../components/layout/Sidebar';
import Header from '../components/layout/Header';
import OverviewTab from '../components/tabs/OverviewTab';
import AnalyticsTab from '../components/tabs/AnalyticsTab';
import PredictionsTab from '../components/tabs/PredictionsTab';
import TrendsTab from '../components/tabs/TrendsTab';
import RiskAlertsPanel from '../components/dashboard/RiskAlertsPanel';
import KeyMetrics from '../components/dashboard/KeyMetrics';
import { commodityService } from '../services/api';

const Dashboard = ({ darkMode, setDarkMode }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [commodities, setCommodities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCommodities();
  }, []);

  const fetchCommodities = async () => {
    try {
      setLoading(true);
      const response = await commodityService.getAll();
      setCommodities(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch commodities');
      console.error('Error fetching commodities:', err);
    } finally {
      setLoading(false);
    }
  };

  const refreshData = () => {
    fetchCommodities();
  };

  return (
    <div className="flex h-screen bg-gray-100 dark:bg-gray-900">
      <Sidebar darkMode={darkMode} setDarkMode={setDarkMode} />
      
      {/* Main content area with left margin to account for sidebar on desktop */}
      <div className="flex-1 flex flex-col overflow-hidden md:ml-64">
        <Header darkMode={darkMode} setDarkMode={setDarkMode} refreshData={refreshData} />
        
        <main className="flex-1 overflow-y-auto p-4 md:p-6">
          {/* Key Metrics */}
          <KeyMetrics commodities={commodities} />
          
          {/* Risk Alerts */}
          <RiskAlertsPanel />
          
          {/* Tab Navigation */}
          <div className="mt-6">
            <div className="border-b border-gray-200 dark:border-gray-700">
              <nav className="-mb-px flex space-x-8">
                <button
                  onClick={() => setActiveTab('overview')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'overview'
                      ? 'border-blue-500 text-blue-600 dark:text-blue-400 dark:border-blue-400'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                  }`}
                >
                  Overview
                </button>
                <button
                  onClick={() => setActiveTab('analytics')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'analytics'
                      ? 'border-blue-500 text-blue-600 dark:text-blue-400 dark:border-blue-400'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                  }`}
                >
                  Analytics
                </button>
                <button
                  onClick={() => setActiveTab('predictions')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'predictions'
                      ? 'border-blue-500 text-blue-600 dark:text-blue-400 dark:border-blue-400'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                  }`}
                >
                  Predictions
                </button>
                <button
                  onClick={() => setActiveTab('trends')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'trends'
                      ? 'border-blue-500 text-blue-600 dark:text-blue-400 dark:border-blue-400'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                  }`}
                >
                  Trends
                </button>
              </nav>
            </div>
          </div>
          
          {/* Tab Content */}
          <div className="mt-6">
            {activeTab === 'overview' && <OverviewTab commodities={commodities} loading={loading} error={error} />}
            {activeTab === 'analytics' && <AnalyticsTab />}
            {activeTab === 'predictions' && <PredictionsTab />}
            {activeTab === 'trends' && <TrendsTab />}
          </div>
        </main>
      </div>
    </div>
  );
};

export default Dashboard;