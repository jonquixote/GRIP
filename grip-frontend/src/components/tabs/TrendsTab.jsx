import { BarChart, Bar, LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Globe, TrendingUp, Activity, AlertTriangle } from 'lucide-react';

const TrendsTab = () => {
  // Mock data - in a real app this would come from the backend
  const regionalData = [
    { region: 'North America', trend: 2.3, risk: 15 },
    { region: 'South America', trend: 3.1, risk: 28 },
    { region: 'Europe', trend: 1.8, risk: 12 },
    { region: 'Asia', trend: 4.2, risk: 35 },
    { region: 'Africa', trend: 3.7, risk: 42 },
    { region: 'Oceania', trend: 1.2, risk: 8 },
  ];

  const volatilityData = [
    { date: 'Jan', volatility: 12 },
    { date: 'Feb', volatility: 15 },
    { date: 'Mar', volatility: 10 },
    { date: 'Apr', volatility: 18 },
    { date: 'May', volatility: 22 },
    { date: 'Jun', volatility: 19 },
    { date: 'Jul', volatility: 14 },
    { date: 'Aug', volatility: 16 },
    { date: 'Sep', volatility: 20 },
  ];

  const supplyChainRisk = [
    { factor: 'Geopolitical', score: 75 },
    { factor: 'Natural Disasters', score: 45 },
    { factor: 'Transportation', score: 60 },
    { factor: 'Regulatory', score: 55 },
    { factor: 'Market Demand', score: 70 },
  ];

  return (
    <div>
      {/* Regional Analysis */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow mb-6">
        <div className="px-6 py-5 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center">
            <Globe className="h-5 w-5 text-blue-500 mr-2" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">Regional Market Analysis</h3>
          </div>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Trend Chart */}
            <div>
              <h4 className="text-md font-medium text-gray-900 dark:text-white mb-4">Growth Trends by Region</h4>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={regionalData}
                    margin={{
                      top: 5,
                      right: 30,
                      left: 20,
                      bottom: 5,
                    }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="region" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="trend" fill="#8884d8" name="Growth Trend (%)" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Risk Chart */}
            <div>
              <h4 className="text-md font-medium text-gray-900 dark:text-white mb-4">Supply Chain Risk by Region</h4>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={regionalData}
                    margin={{
                      top: 5,
                      right: 30,
                      left: 20,
                      bottom: 5,
                    }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="region" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="risk" fill="#ff6b6b" name="Risk Score" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Global Trends */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Volatility Chart */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
          <div className="px-6 py-5 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center">
              <Activity className="h-5 w-5 text-green-500 mr-2" />
              <h3 className="text-lg font-medium text-gray-900 dark:text-white">Market Volatility Index</h3>
            </div>
          </div>
          <div className="p-6 h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart
                data={volatilityData}
                margin={{
                  top: 10,
                  right: 30,
                  left: 0,
                  bottom: 0,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Area type="monotone" dataKey="volatility" stroke="#8884d8" fill="#8884d8" fillOpacity={0.3} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Supply Chain Risk */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
          <div className="px-6 py-5 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center">
              <AlertTriangle className="h-5 w-5 text-yellow-500 mr-2" />
              <h3 className="text-lg font-medium text-gray-900 dark:text-white">Supply Chain Risk Factors</h3>
            </div>
          </div>
          <div className="p-6 h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={supplyChainRisk}
                layout="vertical"
                margin={{
                  top: 5,
                  right: 30,
                  left: 100,
                  bottom: 5,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="factor" type="category" />
                <Tooltip />
                <Bar dataKey="score" fill="#ffc658" name="Risk Score">
                  {supplyChainRisk.map((entry, index) => (
                    <rect key={`rect-${index}`} fill={entry.score > 70 ? '#EF4444' : entry.score > 50 ? '#F59E0B' : '#10B981'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Trend Analysis Summary */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
        <div className="px-6 py-5 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center">
            <TrendingUp className="h-5 w-5 text-purple-500 mr-2" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">Global Trend Analysis</h3>
          </div>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-5">
              <h4 className="font-medium text-gray-900 dark:text-white">Emerging Markets</h4>
              <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                Asia-Pacific region shows strongest growth potential with 4.2% projected annual increase in mineral production.
              </p>
              <div className="mt-4 flex items-center">
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100">
                  +4.2%
                </span>
                <span className="ml-2 text-xs text-gray-500 dark:text-gray-400">YoY Growth</span>
              </div>
            </div>

            <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-5">
              <h4 className="font-medium text-gray-900 dark:text-white">Supply Constraints</h4>
              <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                African operations face highest risk with 42% supply chain disruption probability due to infrastructure challenges.
              </p>
              <div className="mt-4 flex items-center">
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100">
                  42% Risk
                </span>
                <span className="ml-2 text-xs text-gray-500 dark:text-gray-400">Disruption</span>
              </div>
            </div>

            <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-5">
              <h4 className="font-medium text-gray-900 dark:text-white">Technology Impact</h4>
              <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                Automation and AI adoption expected to increase mining efficiency by 15-20% over next 3 years.
              </p>
              <div className="mt-4 flex items-center">
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100">
                  +18%
                </span>
                <span className="ml-2 text-xs text-gray-500 dark:text-gray-400">Efficiency</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TrendsTab;