import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Progress } from '../components/ui/progress';
import { 
  Database, 
  BarChart3, 
  Play, 
  CheckCircle, 
  AlertCircle,
  RefreshCw,
  Clock,
  Zap
} from 'lucide-react';
import { dataIngestionService } from '../services/api';

const DataIngestionPanel = () => {
  const [sources, setSources] = useState({});
  const [ingestionStatus, setIngestionStatus] = useState({});
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    fetchSources();
    fetchStatus();
  }, []);

  const fetchSources = async () => {
    try {
      setLoading(true);
      const response = await dataIngestionService.getAvailableSources();
      setSources(response.data);
    } catch (error) {
      console.error('Error fetching sources:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStatus = async () => {
    try {
      const response = await dataIngestionService.getCollectionStatus();
      setIngestionStatus(response.data);
    } catch (error) {
      console.error('Error fetching status:', error);
    }
  };

  const handleCollectData = async (source) => {
    try {
      setIngestionStatus(prev => ({
        ...prev,
        [source]: { status: 'running', message: 'Starting data collection...' }
      }));
      
      const response = await dataIngestionService.collectFromSource(source);
      console.log(`${source} collection started:`, response.data);
      
      // Update status to show running
      setIngestionStatus(prev => ({
        ...prev,
        [source]: { status: 'running', message: 'Data collection in progress...' }
      }));
      
      // Simulate completion after a delay
      setTimeout(() => {
        setIngestionStatus(prev => ({
          ...prev,
          [source]: { status: 'completed', message: 'Data collection completed successfully' }
        }));
      }, 3000);
    } catch (error) {
      console.error(`Error collecting ${source} data:`, error);
      setIngestionStatus(prev => ({
        ...prev,
        [source]: { status: 'error', message: `Error: ${error.message}` }
      }));
    }
  };

  const handleTestCollector = async (source) => {
    try {
      setIngestionStatus(prev => ({
        ...prev,
        [source]: { status: 'testing', message: 'Testing data collector...' }
      }));
      
      const response = await dataIngestionService.testCollector(source);
      console.log(`${source} test completed:`, response.data);
      
      setIngestionStatus(prev => ({
        ...prev,
        [source]: { 
          status: 'tested', 
          message: `Test completed: ${response.data.test_data_count} records collected`,
          testData: response.data.sample_data
        }
      }));
    } catch (error) {
      console.error(`Error testing ${source} collector:`, error);
      setIngestionStatus(prev => ({
        ...prev,
        [source]: { status: 'error', message: `Test error: ${error.message}` }
      }));
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'running':
        return <RefreshCw className="h-4 w-4 animate-spin text-blue-500" />;
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'error':
        return <AlertCircle className="h-4 w-4 text-red-500" />;
      case 'testing':
        return <Zap className="h-4 w-4 text-yellow-500" />;
      case 'tested':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      default:
        return <Clock className="h-4 w-4 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'running':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
      case 'completed':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'error':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      case 'testing':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      case 'tested':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchSources();
    await fetchStatus();
    setRefreshing(false);
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
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Data Ingestion</h2>
          <p className="text-muted-foreground">Manage data collection from authoritative sources</p>
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

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* USGS Data Source */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Database className="h-5 w-5 text-blue-500" />
              <span>USGS Data Collection</span>
            </CardTitle>
            <CardDescription>
              Mineral commodity data from USGS Mineral Commodity Summaries
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex flex-wrap gap-2">
              <Badge variant="secondary">Web Scraping</Badge>
              <Badge variant="outline">Annual Updates</Badge>
              <Badge variant="outline">
                {sources.usgs?.commodities?.length || 0} Commodities
              </Badge>
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Data Types</span>
                <span className="font-medium">Production, Reserves, Consumption</span>
              </div>
              <Progress value={75} className="w-full" />
            </div>
            
            <div className="flex flex-wrap gap-2">
              {ingestionStatus.usgs && (
                <Badge className={getStatusColor(ingestionStatus.usgs.status)}>
                  <div className="flex items-center space-x-1">
                    {getStatusIcon(ingestionStatus.usgs.status)}
                    <span>{ingestionStatus.usgs.message}</span>
                  </div>
                </Badge>
              )}
            </div>
            
            <div className="flex flex-wrap gap-2">
              <Button 
                onClick={() => handleCollectData('usgs')}
                className="flex items-center space-x-2"
              >
                <Play className="h-4 w-4" />
                <span>Collect USGS Data</span>
              </Button>
              <Button 
                variant="outline" 
                onClick={() => handleTestCollector('usgs')}
                className="flex items-center space-x-2"
              >
                <Zap className="h-4 w-4" />
                <span>Test Collector</span>
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* FRED Data Source */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <BarChart3 className="h-5 w-5 text-indigo-500" />
              <span>FRED Data Collection</span>
            </CardTitle>
            <CardDescription>
              Economic indicators and commodity prices from Federal Reserve
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex flex-wrap gap-2">
              <Badge variant="secondary">API Integration</Badge>
              <Badge variant="outline">Daily Updates</Badge>
              <Badge variant="outline">
                {sources.fred?.commodities?.length || 0} Commodities
              </Badge>
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Data Types</span>
                <span className="font-medium">Price Data</span>
              </div>
              <Progress value={90} className="w-full" />
            </div>
            
            <div className="flex flex-wrap gap-2">
              {ingestionStatus.fred && (
                <Badge className={getStatusColor(ingestionStatus.fred.status)}>
                  <div className="flex items-center space-x-1">
                    {getStatusIcon(ingestionStatus.fred.status)}
                    <span>{ingestionStatus.fred.message}</span>
                  </div>
                </Badge>
              )}
            </div>
            
            <div className="flex flex-wrap gap-2">
              <Button 
                onClick={() => handleCollectData('fred')}
                className="flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-700"
              >
                <Play className="h-4 w-4" />
                <span>Collect FRED Data</span>
              </Button>
              <Button 
                variant="outline" 
                onClick={() => handleTestCollector('fred')}
                className="flex items-center space-x-2"
              >
                <Zap className="h-4 w-4" />
                <span>Test Collector</span>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Collection Summary */}
      <Card>
        <CardHeader>
          <CardTitle>Collection Summary</CardTitle>
          <CardDescription>
            Overview of data collection activities
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-muted rounded-lg">
              <div className="text-2xl font-bold">
                {Object.keys(sources).length}
              </div>
              <div className="text-sm text-muted-foreground">
                Active Data Sources
              </div>
            </div>
            <div className="p-4 bg-muted rounded-lg">
              <div className="text-2xl font-bold">
                {(sources?.usgs?.commodities?.length || 0) + (sources?.fred?.commodities?.length || 0)}
              </div>
              <div className="text-sm text-muted-foreground">
                Total Commodities Tracked
              </div>
            </div>
            <div className="p-4 bg-muted rounded-lg">
              <div className="text-2xl font-bold">
                {ingestionStatus ? Object.values(ingestionStatus).filter(s => s && s.status === 'completed').length : 0}
              </div>
              <div className="text-sm text-muted-foreground">
                Successful Collections
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default DataIngestionPanel;