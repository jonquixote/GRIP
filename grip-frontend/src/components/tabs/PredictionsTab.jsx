import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, Shield, Activity } from 'lucide-react';

const PredictionsTab = () => {
  // Mock data - in a real app this would come from the backend
  const predictionData = [
    { date: '2023-06', actual: 4000, predicted: 4200 },
    { date: '2023-07', actual: 3000, predicted: 3100 },
    { date: '2023-08', actual: 2000, predicted: 2200 },
    { date: '2023-09', actual: 2780, predicted: 2800 },
    { date: '2023-10', actual: 1890, predicted: 2000 },
    { date: '2023-11', actual: 2390, predicted: 2500 },
    { date: '2023-12', actual: null, predicted: 3200 },
    { date: '2024-01', actual: null, predicted: 3500 },
    { date: '2024-02', actual: null, predicted: 3800 },
    { date: '2024-03', actual: null, predicted: 4100 },
  ];

  const confidenceData = [
    { commodity: 'Gold', confidence: 92 },
    { commodity: 'Silver', confidence: 87 },
    { commodity: 'Copper', confidence: 78 },
    { commodity: 'Iron', confidence: 85 },
    { commodity: 'Aluminum', confidence: 90 },
  ];

  const modelPerformance = [
    { metric: 'Accuracy', value: 92.5 },
    { metric: 'Precision', value: 88.3 },
    { metric: 'Recall', value: 90.1 },
    { metric: 'F1 Score', value: 89.2 },
  ];

  return (
    <div>
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="rounded-md bg-blue-100 p-3 dark:bg-blue-900">
              <TrendingUp className="h-6 w-6 text-blue-600 dark:text-blue-300" />
            </div>
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-900 dark:text-white">Prediction Accuracy</h3>
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">92.5%</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="rounded-md bg-green-100 p-3 dark:bg-green-900">
              <Shield className="h-6 w-6 text-green-600 dark:text-green-300" />
            </div>
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-900 dark:text-white">Model Confidence</h3>
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">85.7%</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="rounded-md bg-purple-100 p-3 dark:bg-purple-900">
              <Activity className="h-6 w-6 text-purple-600 dark:text-purple-300" />
            </div>
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-900 dark:text-white">Active Models</h3>
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">12</p>
            </div>
          </div>
        </div>
      </div>

      {/* Prediction Chart */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow mb-6">
        <div className="px-6 py-5 border-b border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white">Price Predictions</h3>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Historical data vs AI predictions with confidence intervals
          </p>
        </div>
        <div className="p-6 h-96">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={predictionData}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="actual"
                stroke="#8884d8"
                activeDot={{ r: 8 }}
                name="Actual Price"
                strokeWidth={2}
              />
              <Line
                type="monotone"
                dataKey="predicted"
                stroke="#82ca9d"
                name="Predicted Price"
                strokeWidth={2}
                strokeDasharray="3 3"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Confidence Scores */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
          <div className="px-6 py-5 border-b border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">Confidence by Commodity</h3>
          </div>
          <div className="p-6 h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={confidenceData}
                layout="vertical"
                margin={{
                  top: 5,
                  right: 30,
                  left: 60,
                  bottom: 5,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" domain={[0, 100]} />
                <YAxis dataKey="commodity" type="category" />
                <Tooltip />
                <Legend />
                <Bar dataKey="confidence" fill="#8884d8" name="Confidence Score">
                  {confidenceData.map((entry, index) => (
                    <rect key={`rect-${index}`} fill={entry.confidence > 85 ? '#10B981' : entry.confidence > 75 ? '#F59E0B' : '#EF4444'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Model Performance */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
          <div className="px-6 py-5 border-b border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">Model Performance Metrics</h3>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {modelPerformance.map((metric, index) => (
                <div key={index}>
                  <div className="flex justify-between mb-1">
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{metric.metric}</span>
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{metric.value}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2 dark:bg-gray-700">
                    <div
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ width: `${metric.value}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Forecast Summary */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
        <div className="px-6 py-5 border-b border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white">Forecast Summary</h3>
        </div>
        <div className="p-6">
          <div className="prose max-w-none dark:prose-invert">
            <p className="text-gray-700 dark:text-gray-300">
              Our AI models predict a bullish trend for precious metals over the next quarter, with gold expected to reach $2,100 per ounce by March 2024. Industrial metals like copper and aluminum show mixed signals, with supply chain concerns offsetting steady demand growth.
            </p>
            <p className="mt-4 text-gray-700 dark:text-gray-300">
              Key factors influencing these predictions include:
            </p>
            <ul className="mt-2 list-disc pl-5 space-y-1 text-gray-700 dark:text-gray-300">
              <li>Global economic recovery patterns</li>
              <li>Central bank policy changes</li>
              <li>Geopolitical tensions affecting supply chains</li>
              <li>Technological adoption rates in emerging markets</li>
            </ul>
            <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/30 rounded-lg">
              <h4 className="text-sm font-medium text-blue-800 dark:text-blue-200">Recommendation</h4>
              <p className="mt-1 text-sm text-blue-700 dark:text-blue-300">
                Based on our analysis, we recommend increasing exposure to precious metals while maintaining a diversified portfolio across commodity sectors.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PredictionsTab;