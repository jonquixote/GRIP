import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { 
  TrendingUp, 
  TrendingDown, 
  Activity, 
  BarChart3, 
  AlertTriangle,
  Zap,
  Database,
  Brain,
  Target,
  RefreshCw,
  Globe,
  MapPin,
  Calendar
} from 'lucide-react';
import { motion } from 'framer-motion';
import { analyticsService, commodityService } from '../services/api';

const AnalyticsDashboard = () => {
  const [commodities, setCommodities] = useState([]);
  const [selectedCommodity, setSelectedCommodity] = useState(null);
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [timeRange, setTimeRange] = useState('1Y');

  useEffect(() => {
    fetchCommodities();
  }, []);

  useEffect(() => {
    if (selectedCommodity) {
      fetchAnalyticsData();
    }
  }, [selectedCommodity, timeRange]);

  const fetchCommodities = async () => {
    try {
      setLoading(true);
      const response = await commodityService.getAll();
      setCommodities(response.data);
      if (response.data.length > 0) {
        setSelectedCommodity(response.data[0]);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchAnalyticsData = async () => {
    try {
      setLoading(true);
      const response = await analyticsService.getCommodityOverview({
        commodity_id: selectedCommodity.id
      });
      setAnalyticsData(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    if (selectedCommodity) {
      await fetchAnalyticsData();
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
          <h1 className="text-3xl font-bold">Analytics Dashboard</h1>
          <p className="text-muted-foreground">Comprehensive resource intelligence analytics</p>
        </div>
        <div className="flex items-center gap-4">
          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger className="w-[120px]">
              <SelectValue placeholder="Time range" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="1M">1 Month</SelectItem>
              <SelectItem value="3M">3 Months</SelectItem>
              <SelectItem value="6M">6 Months</SelectItem>
              <SelectItem value="1Y">1 Year</SelectItem>
              <SelectItem value="5Y">5 Years</SelectItem>
            </SelectContent>
          </Select>
          <Button onClick={handleRefresh} variant="outline" size="sm">
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
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

      {selectedCommodity && analyticsData && (
        <>
          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-950 dark:to-blue-900 border-blue-200 dark:border-blue-800">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Production Trend</CardTitle>
                <Activity className="h-4 w-4 text-blue-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-blue-700 dark:text-blue-300">
                  {analyticsData.analytics?.production_trend || 'N/A'}
                </div>
                <p className="text-xs text-blue-600 dark:text-blue-400">
                  Recent production changes
                </p>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-950 dark:to-green-900 border-green-200 dark:border-green-800">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Reserves Trend</CardTitle>
                <Database className="h-4 w-4 text-green-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-700 dark:text-green-300">
                  {analyticsData.analytics?.reserves_trend || 'N/A'}
                </div>
                <p className="text-xs text-green-600 dark:text-green-400">
                  Reserve availability changes
                </p>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-950 dark:to-purple-900 border-purple-200 dark:border-purple-800">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Price Trend</CardTitle>
                <TrendingUp className="h-4 w-4 text-purple-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-purple-700 dark:text-purple-300">
                  {analyticsData.analytics?.price_trend || 'N/A'}
                </div>
                <p className="text-xs text-purple-600 dark:text-purple-400">
                  Market price movements
                </p>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-950 dark:to-orange-900 border-orange-200 dark:border-orange-800">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Top Producer</CardTitle>
                <Globe className="h-4 w-4 text-orange-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-orange-700 dark:text-orange-300">
                  {analyticsData.analytics?.top_producers?.[0]?.country || 'N/A'}
                </div>
                <p className="text-xs text-orange-600 dark:text-orange-400">
                  Leading production country
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Production and Reserves Data */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Activity className="h-5 w-5 mr-2" />
                  Production Data
                </CardTitle>
                <CardDescription>Historical production volumes</CardDescription>
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
                      {analyticsData.production_data?.slice(0, 10).map((data, index) => (
                        <tr key={index} className="border-b">
                          <td className="py-2">{data.year}</td>
                          <td className="py-2">{data.production_volume?.toLocaleString()}</td>
                          <td className="py-2">{data.unit}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Database className="h-5 w-5 mr-2" />
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
                      {analyticsData.reserves_data?.slice(0, 10).map((data, index) => (
                        <tr key={index} className="border-b">
                          <td className="py-2">{data.year}</td>
                          <td className="py-2">{data.reserves_volume?.toLocaleString()}</td>
                          <td className="py-2">{data.unit}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Price Data */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <TrendingUp className="h-5 w-5 mr-2" />
                Price History
              </CardTitle>
              <CardDescription>Commodity price movements over time</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-64 overflow-y-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b">
                      <th className="text-left py-2">Date</th>
                      <th className="text-left py-2">Price</th>
                      <th className="text-left py-2">Currency</th>
                      <th className="text-left py-2">Volume</th>
                    </tr>
                  </thead>
                  <tbody>
                    {analyticsData.price_data?.slice(0, 15).map((data, index) => (
                      <tr key={index} className="border-b">
                        <td className="py-2">{new Date(data.timestamp).toLocaleDateString()}</td>
                        <td className="py-2">${data.price?.toLocaleString()}</td>
                        <td className="py-2">{data.currency}</td>
                        <td className="py-2">{data.volume?.toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </>
      )}

      {error && (
        <Card>
          <CardContent className="py-6 text-center">
            <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">Error Loading Data</h3>
            <p className="text-muted-foreground mb-4">{error}</p>
            <Button onClick={fetchCommodities}>Retry</Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default AnalyticsDashboard;