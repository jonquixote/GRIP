import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
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
  CheckCircle
} from 'lucide-react';
import { motion } from 'framer-motion';
import { commodityService } from '../services/api';
import AnalyticsDashboard from './AnalyticsDashboard';

const AnalyticsPanel = () => {
  const [selectedCommodity, setSelectedCommodity] = useState('');
  const [commodities, setCommodities] = useState([]);
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analysisType, setAnalysisType] = useState('price');

  useEffect(() => {
    fetchCommodities();
  }, []);

  const fetchCommodities = async () => {
    try {
      const response = await commodityService.getAll();
      setCommodities(response.data);
      if (response.data.length > 0) {
        setSelectedCommodity(response.data[0].id.toString());
      }
    } catch (error) {
      console.error('Error fetching commodities:', error);
    }
  };

  const fetchAnalysis = async () => {
    if (!selectedCommodity) return;

    try {
      setLoading(true);
      // Mock data for now
      const mockData = {
        summary: {
          overall_assessment: 'Positive',
          investment_outlook: 'Buy',
          risk_level: 'Medium',
          confidence_score: 0.85,
          risk_factors: ['Supply chain disruption', 'Geopolitical tension']
        }
      };
      setAnalysisData(mockData);
    } catch (error) {
      console.error('Error fetching analysis:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedCommodity) {
      fetchAnalysis();
    }
  }, [selectedCommodity, analysisType]);

  const generateMockChartData = (type) => {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return months.map(month => ({
      month,
      value: Math.floor(Math.random() * 1000) + 500,
      volume: Math.floor(Math.random() * 100) + 50,
      volatility: Math.random() * 0.1 + 0.02
    }));
  };

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  const selectedCommodityData = commodities.find(c => c.id.toString() === selectedCommodity);

  return (
    <div className="space-y-6">
      {/* Controls */}
      <Card>
        <CardHeader>
          <CardTitle>Analytics Configuration</CardTitle>
          <CardDescription>
            Select commodity and analysis type to view detailed insights
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <label className="text-sm font-medium mb-2 block">Commodity</label>
              <Select value={selectedCommodity} onValueChange={setSelectedCommodity}>
                <SelectTrigger>
                  <SelectValue placeholder="Select a commodity" />
                </SelectTrigger>
                <SelectContent>
                  {commodities.map(commodity => (
                    <SelectItem key={commodity.id} value={commodity.id.toString()}>
                      {commodity.name} ({commodity.symbol})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="flex-1">
              <label className="text-sm font-medium mb-2 block">Analysis Type</label>
              <Select value={analysisType} onValueChange={setAnalysisType}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="price">Price Analysis</SelectItem>
                  <SelectItem value="production">Production Analysis</SelectItem>
                  <SelectItem value="ml">ML Predictions</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="flex items-end">
              <Button onClick={fetchAnalysis} disabled={loading}>
                {loading ? 'Analyzing...' : 'Analyze'}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Analysis Results */}
      {analysisData && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {analysisData.summary && (
              <>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Overall Assessment</CardTitle>
                    <Target className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <Badge className={
                      analysisData.summary.overall_assessment === 'Positive' 
                        ? 'bg-green-100 text-green-800' 
                        : analysisData.summary.overall_assessment === 'Negative'
                        ? 'bg-red-100 text-red-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }>
                      {analysisData.summary.overall_assessment}
                    </Badge>
                    <p className="text-xs text-muted-foreground mt-2">
                      Investment Outlook: {analysisData.summary.investment_outlook}
                    </p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Risk Level</CardTitle>
                    <AlertTriangle className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <Badge className={
                      analysisData.summary.risk_level === 'Low' 
                        ? 'bg-green-100 text-green-800' 
                        : analysisData.summary.risk_level === 'High'
                        ? 'bg-red-100 text-red-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }>
                      {analysisData.summary.risk_level}
                    </Badge>
                    <p className="text-xs text-muted-foreground mt-2">
                      {analysisData.summary.risk_factors?.length || 0} risk factors identified
                    </p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Confidence Score</CardTitle>
                    <CheckCircle className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">
                      {(analysisData.summary.confidence_score * 100).toFixed(0)}%
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Analysis reliability
                    </p>
                  </CardContent>
                </Card>
              </>
            )}
          </div>

          {/* Analysis Tabs */}
          <Tabs defaultValue="charts" className="space-y-4">
            <TabsList>
              <TabsTrigger value="charts">Charts</TabsTrigger>
              <TabsTrigger value="statistics">Statistics</TabsTrigger>
              <TabsTrigger value="insights">Insights</TabsTrigger>
              <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
            </TabsList>

            <TabsContent value="charts" className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Price Trend Chart */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <LineChart className="h-5 w-5" />
                      <span>Price Trend</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ResponsiveContainer width="100%" height={300}>
                      <LineChart data={generateMockChartData('price')}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="month" />
                        <YAxis />
                        <Tooltip />
                        <Line 
                          type="monotone" 
                          dataKey="value" 
                          stroke="#8884d8" 
                          strokeWidth={2}
                          dot={{ fill: '#8884d8' }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>

                {/* Volume Analysis Chart */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <BarChart3 className="h-5 w-5" />
                      <span>Volume Analysis</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={generateMockChartData('volume')}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="month" />
                        <YAxis />
                        <Tooltip />
                        <Bar dataKey="volume" fill="#82ca9d" />
                      </BarChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>

                {/* Volatility Chart */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Activity className="h-5 w-5" />
                      <span>Volatility Index</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ResponsiveContainer width="100%" height={300}>
                      <AreaChart data={generateMockChartData('volatility')}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="month" />
                        <YAxis />
                        <Tooltip />
                        <Area type="monotone" dataKey="volatility" stroke="#ffc658" fill="#ffc658" fillOpacity={0.3} />
                      </AreaChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>

                {/* Distribution Pie Chart */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <PieChartIcon className="h-5 w-5" />
                      <span>Market Distribution</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ResponsiveContainer width="100%" height={300}>
                      <PieChart>
                        <Pie
                          data={[
                            { name: 'North America', value: 35 },
                            { name: 'Europe', value: 25 },
                            { name: 'Asia-Pacific', value: 30 },
                            { name: 'South America', value: 7 },
                            { name: 'Africa', value: 3 }
                          ]}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          outerRadius={80}
                          fill="#8884d8"
                          dataKey="value"
                          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        >
                          {COLORS.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="statistics" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Statistical Summary</CardTitle>
                  <CardDescription>
                    Key statistical measures for the selected commodity
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="p-4 bg-muted rounded-lg">
                      <div className="text-2xl font-bold">1,245.67</div>
                      <div className="text-sm text-muted-foreground">Average Price</div>
                    </div>
                    <div className="p-4 bg-muted rounded-lg">
                      <div className="text-2xl font-bold">8.2%</div>
                      <div className="text-sm text-muted-foreground">Volatility</div>
                    </div>
                    <div className="p-4 bg-muted rounded-lg">
                      <div className="text-2xl font-bold">12.4M</div>
                      <div className="text-sm text-muted-foreground">Volume</div>
                    </div>
                    <div className="p-4 bg-muted rounded-lg">
                      <div className="text-2xl font-bold">0.78</div>
                      <div className="text-sm text-muted-foreground">Correlation</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="insights" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Market Insights</CardTitle>
                  <CardDescription>
                    AI-generated insights and recommendations
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-start space-x-2">
                        <TrendingUp className="h-5 w-5 text-green-500 mt-0.5" />
                        <div>
                          <h4 className="font-medium">Bullish Trend Detected</h4>
                          <p className="text-sm text-muted-foreground mt-1">
                            The commodity is showing strong upward momentum with a 78% confidence level.
                          </p>
                        </div>
                      </div>
                    </div>
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-start space-x-2">
                        <AlertTriangle className="h-5 w-5 text-yellow-500 mt-0.5" />
                        <div>
                          <h4 className="font-medium">Supply Chain Risk</h4>
                          <p className="text-sm text-muted-foreground mt-1">
                            Potential disruption in key production regions may affect supply.
                          </p>
                        </div>
                      </div>
                    </div>
                    <div className="p-4 border rounded-lg">
                      <div className="flex items-start space-x-2">
                        <Target className="h-5 w-5 text-blue-500 mt-0.5" />
                        <div>
                          <h4 className="font-medium">Investment Recommendation</h4>
                          <p className="text-sm text-muted-foreground mt-1">
                            Consider increasing position size with a target price of $1,350.
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="dashboard" className="space-y-6">
              <AnalyticsDashboard />
            </TabsContent>
          </Tabs>
        </motion.div>
      )}
    </div>
  );
};

export default AnalyticsPanel;