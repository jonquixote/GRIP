import { useState } from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import { Download, BarChart3, TrendingUp, PieChartIcon } from 'lucide-react';

const AnalyticsTab = () => {
  const [timeRange, setTimeRange] = useState('30');
  const [chartType, setChartType] = useState('bar');

  // Mock data - in a real app this would come from the backend
  const productionData = [
    { name: 'Gold', value: 4000 },
    { name: 'Silver', value: 3000 },
    { name: 'Copper', value: 2000 },
    { name: 'Iron', value: 2780 },
    { name: 'Aluminum', value: 1890 },
    { name: 'Zinc', value: 2390 },
    { name: 'Lead', value: 3490 },
  ];

  const priceTrendData = [
    { date: 'Jan', price: 4000 },
    { date: 'Feb', price: 3000 },
    { date: 'Mar', price: 2000 },
    { date: 'Apr', price: 2780 },
    { date: 'May', price: 1890 },
    { date: 'Jun', price: 2390 },
    { date: 'Jul', price: 3490 },
  ];

  const reserveData = [
    { name: 'Africa', value: 400 },
    { name: 'Asia', value: 300 },
    { name: 'Europe', value: 300 },
    { name: 'North America', value: 200 },
    { name: 'South America', value: 278 },
    { name: 'Oceania', value: 189 },
  ];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D'];

  const insights = [
    {
      title: 'Market Trend',
      description: 'Gold prices increased by 5% this quarter',
      trend: 'up',
    },
    {
      title: 'Supply Chain',
      description: 'Copper production down 3% due to mining strikes',
      trend: 'down',
    },
    {
      title: 'Demand Forecast',
      description: 'Aluminum demand expected to rise 8% next quarter',
      trend: 'up',
    },
  ];

  return (
    <div>
      {/* Controls */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setTimeRange('7')}
            className={`px-3 py-1 text-sm rounded-md ${
              timeRange === '7'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
            }`}
          >
            7 Days
          </button>
          <button
            onClick={() => setTimeRange('30')}
            className={`px-3 py-1 text-sm rounded-md ${
              timeRange === '30'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
            }`}
          >
            30 Days
          </button>
          <button
            onClick={() => setTimeRange('90')}
            className={`px-3 py-1 text-sm rounded-md ${
              timeRange === '90'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
            }`}
          >
            90 Days
          </button>
          <button
            onClick={() => setTimeRange('365')}
            className={`px-3 py-1 text-sm rounded-md ${
              timeRange === '365'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
            }`}
          >
            1 Year
          </button>
          <button
            onClick={() => setTimeRange('all')}
            className={`px-3 py-1 text-sm rounded-md ${
              timeRange === 'all'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
            }`}
          >
            All Time
          </button>
        </div>

        <div className="flex items-center space-x-2">
          <span className="text-sm text-gray-700 dark:text-gray-300">Chart Type:</span>
          <div className="flex rounded-md shadow-sm">
            <button
              onClick={() => setChartType('bar')}
              className={`px-3 py-1 text-sm rounded-l-md ${
                chartType === 'bar'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
              }`}
            >
              <BarChart3 size={16} />
            </button>
            <button
              onClick={() => setChartType('line')}
              className={`px-3 py-1 text-sm ${
                chartType === 'line'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
              }`}
            >
              <TrendingUp size={16} />
            </button>
            <button
              onClick={() => setChartType('pie')}
              className={`px-3 py-1 text-sm rounded-r-md ${
                chartType === 'pie'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
              }`}
            >
              <PieChartIcon size={16} />
            </button>
          </div>
          <button className="flex items-center px-3 py-1 text-sm bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600">
            <Download size={16} className="mr-1" />
            Export
          </button>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Production Volume Chart */}
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Production Volume by Commodity</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              {chartType === 'bar' ? (
                <BarChart data={productionData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="value" fill="#8884d8" />
                </BarChart>
              ) : chartType === 'line' ? (
                <LineChart data={productionData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="value" stroke="#8884d8" activeDot={{ r: 8 }} />
                </LineChart>
              ) : (
                <PieChart>
                  <Pie
                    data={productionData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  >
                    {productionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              )}
            </ResponsiveContainer>
          </div>
        </div>

        {/* Price Trend Chart */}
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Price Trends</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              {chartType === 'bar' ? (
                <BarChart data={priceTrendData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="price" fill="#82ca9d" />
                </BarChart>
              ) : chartType === 'line' ? (
                <LineChart data={priceTrendData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="price" stroke="#82ca9d" activeDot={{ r: 8 }} />
                </LineChart>
              ) : (
                <PieChart>
                  <Pie
                    data={priceTrendData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={80}
                    fill="#82ca9d"
                    dataKey="price"
                    label={({ date, percent }) => `${date} ${(percent * 100).toFixed(0)}%`}
                  >
                    {priceTrendData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              )}
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Reserve Distribution Chart */}
      <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow mb-6">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Reserve Distribution by Region</h3>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={reserveData}
                cx="50%"
                cy="50%"
                labelLine={true}
                outerRadius={80}
                fill="#ffc658"
                dataKey="value"
                label={({ name, value }) => `${name}: ${value}`}
              >
                {reserveData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Market Insights */}
      <div>
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Key Market Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {insights.map((insight, index) => (
            <div key={index} className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
              <div className="flex items-start">
                <div className={`flex-shrink-0 h-6 w-6 rounded-full flex items-center justify-center ${
                  insight.trend === 'up' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'
                }`}>
                  {insight.trend === 'up' ? '↑' : '↓'}
                </div>
                <div className="ml-3">
                  <h4 className="text-sm font-medium text-gray-900 dark:text-white">{insight.title}</h4>
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{insight.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AnalyticsTab;