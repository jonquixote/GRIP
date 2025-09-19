import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { 
  TrendingUp, 
  TrendingDown, 
  Minus,
  Star,
  BarChart3,
  Activity,
  Globe,
  Zap,
  Calendar,
  Database
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import { motion } from 'framer-motion';
import { commodityService, dataIngestionService } from '../services/api';

const CommodityDashboard = () => {
  const [commodities, setCommodities] = useState([]);
  const [selectedCommodity, setSelectedCommodity] = useState(null);
  const [productionData, setProductionData] = useState([]);
  const [priceData, setPriceData] = useState([]);
  const [reservesData, setReservesData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('5Y');

  useEffect(() => {
    fetchCommodities();
  }, []);

  useEffect(() => {
    if (selectedCommodity) {
      fetchCommodityData(selectedCommodity.id);
    }
  }, [selectedCommodity, timeRange]);

  const fetchCommodities = async () => {
    try {
      setLoading(true);
      const response = await commodityService.getAll();
      setCommodities(response.data);
      
      // Auto-select Copper as it has good data
      const copper = response.data.find(c => c.name === 'Copper');
      if (copper) {
        setSelectedCommodity(copper);
      } else if (response.data.length > 0) {
        setSelectedCommodity(response.data[0]);
      }
    } catch (error) {
      console.error('Error fetching commodities:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCommodityData = async (commodityId) => {
    try {
      setLoading(true);
      
      // Fetch production data
      const productionResponse = await dataIngestionService.ingestFiles({
        data_type: 'production',
        commodity_id: commodityId
      });
      
      // Fetch price data
      const priceResponse = await dataIngestionService.ingestFiles({
        data_type: 'price',
        commodity_id: commodityId
      });
      
      // Fetch reserves data
      const reservesResponse = await dataIngestionService.ingestFiles({
        data_type: 'reserves',
        commodity_id: commodityId
      });
      
      // For now, we'll mock the data since our API doesn't have these endpoints yet
      // In a real implementation, we would use:
      // setProductionData(productionResponse.data);
      // setPriceData(priceResponse.data);
      // setReservesData(reservesResponse.data);
      
      // Mock data for demonstration
      const mockProductionData = [
        { year: 2020, production: 2000 },
        { year: 2021, production: 2100 },
        { year: 2022, production: 2200 },
        { year: 2023, production: 2150 },
        { year: 2024, production: 2300 },
        { year: 2025, production: 2400 }
      ];
      
      const mockPriceData = [
        { date: '2025-01-01', price: 9000 },
        { date: '2025-02-01', price: 9200 },
        { date: '2025-03-01', price: 9400 },
        { date: '2025-04-01', price: 9600 },
        { date: '2025-05-01', price: 9800 },
        { date: '2025-06-01', price: 10000 }
      ];
      
      const mockReservesData = [
        { year: 2020, reserves: 800000 },
        { year: 2021, reserves: 820000 },
        { year: 2022, reserves: 840000 },
        { year: 2023, reserves: 850000 },
        { year: 2024, reserves: 860000 },
        { year: 2025, reserves: 870000 }
      ];
      
      setProductionData(mockProductionData);
      setPriceData(mockPriceData);
      setReservesData(mockReservesData);
    } catch (error) {
      console.error('Error fetching commodity data:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateTrend = (data, valueKey) => {
    if (data.length < 2) return 'neutral';
    
    const firstValue = data[0][valueKey];
    const lastValue = data[data.length - 1][valueKey];
    
    if (lastValue > firstValue * 1.05) return 'up';
    if (lastValue < firstValue * 0.95) return 'down';
    return 'neutral';
  };

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'up': return <TrendingUp className="h-4 w-4 text-green-500" />;
      case 'down': return <TrendingDown className="h-4 w-4 text-red-500" />;
      default: return <Minus className="h-4 w-4 text-gray-500" />;
    }
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
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold">Commodity Intelligence Dashboard</h1>
          <p className="text-muted-foreground">Real-time analytics and insights</p>
        </div>
        <div className="flex items-center gap-4">
          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger className="w-[120px]">
              <SelectValue placeholder="Time range" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="1Y">1 Year</SelectItem>
              <SelectItem value="3Y">3 Years</SelectItem>
              <SelectItem value="5Y">5 Years</SelectItem>
              <SelectItem value="10Y">10 Years</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Commodity Selector */}
      <Card>
        <CardHeader>
          <CardTitle>Select Commodity</CardTitle>
          <CardDescription>Choose a commodity to analyze</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {commodities.map((commodity) => (
              <Button
                key={commodity.id}
                variant={selectedCommodity?.id === commodity.id ? "default" : "outline"}
                onClick={() => setSelectedCommodity(commodity)}
                className="flex items-center"
              >
                <BarChart3 className="h-4 w-4 mr-2" />
                {commodity.name}
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>

      {selectedCommodity && (
        <>
          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-950 dark:to-blue-900 border-blue-200 dark:border-blue-800">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Current Price</CardTitle>
                <Activity className="h-4 w-4 text-blue-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-blue-700 dark:text-blue-300">
                  ${priceData.length > 0 ? priceData[priceData.length - 1].price.toLocaleString() : 'N/A'}
                </div>
                <p className="text-xs text-blue-600 dark:text-blue-400">
                  {priceData.length > 1 && getTrendIcon(calculateTrend(priceData, 'price'))}
                  <span className="ml-1">Recent price trend</span>
                </p>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-950 dark:to-green-900 border-green-200 dark:border-green-800">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Annual Production</CardTitle>
                <Database className="h-4 w-4 text-green-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-700 dark:text-green-300">
                  {productionData.length > 0 ? `${productionData[productionData.length - 1].production}k` : 'N/A'} tons
                </div>
                <p className="text-xs text-green-600 dark:text-green-400">
                  {productionData.length > 1 && getTrendIcon(calculateTrend(productionData, 'production'))}
                  <span className="ml-1">Production trend</span>
                </p>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-950 dark:to-purple-900 border-purple-200 dark:border-purple-800">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Known Reserves</CardTitle>
                <Globe className="h-4 w-4 text-purple-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-purple-700 dark:text-purple-300">
                  {reservesData.length > 0 ? `${(reservesData[reservesData.length - 1].reserves / 1000).toFixed(0)}M` : 'N/A'} tons
                </div>
                <p className="text-xs text-purple-600 dark:text-purple-400">
                  {reservesData.length > 1 && getTrendIcon(calculateTrend(reservesData, 'reserves'))}
                  <span className="ml-1">Reserve trend</span>
                </p>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-950 dark:to-orange-900 border-orange-200 dark:border-orange-800">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Strategic Importance</CardTitle>
                <Star className="h-4 w-4 text-orange-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-orange-700 dark:text-orange-300">
                  {selectedCommodity.strategic_importance || 'N/A'}/10
                </div>
                <p className="text-xs text-orange-600 dark:text-orange-400">
                  Criticality score
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Production Chart */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Database className="h-5 w-5 mr-2" />
                  Production Trend
                </CardTitle>
                <CardDescription>Annual production volumes</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={productionData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="year" />
                      <YAxis />
                      <Tooltip />
                      <Line 
                        type="monotone" 
                        dataKey="production" 
                        stroke="#8884d8" 
                        strokeWidth={2}
                        dot={{ fill: '#8884d8' }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            {/* Price Chart */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <TrendingUp className="h-5 w-5 mr-2" />
                  Price History
                </CardTitle>
                <CardDescription>Monthly price movements</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={priceData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <Tooltip />
                      <Line 
                        type="monotone" 
                        dataKey="price" 
                        stroke="#82ca9d" 
                        strokeWidth={2}
                        dot={{ fill: '#82ca9d' }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            {/* Reserves Chart */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Globe className="h-5 w-5 mr-2" />
                  Reserves Trend
                </CardTitle>
                <CardDescription>Known reserves over time</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={reservesData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="year" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="reserves" fill="#ffc658" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            {/* Production Distribution */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Zap className="h-5 w-5 mr-2" />
                  Production Distribution
                </CardTitle>
                <CardDescription>Top producing regions</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={[
                          { name: 'Chile', value: 30 },
                          { name: 'Peru', value: 20 },
                          { name: 'China', value: 15 },
                          { name: 'DRC', value: 10 },
                          { name: 'Other', value: 25 }
                        ]}
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      >
                        <Cell fill="#0088FE" />
                        <Cell fill="#00C49F" />
                        <Cell fill="#FFBB28" />
                        <Cell fill="#FF8042" />
                        <Cell fill="#8884D8" />
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Detailed Data Tables */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Production Data */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Database className="h-5 w-5 mr-2" />
                  Production Data
                </CardTitle>
                <CardDescription>Recent production volumes</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-64 overflow-y-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b">
                        <th className="text-left py-2">Year</th>
                        <th className="text-left py-2">Volume</th>
                        <th className="text-left py-2">Unit</th>
                      </tr>
                    </thead>
                    <tbody>
                      {productionData.slice(-10).map((data, index) => (
                        <tr key={index} className="border-b">
                          <td className="py-2">{data.year}</td>
                          <td className="py-2">{data.production?.toLocaleString()}</td>
                          <td className="py-2">metric tons</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>

            {/* Price Data */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <TrendingUp className="h-5 w-5 mr-2" />
                  Price Data
                </CardTitle>
                <CardDescription>Recent price movements</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-64 overflow-y-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b">
                        <th className="text-left py-2">Date</th>
                        <th className="text-left py-2">Price</th>
                        <th className="text-left py-2">Currency</th>
                      </tr>
                    </thead>
                    <tbody>
                      {priceData.slice(-10).map((data, index) => (
                        <tr key={index} className="border-b">
                          <td className="py-2">{new Date(data.date).toLocaleDateString()}</td>
                          <td className="py-2">${data.price?.toLocaleString()}</td>
                          <td className="py-2">USD</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>

            {/* Reserves Data */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Globe className="h-5 w-5 mr-2" />
                  Reserves Data
                </CardTitle>
                <CardDescription>Known reserves volumes</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-64 overflow-y-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b">
                        <th className="text-left py-2">Year</th>
                        <th className="text-left py-2">Volume</th>
                        <th className="text-left py-2">Unit</th>
                      </tr>
                    </thead>
                    <tbody>
                      {reservesData.slice(-10).map((data, index) => (
                        <tr key={index} className="border-b">
                          <td className="py-2">{data.year}</td>
                          <td className="py-2">{data.reserves?.toLocaleString()}</td>
                          <td className="py-2">metric tons</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>
          </div>
        </>
      )}
    </div>
  );
};

export default CommodityDashboard;