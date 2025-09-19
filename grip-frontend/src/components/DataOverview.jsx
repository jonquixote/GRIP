import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { 
  Database, 
  TrendingUp, 
  AlertTriangle, 
  Brain,
  RefreshCw
} from 'lucide-react';
import { commodityService, analyticsService } from '../services/api';

const DataOverview = () => {
  const [dataStats, setDataStats] = useState({
    total_commodities: 0,
    positive_outlook: 0,
    high_risk_commodities: 0,
    market_sentiment: 'Neutral'
  });
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    fetchDataStats();
  }, []);

  const fetchDataStats = async () => {
    try {
      setLoading(true);
      // Try to fetch real data
      try {
        const response = await analyticsService.getMarketDashboard();
        
        // Transform the response data
        const stats = {
          total_commodities: response.data.total_commodities || response.data.commodities_count || 0,
          positive_outlook: response.data.positive_outlook || response.data.trending_up || 0,
          high_risk_commodities: response.data.high_risk_commodities || response.data.high_risk || 0,
          market_sentiment: response.data.market_sentiment || response.data.sentiment || 'Neutral'
        };
        
        setDataStats(stats);
      } catch (apiError) {
        // Fallback to fetching commodities count
        const commoditiesResponse = await commodityService.getAll();
        setDataStats(prev => ({
          ...prev,
          total_commodities: commoditiesResponse.data.length
        }));
      }
    } catch (error) {
      console.error('Error fetching data stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchDataStats();
    setRefreshing(false);
  };

  const getSentimentColor = (sentiment) => {
    switch (sentiment.toLowerCase()) {
      case 'bullish': return 'text-green-600';
      case 'bearish': return 'text-red-600';
      default: return 'text-purple-600';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Data Overview</h2>
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

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-950 dark:to-blue-900 border-blue-200 dark:border-blue-800">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Commodities</CardTitle>
            <Database className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-700 dark:text-blue-300">
              {dataStats.total_commodities}
            </div>
            <p className="text-xs text-blue-600 dark:text-blue-400">
              Tracked globally
            </p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-950 dark:to-green-900 border-green-200 dark:border-green-800">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Positive Outlook</CardTitle>
            <TrendingUp className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-700 dark:text-green-300">
              {dataStats.positive_outlook}
            </div>
            <p className="text-xs text-green-600 dark:text-green-400">
              Commodities trending up
            </p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-red-50 to-red-100 dark:from-red-950 dark:to-red-900 border-red-200 dark:border-red-800">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">High Risk</CardTitle>
            <AlertTriangle className="h-4 w-4 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-700 dark:text-red-300">
              {dataStats.high_risk_commodities}
            </div>
            <p className="text-xs text-red-600 dark:text-red-400">
              Require attention
            </p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-950 dark:to-purple-900 border-purple-200 dark:border-purple-800">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Market Sentiment</CardTitle>
            <Brain className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className={`text-2xl font-bold ${getSentimentColor(dataStats.market_sentiment)} dark:${getSentimentColor(dataStats.market_sentiment)}`}>
              {dataStats.market_sentiment}
            </div>
            <p className="text-xs text-purple-600 dark:text-purple-400">
              Overall market mood
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default DataOverview;