import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Input } from '../components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Switch } from '../components/ui/switch';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { 
  LineChart, 
  Line, 
  AreaChart, 
  Area, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { 
  TrendingUp, 
  TrendingDown, 
  Activity, 
  BarChart3, 
  PieChart as PieChartIcon,
  Target,
  AlertTriangle,
  CheckCircle,
  Settings,
  Zap,
  Database,
  Globe
} from 'lucide-react';
import { motion } from 'framer-motion';
import { commodityService } from '../services/api';
import AnalyticsDashboard from './AnalyticsDashboard';
import CommodityDashboard from './CommodityDashboard';
import CommoditySelect from './CommoditySelect';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

const AnalyticsPanel = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [commodities, setCommodities] = useState([]);
  const [selectedCommodity, setSelectedCommodity] = useState(null);
  const [timeRange, setTimeRange] = useState('1Y');
  const [analysisMode, setAnalysisMode] = useState('comprehensive');
  
  // Configuration states
  const [config, setConfig] = useState({
    dataSources: ['usgs', 'fred'],
    analysisDepth: 'detailed',
    forecastingModels: ['ml_ensemble', 'econometric'],
    riskFactors: ['political', 'environmental', 'economic'],
    visualizationType: 'interactive',
    autoRefresh: false,
    refreshInterval: 300
  });

  useEffect(() => {
    fetchCommodities();
  }, []);

  const fetchCommodities = async () => {
    try {
      const response = await commodityService.getAll();
      setCommodities(response.data);
      if (response.data.length > 0) {
        setSelectedCommodity(response.data[0]);
      }
    } catch (error) {
      console.error('Error fetching commodities:', error);
    }
  };

  const generateMockChartData = (type) => {
    const data = [];
    for (let i = 0; i < 12; i++) {
      data.push({
        month: new Date(2023, i).toLocaleString('default', { month: 'short' }),
        value: Math.floor(Math.random() * 1000) + 500,
        volume: Math.floor(Math.random() * 100000) + 50000,
        volatility: Math.random() * 10
      });
    }
    return data;
  };

  const handleConfigChange = (key, value) => {
    setConfig(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleDataSourceToggle = (source) => {
    const newSources = config.dataSources.includes(source)
      ? config.dataSources.filter(s => s !== source)
      : [...config.dataSources, source];
    handleConfigChange('dataSources', newSources);
  };

  const handleForecastingModelToggle = (model) => {
    const newModels = config.forecastingModels.includes(model)
      ? config.forecastingModels.filter(m => m !== model)
      : [...config.forecastingModels, model];
    handleConfigChange('forecastingModels', newModels);
  };

  const handleRiskFactorToggle = (factor) => {
    const newFactors = config.riskFactors.includes(factor)
      ? config.riskFactors.filter(f => f !== factor)
      : [...config.riskFactors, factor];
    handleConfigChange('riskFactors', newFactors);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold">Analytics Dashboard</h2>
          <p className="text-muted-foreground">Advanced resource intelligence analytics</p>
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
              <SelectItem value="3Y">3 Years</SelectItem>
              <SelectItem value="5Y">5 Years</SelectItem>
            </SelectContent>
          </Select>
          <Select value={analysisMode} onValueChange={setAnalysisMode}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Analysis mode" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="comprehensive">Comprehensive</SelectItem>
              <SelectItem value="price">Price Focus</SelectItem>
              <SelectItem value="production">Production Focus</SelectItem>
              <SelectItem value="risk">Risk Assessment</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Analysis Tabs */}
      <Tabs defaultValue="dashboard" className="space-y-4">
        <TabsList>
          <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
          <TabsTrigger value="configuration">Configuration</TabsTrigger>
          <TabsTrigger value="commodities">Commodities</TabsTrigger>
        </TabsList>

        <TabsContent value="dashboard" className="space-y-6">
          <AnalyticsDashboard />
        </TabsContent>

        <TabsContent value="configuration" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Settings className="h-5 w-5" />
                <span>Analytics Configuration</span>
              </CardTitle>
              <CardDescription>
                Configure data sources, analysis parameters, and visualization options
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Data Sources */}
              <div>
                <h3 className="text-lg font-medium mb-3">Data Sources</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Card>
                    <CardContent className="pt-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <Database className="h-5 w-5 text-blue-500" />
                          <span>USGS Data</span>
                        </div>
                        <Switch
                          checked={config.dataSources.includes('usgs')}
                          onCheckedChange={() => handleDataSourceToggle('usgs')}
                        />
                      </div>
                      <p className="text-sm text-muted-foreground mt-2">
                        Geological survey data from USGS and other national agencies
                      </p>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="pt-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <BarChart3 className="h-5 w-5 text-indigo-500" />
                          <span>FRED Data</span>
                        </div>
                        <Switch
                          checked={config.dataSources.includes('fred')}
                          onCheckedChange={() => handleDataSourceToggle('fred')}
                        />
                      </div>
                      <p className="text-sm text-muted-foreground mt-2">
                        Economic indicators and financial data from Federal Reserve
                      </p>
                    </CardContent>
                  </Card>
                </div>
              </div>

              {/* Analysis Depth */}
              <div>
                <h3 className="text-lg font-medium mb-3">Analysis Depth</h3>
                <Select value={config.analysisDepth} onValueChange={(value) => handleConfigChange('analysisDepth', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select analysis depth" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="basic">Basic Analysis</SelectItem>
                    <SelectItem value="standard">Standard Analysis</SelectItem>
                    <SelectItem value="detailed">Detailed Analysis</SelectItem>
                    <SelectItem value="comprehensive">Comprehensive Analysis</SelectItem>
                  </SelectContent>
                </Select>
                <p className="text-sm text-muted-foreground mt-2">
                  Controls the depth and complexity of analytical computations
                </p>
              </div>

              {/* Forecasting Models */}
              <div>
                <h3 className="text-lg font-medium mb-3">Forecasting Models</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {['ml_ensemble', 'econometric', 'expert_consensus', 'timeseries_arima'].map((model) => (
                    <Card key={model}>
                      <CardContent className="pt-4">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-2">
                            <Zap className="h-5 w-5 text-yellow-500" />
                            <span className="capitalize">
                              {model.replace('_', ' ')}
                            </span>
                          </div>
                          <Switch
                            checked={config.forecastingModels.includes(model)}
                            onCheckedChange={() => handleForecastingModelToggle(model)}
                          />
                        </div>
                        <p className="text-sm text-muted-foreground mt-2">
                          {model === 'ml_ensemble' && 'Machine learning ensemble models'}
                          {model === 'econometric' && 'Econometric forecasting models'}
                          {model === 'expert_consensus' && 'Expert consensus algorithms'}
                          {model === 'timeseries_arima' && 'Time series ARIMA models'}
                        </p>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>

              {/* Risk Factors */}
              <div>
                <h3 className="text-lg font-medium mb-3">Risk Assessment Factors</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {['political', 'environmental', 'economic', 'geopolitical', 'supply_chain', 'market'].map((factor) => (
                    <Card key={factor}>
                      <CardContent className="pt-4">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-2">
                            <AlertTriangle className="h-5 w-5 text-red-500" />
                            <span className="capitalize">{factor.replace('_', ' ')}</span>
                          </div>
                          <Switch
                            checked={config.riskFactors.includes(factor)}
                            onCheckedChange={() => handleRiskFactorToggle(factor)}
                          />
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>

              {/* Visualization Options */}
              <div>
                <h3 className="text-lg font-medium mb-3">Visualization</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="visualizationType">Visualization Type</Label>
                    <Select 
                      value={config.visualizationType} 
                      onValueChange={(value) => handleConfigChange('visualizationType', value)}
                    >
                      <SelectTrigger id="visualizationType">
                        <SelectValue placeholder="Select visualization type" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="interactive">Interactive Charts</SelectItem>
                        <SelectItem value="static">Static Reports</SelectItem>
                        <SelectItem value="dashboard">Dashboard View</SelectItem>
                        <SelectItem value="presentation">Presentation Mode</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <div className="flex items-center justify-between">
                      <Label htmlFor="autoRefresh">Auto Refresh</Label>
                      <Switch
                        id="autoRefresh"
                        checked={config.autoRefresh}
                        onCheckedChange={(checked) => handleConfigChange('autoRefresh', checked)}
                      />
                    </div>
                    {config.autoRefresh && (
                      <div className="mt-2">
                        <Label htmlFor="refreshInterval">Refresh Interval (seconds)</Label>
                        <Input
                          id="refreshInterval"
                          type="number"
                          min="30"
                          max="3600"
                          value={config.refreshInterval}
                          onChange={(e) => handleConfigChange('refreshInterval', parseInt(e.target.value))}
                        />
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Save Configuration */}
              <div className="flex justify-end">
                <Button onClick={() => console.log('Configuration saved:', config)}>
                  Save Configuration
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="commodities" className="space-y-6">
          <CommodityDashboard />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default AnalyticsPanel;