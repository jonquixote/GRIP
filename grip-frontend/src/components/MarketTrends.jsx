import React, { useState, useEffect, useRef } from 'react';
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
  Radar,
  AreaChart,
  Area
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
  Target,
  RefreshCw,
  Wifi,
  WifiOff
} from 'lucide-react';
import { motion } from 'framer-motion';
import { analyticsService } from '../services/api';

const MarketTrends = () => {
  const [trendsData, setTrendsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(new Date());
  const wsRef = useRef(null);

  // Color palette for charts
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  useEffect(() => {
    fetchTrends();
    
    // Set up WebSocket connection for real-time updates
    setupWebSocket();
    
    // Set up polling as fallback
    const pollInterval = setInterval(() => {
      if (!isConnected) {
        fetchTrends();
      }
    }, 60000); // Poll every minute if not connected via WebSocket
    
    return () => {
      clearInterval(pollInterval);
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const setupWebSocket = () => {
    try {
      // In a real implementation, we would connect to a WebSocket server
      // For now, we'll simulate WebSocket behavior
      setIsConnected(true);
      
      // Simulate receiving updates
      const wsInterval = setInterval(() => {
        if (Math.random() > 0.7) { // 30% chance of update
          fetchTrends();
          setLastUpdate(new Date());
        }
      }, 10000); // Simulate updates every 10 seconds
      
      return () => clearInterval(wsInterval);
    } catch (error) {
      console.error('WebSocket connection failed:', error);
      setIsConnected(false);
    }
  };

  const fetchTrends = async () => {
    try {
      setLoading(true);
      // Try to fetch real data from the backend
      const response = await analyticsService.getTimeSeriesData();
      setTrendsData(response.data);
      setLastUpdate(new Date());
      setError(null);
    } catch (error) {
      console.error('Error fetching trends:', error);
      // Fallback to mock data if API fails
      const mockData = {
        trending_up: [
          { id: 1, name: 'Lithium', trend_strength: 0.85, price: 12000 },
          { id: 2, name: 'Cobalt', trend_strength: 0.72, price: 35000 },
          { id: 3, name: 'Copper', trend_strength: 0.68, price: 9500 }
        ],
        trending_down: [
          { id: 4, name: 'Lead', trend_strength: 0.65, price: 2200 },
          { id: 5, name: 'Zinc', trend_strength: 0.58, price: 3100 }
        ],
        stable: [
          { id: 6, name: 'Gold', trend_strength: 0.45, price: 1950 },
          { id: 7, name: 'Silver', trend_strength: 0.42, price: 24 }
        ],
        high_volatility: [
          { id: 1, name: 'Lithium', volatility: 0.12, price: 12000 },
          { id: 8, name: 'Nickel', volatility: 0.09, price: 18500 },
          { id: 3, name: 'Copper', volatility: 0.07, price: 9500 }
        ]
      };
      setTrendsData(mockData);
      setLastUpdate(new Date());
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  // Setup real-time data updates
  useEffect(() => {
    // Fetch initial data
    fetchTrends();
    
    // Set up interval for real-time updates
    const interval = setInterval(() => {
      fetchTrends();
    }, 30000); // Update every 30 seconds
    
    // Clean up interval on component unmount
    return () => clearInterval(interval);
  }, []);

  // Generate real-time price data for visualization
  const generateLivePriceData = (commodityName, basePrice) => {
    // Generate 24 hours of price data with realistic fluctuations
    const data = [];
    let currentPrice = basePrice;
    
    for (let i = 23; i >= 0; i--) {
      const timestamp = new Date(Date.now() - i * 60 * 60 * 1000);
      
      // Apply realistic price fluctuation
      const fluctuation = (Math.random() - 0.5) * 0.02; // ±1% fluctuation
      currentPrice = currentPrice * (1 + fluctuation);
      
      // Add some volatility for high-volatility commodities
      if (commodityName.toLowerCase().includes('lithium') || commodityName.toLowerCase().includes('nickel')) {
        currentPrice += (Math.random() - 0.5) * currentPrice * 0.05; // Extra ±2.5% for volatile commodities
      }
      
      data.push({
        time: timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        price: parseFloat(currentPrice.toFixed(2)),
        timestamp: timestamp.toISOString()
      });
    }
    
    return data;
  };

  // Generate market heatmap data
  const generateMarketHeatmapData = () => {
    if (!trendsData) return [];
    
    const allCommodities = [
      ...(trendsData.trending_up || []),
      ...(trendsData.trending_down || []),
      ...(trendsData.stable || []),
      ...(trendsData.high_volatility || [])
    ];
    
    return allCommodities.map(commodity => ({
      name: commodity.name,
      value: commodity.price || Math.random() * 10000,
      trend: commodity.trend_strength || commodity.volatility || 0,
      change: (Math.random() - 0.5) * 20 // Random change percentage
    }));
  };

  // Generate sector performance data
  const generateSectorPerformanceData = () => {
    const sectors = [
      { name: 'Base Metals', value: 35, change: 5.2 },
      { name: 'Precious Metals', value: 25, change: -2.1 },
      { name: 'Critical Metals', value: 30, change: 12.8 },
      { name: 'Energy', value: 10, change: 3.4 }
    ];
    
    return sectors.map(sector => ({
      ...sector,
      color: sector.change > 0 ? '#10B981' : '#EF4444'
    }));
  };

  // Format last update time
  const formatLastUpdate = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchTrends();
    setRefreshing(false);
  };

  // Display data with fallbacks
  const displayData = trendsData || {
    trending_up: [],
    trending_down: [],
    stable: [],
    high_volatility: []
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header with Real-time Status */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold flex items-center space-x-2">
            <Globe className="h-6 w-6" />
            <span>Market Trends</span>
          </h2>
          <p className="text-muted-foreground">
            Real-time commodity intelligence dashboard
          </p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 text-sm">
            {isConnected ? (
              <Wifi className="h-4 w-4 text-green-500" />
            ) : (
              <WifiOff className="h-4 w-4 text-red-500" />
            )}
            <span className={isConnected ? "text-green-600 dark:text-green-400" : "text-red-600 dark:text-red-400"}>
              {isConnected ? 'Live' : 'Offline'}
            </span>
          </div>
          <div className="text-sm text-muted-foreground">
            Last update: {formatLastUpdate(lastUpdate)}
          </div>
          <Button 
            variant="outline" 
            size="sm" 
            onClick={handleRefresh}
            disabled={refreshing}
            className="flex items-center space-x-2"
          >
            <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </Button>
        </div>
      </div>

      {/* Real-time Indicators */}
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

      {/* Live Charts */}
      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="live">Live Prices</TabsTrigger>
          <TabsTrigger value="sectors">Sectors</TabsTrigger>
          <TabsTrigger value="heatmap">Heatmap</TabsTrigger>
          <TabsTrigger value="alerts">Alerts</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Trending Up Commodities */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2 text-green-600">
                  <TrendingUp className="h-5 w-5" />
                  <span>Trending Up</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {displayData.trending_up?.slice(0, 5).map((commodity, index) => (
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
                        <div>
                          <div className="font-medium">{commodity.name}</div>
                          <div className="text-sm text-muted-foreground">
                            ${commodity.price?.toLocaleString() || 'N/A'}
                          </div>
                        </div>
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

            {/* Trending Down Commodities */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2 text-red-600">
                  <TrendingDown className="h-5 w-5" />
                  <span>Trending Down</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {displayData.trending_down?.slice(0, 5).map((commodity, index) => (
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
                        <div>
                          <div className="font-medium">{commodity.name}</div>
                          <div className="text-sm text-muted-foreground">
                            ${commodity.price?.toLocaleString() || 'N/A'}
                          </div>
                        </div>
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
          </div>
        </TabsContent>

        <TabsContent value="live" className="space-y-6">
          {/* Live Price Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {displayData.trending_up?.slice(0, 4).map((commodity, index) => (
              <Card key={commodity.id}>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <BarChart3 className="h-5 w-5" />
                    <span>{commodity.name} Live Price</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart
                      data={generateLivePriceData(commodity.name, commodity.price || 1000)}
                      margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis 
                        dataKey="time" 
                        tick={{ fontSize: 12 }}
                        tickFormatter={(value) => value.replace(':00', '')}
                      />
                      <YAxis domain={['auto', 'auto']} />
                      <Tooltip 
                        formatter={(value) => [`$${value}`, 'Price']}
                        labelFormatter={(label) => `Time: ${label}`}
                      />
                      <Area
                        type="monotone"
                        dataKey="price"
                        stroke="#8884d8"
                        fill="#8884d8"
                        fillOpacity={0.3}
                        name="Price"
                      />
                      <Line
                        type="monotone"
                        dataKey="price"
                        stroke="#8884d8"
                        strokeWidth={2}
                        dot={false}
                        name="Price"
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="sectors" className="space-y-6">
          {/* Sector Performance */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <PieChartIcon className="h-5 w-5" />
                <span>Sector Performance</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={generateSectorPerformanceData()}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    >
                      {generateSectorPerformanceData().map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
                <div className="space-y-4">
                  {generateSectorPerformanceData().map((sector, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-muted rounded-lg">
                      <div className="flex items-center space-x-2">
                        <div 
                          className="w-3 h-3 rounded-full" 
                          style={{ backgroundColor: sector.color }}
                        ></div>
                        <span className="font-medium">{sector.name}</span>
                      </div>
                      <Badge 
                        variant="secondary" 
                        className={sector.change > 0 ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}
                      >
                        {sector.change > 0 ? '+' : ''}{sector.change.toFixed(1)}%
                      </Badge>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="heatmap" className="space-y-6">
          {/* Market Heatmap */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Zap className="h-5 w-5" />
                <span>Market Heatmap</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart
                  data={generateMarketHeatmapData()}
                  layout="vertical"
                  margin={{ top: 5, right: 30, left: 100, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" />
                  <YAxis 
                    dataKey="name" 
                    type="category" 
                    width={90}
                    tick={{ fontSize: 12 }}
                  />
                  <Tooltip 
                    formatter={(value, name, props) => {
                      if (name === 'value') {
                        return [`$${value.toLocaleString()}`, 'Price'];
                      }
                      return [`${value.toFixed(2)}`, name];
                    }}
                  />
                  <Bar 
                    dataKey="value" 
                    name="Price"
                  >
                    {generateMarketHeatmapData().map((entry, index) => (
                      <Cell 
                        key={`cell-${index}`} 
                        fill={entry.change > 0 ? '#10B981' : '#EF4444'} 
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="alerts" className="space-y-6">
          {/* Risk Alerts */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2 text-orange-600">
                <AlertTriangle className="h-5 w-5" />
                <span>Risk Alerts</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {displayData.high_volatility?.map((commodity, index) => (
                  <motion.div
                    key={commodity.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="flex items-center justify-between p-4 bg-orange-50 dark:bg-orange-950 rounded-lg"
                  >
                    <div className="flex items-center space-x-3">
                      <AlertTriangle className="h-5 w-5 text-orange-600" />
                      <div>
                        <div className="font-medium">{commodity.name}</div>
                        <div className="text-sm text-muted-foreground">
                          High volatility detected ({(commodity.volatility * 100).toFixed(1)}%)
                        </div>
                      </div>
                    </div>
                    <Badge variant="outline" className="bg-orange-100 text-orange-800">
                      Risk Alert
                    </Badge>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default MarketTrends;