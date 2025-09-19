import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Input } from '../components/ui/input';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Area,
  AreaChart,
  ReferenceLine
} from 'recharts';
import { 
  Brain, 
  TrendingUp, 
  TrendingDown, 
  Target, 
  AlertCircle,
  Zap,
  Calendar,
  BarChart3,
  Activity
} from 'lucide-react';
import { motion } from 'framer-motion';
import { commodityService } from '../services/api';

const PredictionsPanel = () => {
  const [selectedCommodity, setSelectedCommodity] = useState('');
  const [commodities, setCommodities] = useState([]);
  const [predictionData, setPredictionData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [predictionPeriods, setPredictionPeriods] = useState(30);

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

  const fetchPredictions = async () => {
    if (!selectedCommodity) return;

    try {
      setLoading(true);
      // Mock data for now
      const mockData = {
        best_model: 'random_forest',
        model_performance: {
          random_forest: {
            test_r2: 0.852
          }
        },
        predictions: {
          predictions: Array.from({ length: predictionPeriods }, () => Math.random() * 1000 + 1000),
          confidence_intervals: Array.from({ length: predictionPeriods }, (_, i) => ({
            lower: 1000 + Math.random() * 500,
            upper: 1500 + Math.random() * 500
          })),
          prediction_dates: Array.from({ length: predictionPeriods }, (_, i) => 
            new Date(Date.now() + i * 24 * 60 * 60 * 1000).toISOString()
          )
        }
      };
      setPredictionData(mockData);
    } catch (error) {
      console.error('Error fetching predictions:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedCommodity) {
      fetchPredictions();
    }
  }, [selectedCommodity]);

  // Generate mock prediction data for visualization
  const generatePredictionChartData = () => {
    if (!predictionData?.predictions?.predictions) return [];

    const predictions = predictionData.predictions.predictions;
    const confidenceIntervals = predictionData.predictions.confidence_intervals || [];
    const predictionDates = predictionData.predictions.prediction_dates || [];

    return predictions.map((prediction, index) => ({
      date: predictionDates[index] ? new Date(predictionDates[index]).toLocaleDateString() : `Day ${index + 1}`,
      prediction: prediction,
      lower: confidenceIntervals[index]?.lower || prediction * 0.9,
      upper: confidenceIntervals[index]?.upper || prediction * 1.1,
      confidence: Math.max(0.5, 1 - (index * 0.02)) // Decreasing confidence over time
    }));
  };

  // Generate historical + prediction combined data
  const generateCombinedChartData = () => {
    const historical = Array.from({ length: 30 }, (_, i) => ({
      date: new Date(Date.now() - (29 - i) * 24 * 60 * 60 * 1000).toLocaleDateString(),
      value: 1000 + Math.sin(i * 0.2) * 100 + Math.random() * 50,
      type: 'historical'
    }));

    const predictions = generatePredictionChartData().map(item => ({
      date: item.date,
      value: item.prediction,
      lower: item.lower,
      upper: item.upper,
      type: 'prediction'
    }));

    return [...historical, ...predictions];
  };

  const selectedCommodityData = commodities.find(c => c.id.toString() === selectedCommodity);

  return (
    <div className="space-y-6">
      {/* Controls */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Brain className="h-5 w-5" />
            <span>ML Predictions Configuration</span>
          </CardTitle>
          <CardDescription>
            Generate AI-powered predictions for commodity prices and trends
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
              <label className="text-sm font-medium mb-2 block">Prediction Period (Days)</label>
              <Input
                type="number"
                value={predictionPeriods}
                onChange={(e) => setPredictionPeriods(parseInt(e.target.value) || 30)}
                min="1"
                max="365"
              />
            </div>
            <div className="flex items-end">
              <Button onClick={fetchPredictions} disabled={loading}>
                {loading ? 'Predicting...' : 'Generate Predictions'}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Prediction Results */}
      {predictionData && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Model Performance Summary */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Best Model</CardTitle>
                <Brain className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold capitalize">
                  {predictionData.best_model?.replace('_', ' ') || 'Random Forest'}
                </div>
                <p className="text-xs text-muted-foreground">
                  Selected algorithm
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Model Accuracy</CardTitle>
                <Target className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {predictionData.model_performance?.random_forest?.test_r2 
                    ? (predictionData.model_performance.random_forest.test_r2 * 100).toFixed(1) + '%'
                    : '85.2%'}
                </div>
                <p className="text-xs text-muted-foreground">
                  R² Score
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Prediction Confidence</CardTitle>
                <Zap className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {predictionData.predictions?.confidence_intervals 
                    ? '78%' 
                    : '75%'}
                </div>
                <p className="text-xs text-muted-foreground">
                  Average confidence
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Forecast Horizon</CardTitle>
                <Calendar className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {predictionPeriods}
                </div>
                <p className="text-xs text-muted-foreground">
                  Days ahead
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Prediction Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Main Prediction Chart */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <LineChart className="h-5 w-5" />
                  <span>Price Predictions with Confidence Intervals</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart
                    data={generateCombinedChartData()}
                    margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="date" 
                      tick={{ fontSize: 12 }}
                      tickFormatter={(value) => {
                        if (value.includes('/')) {
                          const [month, day] = value.split('/');
                          return `${month}/${day}`;
                        }
                        return value;
                      }}
                    />
                    <YAxis domain={['auto', 'auto']} />
                    <Tooltip 
                      formatter={(value) => [`$${value.toFixed(2)}`, 'Price']}
                      labelFormatter={(label) => `Date: ${label}`}
                    />
                    <Line
                      type="monotone"
                      dataKey="value"
                      stroke="#8884d8"
                      strokeWidth={2}
                      dot={false}
                      name="Price"
                    />
                    <Line
                      type="monotone"
                      dataKey="lower"
                      stroke="#82ca9d"
                      strokeDasharray="3 3"
                      strokeWidth={1}
                      dot={false}
                      name="Lower Bound"
                    />
                    <Line
                      type="monotone"
                      dataKey="upper"
                      stroke="#82ca9d"
                      strokeDasharray="3 3"
                      strokeWidth={1}
                      dot={false}
                      name="Upper Bound"
                    />
                    <ReferenceLine 
                      x={generateCombinedChartData().findIndex(d => d.type === 'prediction') > 0 
                        ? generateCombinedChartData()[generateCombinedChartData().findIndex(d => d.type === 'prediction') - 1].date 
                        : null}
                      stroke="red" 
                      strokeDasharray="3 3"
                    />
                  </LineChart>
                </ResponsiveContainer>
                <div className="flex justify-center mt-2">
                  <div className="flex items-center space-x-4 text-sm">
                    <div className="flex items-center space-x-1">
                      <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
                      <span>Historical Data</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                      <span>Predictions</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                      <span>Confidence Interval</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <div className="w-3 h-0.5 bg-red-500"></div>
                      <span>Prediction Start</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Confidence Over Time */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Zap className="h-5 w-5" />
                  <span>Confidence Over Time</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart
                    data={generatePredictionChartData()}
                    margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="date" 
                      tick={{ fontSize: 12 }}
                      tickFormatter={(value) => {
                        if (value.includes('/')) {
                          const [month, day] = value.split('/');
                          return `${month}/${day}`;
                        }
                        return value;
                      }}
                    />
                    <YAxis domain={[0, 1]} />
                    <Tooltip 
                      formatter={(value) => [`${(value * 100).toFixed(1)}%`, 'Confidence']}
                      labelFormatter={(label) => `Date: ${label}`}
                    />
                    <Area
                      type="monotone"
                      dataKey="confidence"
                      stroke="#ffc658"
                      fill="#ffc658"
                      fillOpacity={0.3}
                      name="Confidence"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Prediction Summary */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Target className="h-5 w-5" />
                  <span>Prediction Summary</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                    <span>Expected Price Change</span>
                    <Badge variant="secondary" className="flex items-center space-x-1">
                      <TrendingUp className="h-3 w-3" />
                      <span>+5.2%</span>
                    </Badge>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                    <span>Risk Level</span>
                    <Badge variant="outline" className="bg-yellow-100 text-yellow-800">
                      Medium
                    </Badge>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                    <span>Volatility Forecast</span>
                    <Badge variant="outline" className="bg-orange-100 text-orange-800">
                      Increasing
                    </Badge>
                  </div>
                  <div className="p-3 bg-blue-50 dark:bg-blue-950 rounded-lg">
                    <h4 className="font-medium mb-2">Recommendation</h4>
                    <p className="text-sm text-muted-foreground">
                      Based on the analysis, consider a cautious buy position with a target price of $1,350.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default PredictionsPanel;