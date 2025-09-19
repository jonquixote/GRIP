import { AlertTriangle, X } from 'lucide-react';

const RiskAlertsPanel = () => {
  // In a real app, these would come from the backend
  const alerts = [
    {
      id: 1,
      title: 'Supply Disruption',
      description: 'Copper supply from Chile may be affected due to mining strikes',
      severity: 'high',
      time: '2 hours ago',
    },
    {
      id: 2,
      title: 'Geopolitical Tension',
      description: 'Trade restrictions on rare earth elements from China',
      severity: 'medium',
      time: '5 hours ago',
    },
    {
      id: 3,
      title: 'Market Volatility',
      description: 'Gold prices experiencing unusual fluctuations',
      severity: 'low',
      time: '1 day ago',
    },
  ];

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100';
      case 'low':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-100';
    }
  };

  return (
    <div className="mt-6 bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
      <div className="px-4 py-5 sm:px-6 border-b border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white">Risk Alerts</h3>
      </div>
      <div className="divide-y divide-gray-200 dark:divide-gray-700">
        {alerts.map((alert) => (
          <div key={alert.id} className="px-4 py-4 sm:px-6 hover:bg-gray-50 dark:hover:bg-gray-750">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <AlertTriangle className="h-5 w-5 text-red-500" />
              </div>
              <div className="ml-3 flex-1">
                <div className="flex items-center justify-between">
                  <h4 className="text-sm font-medium text-gray-900 dark:text-white">
                    {alert.title}
                  </h4>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getSeverityColor(alert.severity)}`}>
                    {alert.severity.charAt(0).toUpperCase() + alert.severity.slice(1)}
                  </span>
                </div>
                <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                  {alert.description}
                </p>
                <div className="mt-2 flex justify-between">
                  <p className="text-xs text-gray-400 dark:text-gray-500">
                    {alert.time}
                  </p>
                  <button className="text-xs text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300">
                    View Details
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RiskAlertsPanel;