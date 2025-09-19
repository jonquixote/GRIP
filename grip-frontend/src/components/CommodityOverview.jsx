import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Input } from '../components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { 
  Search, 
  TrendingUp, 
  TrendingDown, 
  Minus,
  Star,
  AlertCircle,
  BarChart3,
  Activity,
  Globe,
  Zap
} from 'lucide-react';
import { motion } from 'framer-motion';
import { commodityService } from '../services/api';
import { mockDataService } from '../services/mockData';
import CommoditySearch from './CommoditySearch';

const CommodityOverview = () => {
  const [commodities, setCommodities] = useState([]);
  const [filteredCommodities, setFilteredCommodities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [selectedCommodity, setSelectedCommodity] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchCommodities();
  }, []);

  useEffect(() => {
    filterCommodities();
  }, [commodities, categoryFilter, searchTerm]);

  const fetchCommodities = async () => {
    try {
      setLoading(true);
      const response = await commodityService.getAll();
      // Add mock strategic importance and categories for now
      const commoditiesWithDetails = response.data.map(commodity => ({
        ...commodity,
        strategic_importance: Math.floor(Math.random() * 10) + 1,
        category: ['base metal', 'precious metal', 'critical metal', 'energy'][Math.floor(Math.random() * 4)]
      }));
      setCommodities(commoditiesWithDetails);
    } catch (error) {
      console.error('Error fetching commodities:', error);
      // Fallback to mock data
      try {
        const mockResponse = await mockDataService.getCommodities();
        const commoditiesWithDetails = mockResponse.data.map(commodity => ({
          ...commodity,
          strategic_importance: Math.floor(Math.random() * 10) + 1,
          category: ['base metal', 'precious metal', 'critical metal', 'energy'][Math.floor(Math.random() * 4)]
        }));
        setCommodities(commoditiesWithDetails);
      } catch (mockError) {
        console.error('Error fetching mock commodities:', mockError);
      }
    } finally {
      setLoading(false);
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

    if (categoryFilter !== 'all') {
      filtered = filtered.filter(commodity =>
        commodity.category && commodity.category.toLowerCase() === categoryFilter.toLowerCase()
      );
    }

    setFilteredCommodities(filtered);
  };

  const getStrategicImportanceColor = (importance) => {
    if (!importance) return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
    if (importance >= 9) return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
    if (importance >= 7) return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200';
    if (importance >= 5) return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
    return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
  };

  const getCategoryColor = (category) => {
    const colors = {
      'base metal': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
      'precious metal': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
      'critical metal': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
      'energy': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
    };
    return colors[category?.toLowerCase()] || 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
  };

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleCommoditySelect = (commodity) => {
    setSelectedCommodity({
      commodity
    });
    // Also set the search term to the selected commodity name
    setSearchTerm(commodity.name);
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
      {/* Search and Filter Controls */}
      <Card>
        <CardHeader>
          <CardTitle>Commodity Explorer</CardTitle>
          <CardDescription>
            Search and filter through global commodity data
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <CommoditySearch 
                onCommoditySelect={handleCommoditySelect} 
                onSearchChange={handleSearchChange}
                searchValue={searchTerm}
              />
            </div>
            <div className="w-full sm:w-[200px]">
              <Input
                placeholder="Or type to search..."
                value={searchTerm}
                onChange={handleSearchChange}
              />
            </div>
            <Select value={categoryFilter} onValueChange={setCategoryFilter}>
              <SelectTrigger className="w-full sm:w-[200px]">
                <SelectValue placeholder="Filter by category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories</SelectItem>
                <SelectItem value="base metal">Base Metal</SelectItem>
                <SelectItem value="precious metal">Precious Metal</SelectItem>
                <SelectItem value="critical metal">Critical Metal</SelectItem>
                <SelectItem value="energy">Energy</SelectItem>
              </SelectContent>
            </Select>
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
                    {Array.from({ length: 5 }, (_, i) => (
                      <Star
                        key={i}
                        className={`h-3 w-3 ${
                          commodity.strategic_importance && i < Math.floor(commodity.strategic_importance / 2)
                            ? 'text-yellow-400 fill-current'
                            : 'text-gray-300'
                        }`}
                      />
                    ))}
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex flex-wrap gap-2">
                  {commodity.category && (
                    <Badge className={getCategoryColor(commodity.category)}>
                      {commodity.category}
                    </Badge>
                  )}
                  <Badge className={getStrategicImportanceColor(commodity.strategic_importance)}>
                    Importance: {commodity.strategic_importance || 'N/A'}/10
                  </Badge>
                </div>

                <div className="flex items-center justify-between pt-2">
                  <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                    <div className="flex items-center space-x-1">
                      <TrendingUp className="h-4 w-4 text-green-500" />
                      <span>Trend</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Activity className="h-4 w-4 text-blue-500" />
                      <span>Active</span>
                    </div>
                  </div>
                  <Button
                    size="sm"
                    onClick={() => handleAnalyzeCommodity(commodity.id)}
                    className="flex items-center space-x-1"
                  >
                    <BarChart3 className="h-3 w-3" />
                    <span>Analyze</span>
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
            <AlertCircle className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">No commodities found</h3>
            <p className="text-muted-foreground">
              Try adjusting your search terms or filters
            </p>
          </CardContent>
        </Card>
      )}

      {/* Analysis Results Modal/Panel */}
      {selectedCommodity && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50"
          onClick={() => setSelectedCommodity(null)}
        >
          <Card 
            className="max-w-4xl w-full max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-2xl">
                    {selectedCommodity.commodity?.name} Analysis
                  </CardTitle>
                  <CardDescription>
                    Comprehensive analysis results
                  </CardDescription>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setSelectedCommodity(null)}
                >
                  Close
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <p>Analysis data would be displayed here.</p>
                <p>Commodity ID: {selectedCommodity.commodity?.id}</p>
                <p>Commodity Name: {selectedCommodity.commodity?.name}</p>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}
    </div>
  );
};

export default CommodityOverview;