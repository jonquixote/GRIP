import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Input } from '../components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Search, Star, TrendingUp, TrendingDown, Minus, BarChart3 } from 'lucide-react';
import { motion } from 'framer-motion';
import { commodityService } from '../services/api';
import { mockDataService } from '../services/mockData';

const CommodityList = () => {
  const [commodities, setCommodities] = useState([]);
  const [filteredCommodities, setFilteredCommodities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCommodity, setSelectedCommodity] = useState(null);
  const [commodityDetails, setCommodityDetails] = useState(null);

  useEffect(() => {
    fetchCommodities();
  }, []);

  useEffect(() => {
    filterCommodities();
  }, [commodities, searchTerm]);

  const fetchCommodities = async () => {
    try {
      setLoading(true);
      const response = await commodityService.getAll();
      setCommodities(response.data);
    } catch (error) {
      console.error('Error fetching commodities:', error);
      // Fallback to mock data
      try {
        const mockResponse = await mockDataService.getCommodities();
        setCommodities(mockResponse.data);
      } catch (mockError) {
        console.error('Error fetching mock commodities:', mockError);
      }
    } finally {
      setLoading(false);
    }
  };

  const fetchCommodityDetails = async (commodityId) => {
    try {
      const response = await commodityService.getDetails(commodityId);
      setCommodityDetails(response.data);
    } catch (error) {
      console.error('Error fetching commodity details:', error);
    }
  };

  const filterCommodities = () => {
    let filtered = commodities;

    if (searchTerm) {
      filtered = filtered.filter(commodity =>
        commodity.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        commodity.symbol.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFilteredCommodities(filtered);
  };

  const getTrendIcon = (trend) => {
    if (trend === 'up') return <TrendingUp className="h-4 w-4 text-green-500" />;
    if (trend === 'down') return <TrendingDown className="h-4 w-4 text-red-500" />;
    return <Minus className="h-4 w-4 text-gray-500" />;
  };

  const handleViewDetails = async (commodity) => {
    setSelectedCommodity(commodity);
    await fetchCommodityDetails(commodity.id);
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
      {/* Header with Search */}
      <Card>
        <CardHeader>
          <CardTitle>Commodity Database</CardTitle>
          <CardDescription>
            Browse and analyze global commodity data
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="relative">
            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search commodities..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </CardContent>
      </Card>

      {/* Commodities Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredCommodities.map((commodity, index) => (
          <motion.div
            key={commodity.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <Card className="hover:shadow-lg transition-all duration-300 hover:scale-105">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div className="w-10 h-10 bg-gradient-to-br from-primary to-blue-600 rounded-lg flex items-center justify-center text-white font-bold">
                      {commodity.symbol?.substring(0, 3) || 'N/A'}
                    </div>
                    <div>
                      <CardTitle className="text-lg">{commodity.name}</CardTitle>
                      <CardDescription>{commodity.symbol}</CardDescription>
                    </div>
                  </div>
                  <div className="flex items-center space-x-1">
                    {/* Mock strategic importance rating */}
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        className={`h-3 w-3 ${i < 3 ? 'text-yellow-400 fill-current' : 'text-gray-300'}`}
                      />
                    ))}
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex flex-wrap gap-2">
                  <Badge variant="secondary">
                    Criticality: {Math.floor(Math.random() * 10) + 1}/10
                  </Badge>
                  <Badge variant="outline">
                    <div className="flex items-center space-x-1">
                      {getTrendIcon(['up', 'down', 'neutral'][Math.floor(Math.random() * 3)])}
                      <span>Trend</span>
                    </div>
                  </Badge>
                </div>

                <div className="flex items-center justify-between pt-2">
                  <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                    <span>{Math.floor(Math.random() * 100) + 1} Countries</span>
                    <span>•</span>
                    <span>{Math.floor(Math.random() * 50) + 10} Years</span>
                  </div>
                  <Button
                    size="sm"
                    onClick={() => handleViewDetails(commodity)}
                    className="flex items-center space-x-1"
                  >
                    <BarChart3 className="h-3 w-3" />
                    <span>Details</span>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {filteredCommodities.length === 0 && (
        <Card>
          <CardContent className="py-12 text-center">
            <Search className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">No commodities found</h3>
            <p className="text-muted-foreground">
              Try adjusting your search terms
            </p>
          </CardContent>
        </Card>
      )}

      {/* Analysis Modal */}
      {selectedCommodity && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50"
          onClick={() => {
            setSelectedCommodity(null);
            setCommodityDetails(null);
          }}
        >
          <Card 
            className="max-w-4xl w-full max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-2xl">
                    {selectedCommodity.name} Analysis
                  </CardTitle>
                  <CardDescription>
                    Detailed commodity intelligence
                  </CardDescription>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    setSelectedCommodity(null);
                    setCommodityDetails(null);
                  }}
                >
                  Close
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {/* Key Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="p-4 bg-blue-50 dark:bg-blue-950 rounded-lg">
                    <div className="text-2xl font-bold text-blue-700 dark:text-blue-300">
                      ${commodityDetails?.summary?.average_price ? commodityDetails.summary.average_price.toLocaleString() : 'N/A'}
                    </div>
                    <div className="text-sm text-blue-600 dark:text-blue-400">
                      Avg Price (USD/ton)
                    </div>
                  </div>
                  <div className="p-4 bg-green-50 dark:bg-green-950 rounded-lg">
                    <div className="text-2xl font-bold text-green-700 dark:text-green-300">
                      {commodityDetails?.summary?.total_production ? (commodityDetails.summary.total_production / 1000000).toFixed(2) : 'N/A'}M
                    </div>
                    <div className="text-sm text-green-600 dark:text-green-400">
                      Total Production (tons)
                    </div>
                  </div>
                  <div className="p-4 bg-purple-50 dark:bg-purple-950 rounded-lg">
                    <div className="text-2xl font-bold text-purple-700 dark:text-purple-300">
                      {commodityDetails?.summary?.latest_reserves ? (commodityDetails.summary.latest_reserves / 1000000).toFixed(2) : 'N/A'}M
                    </div>
                    <div className="text-sm text-purple-600 dark:text-purple-400">
                      Known Reserves (tons)
                    </div>
                  </div>
                </div>

                {/* Data Sections */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Production Data */}
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center space-x-2">
                        <Database className="h-5 w-5" />
                        <span>Production Data</span>
                      </CardTitle>
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
                            {commodityDetails?.production_data?.slice(0, 10).map((data, index) => (
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

                  {/* Price Data */}
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center space-x-2">
                        <Zap className="h-5 w-5" />
                        <span>Price Data</span>
                      </CardTitle>
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
                            {commodityDetails?.price_data?.slice(0, 10).map((data, index) => (
                              <tr key={index} className="border-b">
                                <td className="py-2">{new Date(data.timestamp).toLocaleDateString()}</td>
                                <td className="py-2">${data.price?.toLocaleString()}</td>
                                <td className="py-2">{data.currency}</td>
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
                      <CardTitle className="flex items-center space-x-2">
                        <Globe className="h-5 w-5" />
                        <span>Reserves Data</span>
                      </CardTitle>
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
                            {commodityDetails?.reserves_data?.slice(0, 10).map((data, index) => (
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

                  {/* Key Insights */}
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center space-x-2">
                        <BarChart3 className="h-5 w-5" />
                        <span>Key Insights</span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        <div className="p-3 bg-muted rounded-lg">
                          <h4 className="font-medium">Production Trend</h4>
                          <p className="text-sm text-muted-foreground mt-1">
                            {commodityDetails?.production_data?.length > 1 ? 
                              "Stable growth over the past decade" : 
                              "Insufficient data for trend analysis"}
                          </p>
                        </div>
                        <div className="p-3 bg-muted rounded-lg">
                          <h4 className="font-medium">Price Volatility</h4>
                          <p className="text-sm text-muted-foreground mt-1">
                            {commodityDetails?.price_data?.length > 1 ? 
                              "Moderate volatility with seasonal patterns" : 
                              "Insufficient data for volatility analysis"}
                          </p>
                        </div>
                        <div className="p-3 bg-muted rounded-lg">
                          <h4 className="font-medium">Reserve Status</h4>
                          <p className="text-sm text-muted-foreground mt-1">
                            {commodityDetails?.reserves_data?.length > 1 ? 
                              "Adequate reserves to meet current demand levels" : 
                              "Reserve data limited"}
                          </p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>

                {/* Action Buttons */}
                <div className="flex flex-wrap gap-4">
                  <Button variant="outline">
                    Export Data
                  </Button>
                  <Button variant="outline">
                    Compare with Peers
                  </Button>
                  <Button>
                    Add to Watchlist
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}
    </div>
  );
};

export default CommodityList;