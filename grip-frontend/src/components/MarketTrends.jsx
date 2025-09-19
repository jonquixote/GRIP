import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts';
import { 
  TrendingUp, 
  TrendingDown, 
  Activity, 
  Globe, 
  AlertTriangle,
  Star,
  Zap,
  BarChart3,
  PieChart as PieChartIcon,
  Target
} from 'lucide-react';
import { motion } from 'framer-motion';

const MarketTrends = () => {
  const [trendsData, setTrendsData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTrends();
  }, []);

  const fetchTrends = async () => {
    try {
      setLoading(true);
      // Mock data for now
      const mockData = {
        trending_up: [
          { id: 1, name: 'Lithium', trend_strength: 0.85 },
          { id: 2, name: 'Cobalt', trend_strength: 0.72 },
          { id: 3, name: 'Copper', trend_strength: 0.68 }
        ],
        trending_down: [
          { id: 4, name: 'Lead', trend_strength: 0.65 },
          { id: 5, name: 'Zinc', trend_strength: 0.58 }
        ],
        stable: [
          { id: 6, name: 'Gold', trend_strength: 0.45 },
          { id: 7, name: 'Silver', trend_strength: 0.42 }
        ],
        high_volatility: [
          { id: 1, name: 'Lithium', volatility: 0.12 },
          { id: 8, name: 'Nickel', volatility: 0.09 },
          { id: 3, name: 'Copper', volatility: 0.07 }
        ]
      };
      setTrendsData(mockData);
    } catch (error) {
      console.error('Error fetching trends:', error);
    } finally {
      setLoading(false);
    }
  };

  // Mock data for demonstration
  const mockTrendsData = {
    trending_up: [
      { id: 1, name: 'Lithium', trend_strength: 0.85 },
      { id: 2, name: 'Cobalt', trend_strength: 0.72 },
      { id: 3, name: 'Copper', trend_strength: 0.68 }
    ],
    trending_down: [
      { id: 4, name: 'Lead', trend_strength: 0.65 },
      { id: 5, name: 'Zinc', trend_strength: 0.58 }
    ],
    stable: [
      { id: 6, name: 'Gold', trend_strength: 0.45 },
      { id: 7, name: 'Silver', trend_strength: 0.42 }
    ],
    high_volatility: [
      { id: 1, name: 'Lithium', volatility: 0.12 },
      { id: 8, name: 'Nickel', volatility: 0.09 },
      { id: 3, name: 'Copper', volatility: 0.07 }
    ]
  };

  const displayData = trendsData || mockTrendsData;

  // Generate market performance data
  const generateMarketPerformanceData = () => {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return months.map(month => ({
      month,
      baseMetals: Math.floor(Math.random() * 200) + 800,
      preciousMetals: Math.floor(Math.random() * 300) + 1200,
      criticalMetals: Math.floor(Math.random() * 400) + 600,
      energy: Math.floor(Math.random() * 150) + 400
    }));
  };

  // Generate sector performance data
  const generateSectorData = () => [
    { name: 'Base Metals', value: 35, growth: 5.2 },
    { name: 'Precious Metals', value: 25, growth: -2.1 },
    { name: 'Critical Metals', value: 30, growth: 12.8 },
    { name: 'Energy', value: 10, growth: 3.4 }
  ];

  // Generate regional performance data
  const generateRegionalData = () => [
    { region: 'Asia-Pacific', production: 45, reserves: 38, growth: 6.2 },
    { region: 'North America', production: 25, reserves: 28, growth: 3.1 },
    { region: 'Europe', production: 15, reserves: 18, growth: 1.8 },
    { region: 'South America', production: 10, reserves: 12, growth: 4.5 },
    { region: 'Africa', production: 5, reserves: 4, growth: 8.9 }
  ];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Trend Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-950 dark:to-green-900 border-green-200 dark:border-green-800">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Trending Up</CardTitle>
            <TrendingUp className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-700 dark:text-green-300">
              {displayData.trending_up?.length || 0}
            </div>
            <p className="text-xs text-green-600 dark:text-green-400">
              Commodities rising
            </p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-red-50 to-red-100 dark:from-red-950 dark:to-red-900 border-red-200 dark:border-red-800">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Trending Down</CardTitle>
            <TrendingDown className="h-4 w-4 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-700 dark:text-red-300">
              {displayData.trending_down?.length || 0}
            </div>
            <p className="text-xs text-red-600 dark:text-red-400">
              Commodities falling
            </p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-950 dark:to-blue-900 border-blue-200 dark:border-blue-800">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Stable</CardTitle>
            <Activity className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-700 dark:text-blue-300">
              {displayData.stable?.length || 0}
            </div>
            <p className="text-xs text-blue-600 dark:text-blue-400">
              Sideways movement
            </p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-950 dark:to-orange-900 border-orange-200 dark:border-orange-800">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">High Volatility</CardTitle>
            <Zap className="h-4 w-4 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-700 dark:text-orange-300">
              {displayData.high_volatility?.length || 0}
            </div>
            <p className="text-xs text-orange-600 dark:text-orange-400">
              Highly volatile
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Trending Commodities */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Trending Up */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2 text-green-600">
              <TrendingUp className="h-5 w-5" />
              <span>Trending Up</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {displayData.trending_up?.map((commodity, index) => (
                <motion.div
                  key={commodity.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="flex items-center justify-between p-3 bg-green-50 dark:bg-green-950 rounded-lg"
                >
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                      {index + 1}
                    </div>
                    <span className="font-medium">{commodity.name}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="text-sm text-green-600">
                      {(commodity.trend_strength * 100).toFixed(0)}%
                    </div>
                    <TrendingUp className="h-4 w-4 text-green-500" />
                  </div>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Trending Down */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2 text-red-600">
              <TrendingDown className="h-5 w-5" />
              <span>Trending Down</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {displayData.trending_down?.map((commodity, index) => (
                <motion.div
                  key={commodity.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="flex items-center justify-between p-3 bg-red-50 dark:bg-red-950 rounded-lg"
                >
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                      {index + 1}
                    </div>
                    <span className="font-medium">{commodity.name}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="text-sm text-red-600">
                      {(commodity.trend_strength * 100).toFixed(0)}%
                    </div>
                    <TrendingDown className="h-4 w-4 text-red-500" />
                  </div>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Stable Commodities */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2 text-blue-600">
              <Activity className="h-5 w-5" />
              <span>Stable</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {displayData.stable?.map((commodity, index) => (
                <motion.div
                  key={commodity.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="flex items-center justify-between p-3 bg-blue-50 dark:bg-blue-950 rounded-lg"
                >
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                      {index + 1}
                    </div>
                    <span className="font-medium">{commodity.name}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="text-sm text-blue-600">
                      {(commodity.trend_strength * 100).toFixed(0)}%
                    </div>
                    <Activity className="h-4 w-4 text-blue-500" />
                  </div>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Trends Analysis */}
      <Tabs defaultValue="market" className="space-y-6">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="market">Market Performance</TabsTrigger>
          <TabsTrigger value="sector">Sector Analysis</TabsTrigger>
          <TabsTrigger value="regional">Regional Trends</TabsTrigger>
        </TabsList>

        <TabsContent value="market" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <BarChart3 className="h-5 w-5" />
                <span>Market Performance Over Time</span>
              </CardTitle>
              <CardDescription>
                Monthly performance across different commodity sectors
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart
                  data={generateMarketPerformanceData()}
                  margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="baseMetals" stroke="#8884d8" name="Base Metals" />
                  <Line type="monotone" dataKey="preciousMetals" stroke="#82ca9d" name="Precious Metals" />
                  <Line type="monotone" dataKey="criticalMetals" stroke="#ffc658" name="Critical Metals" />
                  <Line type="monotone" dataKey="energy" stroke="#ff8042" name="Energy" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="sector" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <PieChartIcon className="h-5 w-5" />
                  <span>Sector Distribution</span>
                </CardTitle>
                <CardDescription>
                  Market share by commodity sector
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={generateSectorData()}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    >
                      {generateSectorData().map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Target className="h-5 w-5" />
                  <span>Sector Growth Rates</span>
                </CardTitle>
                <CardDescription>
                  Year-over-year growth by sector
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart
                    data={generateSectorData()}
                    layout="vertical"
                    margin={{ top: 5, right: 30, left: 60, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" domain={[-10, 20]} />
                    <YAxis dataKey="name" type="category" />
                    <Tooltip />
                    <Bar dataKey="growth" name="Growth Rate (%)">
                      {generateSectorData().map((entry, index) => (
                        <Cell 
                          key={`cell-${index}`} 
                          fill={entry.growth > 0 ? '#10B981' : '#EF4444'} 
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="regional" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Globe className="h-5 w-5" />
                <span>Regional Analysis</span>
              </CardTitle>
              <CardDescription>
                Production, reserves, and growth by region
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={generateRegionalData()}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="region" />
                  <PolarRadiusAxis angle={30} domain={[0, 50]} />
                  <Radar
                    name="Production (%)"
                    dataKey="production"
                    stroke="#8884d8"
                    fill="#8884d8"
                    fillOpacity={0.6}
                  />
                  <Radar
                    name="Reserves (%)"
                    dataKey="reserves"
                    stroke="#82ca9d"
                    fill="#82ca9d"
                    fillOpacity={0.6}
                  />
                  <Tooltip />
                </RadarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default MarketTrends;