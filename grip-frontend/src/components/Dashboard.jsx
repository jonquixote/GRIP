import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { 
  TrendingUp, 
  TrendingDown, 
  Activity, 
  Globe, 
  BarChart3, 
  AlertTriangle,
  Zap,
  Database,
  Brain,
  Target,
  RefreshCw,
  Download,
  CheckCircle
} from 'lucide-react';
import { motion } from 'framer-motion';
import CommodityOverview from './CommodityOverview';
import AnalyticsPanel from './AnalyticsPanel';
import PredictionsPanel from './PredictionsPanel';
import MarketTrends from './MarketTrends';
import { dataIngestionService } from '../services/api';
import '../App.css';

const Dashboard = () => {
  const [marketOverview, setMarketOverview] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    fetchMarketOverview();
  }, []);

  const fetchMarketOverview = async () => {
    try {
      setLoading(true);
      // Mock data for now since we don't have the actual API endpoint
      const mockData = {
        total_commodities: 42,
        market_summary: {
          positive_outlook: 28,
          high_risk_commodities: 8,
          market_sentiment: 'Bullish'
        },
        risk_alerts: [
          "Copper supply disruption in Chile",
          "Lithium price volatility in Australia",
          "Gold reserves declining in South Africa"
        ]
      };
      setMarketOverview(mockData);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchMarketOverview();
    setRefreshing(false);
  };

  const handleDataIngestion = async (dataType) => {
    try {
      setRefreshing(true);
      const response = await dataIngestionService.ingestFiles({ data_type: dataType });
      console.log('Data ingestion response:', response);
      // Refresh the dashboard after ingestion
      await fetchMarketOverview();
    } catch (err) {
      console.error('Error ingesting data:', err);
      setError(err.message);
    } finally {
      setRefreshing(false);
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.5
      }
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="flex items-center space-x-2">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          <span className="text-lg">Loading GRIP Dashboard...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <motion.header 
        className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm border-b border-slate-200 dark:border-slate-700 sticky top-0 z-50"
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Globe className="h-8 w-8 text-primary" />
                <div>
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">
                    GRIP
                  </h1>
                  <p className="text-sm text-muted-foreground">Global Resource Intelligence Platform</p>
                </div>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="flex items-center space-x-1">
                <Activity className="h-3 w-3" />
                <span className="text-foreground dark:text-foreground">Live Data</span>
              </Badge>
              <Button 
                variant="secondary" 
                size="sm" 
                onClick={handleRefresh}
                disabled={refreshing}
                className="flex items-center space-x-2"
              >
                <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
                <span className="text-foreground dark:text-foreground">Refresh</span>
              </Button>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Data Ingestion Section */}
      <motion.div 
        className="container mx-auto px-6 py-4"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <Card className="bg-gradient-to-br from-indigo-50 to-purple-50 dark:from-indigo-950 dark:to-purple-950 border-indigo-200 dark:border-indigo-800">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2 text-indigo-700 dark:text-indigo-300">
              <Download className="h-5 w-5" />
              <span>Data Ingestion</span>
            </CardTitle>
            <CardDescription>
              Import existing data files into the GRIP system
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col sm:flex-row gap-4">
              <Button 
                onClick={() => handleDataIngestion('all')}
                disabled={refreshing}
                className="flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-700"
              >
                {refreshing ? (
                  <RefreshCw className="h-4 w-4 animate-spin" />
                ) : (
                  <Download className="h-4 w-4" />
                )}
                <span>Ingest All Data</span>
              </Button>
              <Button 
                variant="outline" 
                onClick={() => handleDataIngestion('usgs')}
                disabled={refreshing}
                className="flex items-center space-x-2 border-indigo-300 text-indigo-700 dark:text-indigo-300"
              >
                <Database className="h-4 w-4" />
                <span>USGS Data Only</span>
              </Button>
              <Button 
                variant="outline" 
                onClick={() => handleDataIngestion('fred')}
                disabled={refreshing}
                className="flex items-center space-x-2 border-indigo-300 text-indigo-700 dark:text-indigo-300"
              >
                <BarChart3 className="h-4 w-4" />
                <span>FRED Data Only</span>
              </Button>
            </div>
            {refreshing && (
              <div className="mt-4 text-sm text-indigo-600 dark:text-indigo-400">
                Ingesting data, please wait...
              </div>
            )}
          </CardContent>
        </Card>
      </motion.div>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="space-y-8"
        >
          {/* Key Metrics */}
          <motion.div variants={itemVariants}>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-950 dark:to-blue-900 border-blue-200 dark:border-blue-800">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Commodities</CardTitle>
                  <Database className="h-4 w-4 text-blue-600" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-blue-700 dark:text-blue-300">
                    {marketOverview?.total_commodities || 0}
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
                    {marketOverview?.market_summary?.positive_outlook || 0}
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
                    {marketOverview?.market_summary?.high_risk_commodities || 0}
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
                  <div className="text-2xl font-bold text-purple-700 dark:text-purple-300">
                    {marketOverview?.market_summary?.market_sentiment || 'Mixed'}
                  </div>
                  <p className="text-xs text-purple-600 dark:text-purple-400">
                    Overall market mood
                  </p>
                </CardContent>
              </Card>
            </div>
          </motion.div>

          {/* Risk Alerts */}
          {marketOverview?.risk_alerts && marketOverview.risk_alerts.length > 0 && (
            <motion.div variants={itemVariants}>
              <Card className="border-orange-200 dark:border-orange-800">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2 text-orange-700 dark:text-orange-300">
                    <AlertTriangle className="h-5 w-5" />
                    <span>Risk Alerts</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {marketOverview.risk_alerts.map((alert, index) => (
                      <div key={index} className="flex items-center space-x-2 p-2 bg-orange-50 dark:bg-orange-950 rounded-lg">
                        <AlertTriangle className="h-4 w-4 text-orange-600" />
                        <span className="text-sm">{alert}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}

          {/* Main Dashboard Tabs */}
          <motion.div variants={itemVariants}>
            <Tabs defaultValue="overview" className="space-y-6">
              <TabsList className="grid w-full grid-cols-4 lg:w-[600px]">
                <TabsTrigger value="overview" className="flex items-center space-x-2">
                  <BarChart3 className="h-4 w-4" />
                  <span>Overview</span>
                </TabsTrigger>
                <TabsTrigger value="analytics" className="flex items-center space-x-2">
                  <Activity className="h-4 w-4" />
                  <span>Analytics</span>
                </TabsTrigger>
                <TabsTrigger value="predictions" className="flex items-center space-x-2">
                  <Brain className="h-4 w-4" />
                  <span>Predictions</span>
                </TabsTrigger>
                <TabsTrigger value="trends" className="flex items-center space-x-2">
                  <TrendingUp className="h-4 w-4" />
                  <span>Trends</span>
                </TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="space-y-6">
                <CommodityOverview />
              </TabsContent>

              <TabsContent value="analytics" className="space-y-6">
                <AnalyticsPanel />
              </TabsContent>

              <TabsContent value="predictions" className="space-y-6">
                <PredictionsPanel />
              </TabsContent>

              <TabsContent value="trends" className="space-y-6">
                <MarketTrends />
              </TabsContent>
            </Tabs>
          </motion.div>
        </motion.div>
      </main>
    </div>
  );
};

export default Dashboard;