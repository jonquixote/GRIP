import { Package, TrendingUp, AlertTriangle, BarChart3 } from 'lucide-react';

const KeyMetrics = ({ commodities }) => {
  // In a real app, these would come from the backend
  const totalCommodities = commodities.length;
  const positiveOutlook = Math.floor(totalCommodities * 0.6);
  const highRisk = Math.floor(totalCommodities * 0.2);
  const marketSentiment = 'Bullish';

  const metrics = [
    {
      name: 'Total Commodities Tracked',
      value: totalCommodities,
      icon: Package,
      color: 'bg-blue-500',
    },
    {
      name: 'Positive Outlook',
      value: positiveOutlook,
      icon: TrendingUp,
      color: 'bg-green-500',
    },
    {
      name: 'High Risk',
      value: highRisk,
      icon: AlertTriangle,
      color: 'bg-red-500',
    },
    {
      name: 'Market Sentiment',
      value: marketSentiment,
      icon: BarChart3,
      color: 'bg-purple-500',
    },
  ];

  return (
    <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
      {metrics.map((metric) => {
        const Icon = metric.icon;
        return (
          <div
            key={metric.name}
            className="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg"
          >
            <div className="p-5">
              <div className="flex items-center">
                <div className={`flex-shrink-0 rounded-md p-3 ${metric.color} text-white`}>
                  <Icon className="h-6 w-6" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
                      {metric.name}
                    </dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900 dark:text-white">
                        {metric.value}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default KeyMetrics;