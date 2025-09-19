import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { 
  Leaf, 
  Recycle, 
  Droplets, 
  Wind, 
  Sun, 
  Zap, 
  Award, 
  TrendingUp, 
  TrendingDown, 
  AlertTriangle,
  Users,
  Globe
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, AreaChart, Area, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from 'recharts';
import { motion } from 'framer-motion';

const SustainabilityMetrics = () => {
  const [selectedCommodity, setSelectedCommodity] = useState('copper');
  const [sustainabilityData, setSustainabilityData] = useState(null);
  const [loading, setLoading] = useState(false);

  // Mock data for demonstration
  const mockSustainabilityData = {
    esg_score: 7.2,
    carbon_footprint: 4.5, // tons CO2/ton of commodity
    water_usage: 1200, // liters/ton
    energy_consumption: 8.2, // kWh/ton
    recycling_rate: 35, // percentage
    social_impact_score: 6.8,
    governance_score: 7.5,
    top_metrics: [
      { metric: 'Carbon Footprint', value: 4.5, unit: 'tons CO2/ton', trend: 'decreasing' },
      { metric: 'Water Usage', value: 1200, unit: 'L/ton', trend: 'decreasing' },
      { metric: 'Energy Consumption', value: 8.2, unit: 'kWh/ton', trend: 'stable' },
      { metric: 'Recycling Rate', value: 35, unit: '%', trend: 'increasing' },
      { metric: 'Social Impact', value: 6.8, unit: '/10', trend: 'increasing' }
    ],
    esg_breakdown: [
      { category: 'Environmental', score: 6.5 },
      { category: 'Social', score: 7.8 },
      { category: 'Governance', score: 8.2 }
    ],
    sustainability_timeline: [
      { year: '2020', carbon: 6.2, water: 1500, energy: 9.1, recycling: 22 },
      { year: '2021', carbon: 5.8, water: 1400, energy: 8.9, recycling: 25 },
      { year: '2022', carbon: 5.3, water: 1350, energy: 8.7, recycling: 28 },
      { year: '2023', carbon: 4.9, water: 1300, energy: 8.5, recycling: 31 },
      { year: '2024', carbon: 4.7, water: 1250, energy: 8.3, recycling: 33 },
      { year: '2025', carbon: 4.5, water: 1200, energy: 8.2, recycling: 35 }
    ],
    top_producers: [
      { producer: 'Producer A', esg_score: 8.5, location: 'Chile', carbon: 3.2 },
      { producer: 'Producer B', esg_score: 7.8, location: 'Peru', carbon: 4.1 },
      { producer: 'Producer C', esg_score: 7.2, location: 'Democratic Republic of Congo', carbon: 5.3 },
      { producer: 'Producer D', esg_score: 6.9, location: 'Australia', carbon: 4.8 },
      { producer: 'Producer E', esg_score: 6.5, location: 'United States', carbon: 5.1 }
    ]
  };

  useEffect(() => {
    // Simulate API call
    const fetchData = async () => {
      setLoading(true);
      // In a real implementation, this would fetch from the backend
      setTimeout(() => {
        setSustainabilityData(mockSustainabilityData);
        setLoading(false);
      }, 800);
    };

    fetchData();
  }, [selectedCommodity]);

  const getScoreColor = (score) => {
    if (score >= 8) return 'text-green-500';
    if (score >= 6) return 'text-blue-500';
    if (score >= 4) return 'text-yellow-500';
    return 'text-red-500';
  };

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'increasing': return <TrendingUp className="h-4 w-4 text-green-500" />;
      case 'decreasing': return <TrendingDown className="h-4 w-4 text-red-500" />;
      case 'stable': return <div className="h-4 w-4 text-gray-500">—</div>;
      default: return null;
    }
  };

  const getMetricLevelColor = (value, metric) => {
    // Different thresholds for different metrics
    if (metric === 'Carbon Footprint') {
      if (value <= 3) return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      if (value <= 5) return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
    }
    if (metric === 'Water Usage') {
      if (value <= 1000) return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      if (value <= 1500) return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
    }
    if (metric === 'Energy Consumption') {
      if (value <= 6) return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      if (value <= 9) return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
    }
    if (metric === 'Recycling Rate') {
      if (value >= 50) return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      if (value >= 30) return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
    }
    if (metric === 'Social Impact') {
      if (value >= 8) return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      if (value >= 6) return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
    }
    return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
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
          <h2 className="text-2xl font-bold">Sustainability Metrics</h2>
          <p className="text-muted-foreground">Environmental, Social, and Governance performance tracking</p>
        </div>
        <Select value={selectedCommodity} onValueChange={setSelectedCommodity}>
          <SelectTrigger className="w-[200px]">
            <SelectValue placeholder="Select commodity" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="copper">Copper</SelectItem>
            <SelectItem value="lithium">Lithium</SelectItem>
            <SelectItem value="rare_earths">Rare Earths</SelectItem>
            <SelectItem value="nickel">Nickel</SelectItem>
            <SelectItem value="cobalt">Cobalt</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {sustainabilityData && (
        <>
          {/* Overall ESG Score */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Leaf className="h-5 w-5" />
                <span>Overall ESG Performance</span>
              </CardTitle>
              <CardDescription>
                Comprehensive sustainability assessment score
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col md:flex-row items-center justify-between gap-6">
                <div className="text-center">
                  <div className={`text-5xl font-bold ${getScoreColor(sustainabilityData.esg_score)}`}>
                    {sustainabilityData.esg_score.toFixed(1)}
                  </div>
                  <div className="text-lg mt-2">ESG Score</div>
                  <Badge className={`${getMetricLevelColor(sustainabilityData.esg_score, 'ESG')} mt-2 text-lg px-3 py-1`}>
                    {sustainabilityData.esg_score >= 8 ? 'Excellent' : 
                     sustainabilityData.esg_score >= 6 ? 'Good' : 
                     sustainabilityData.esg_score >= 4 ? 'Fair' : 'Poor'}
                  </Badge>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="p-4 bg-muted rounded-lg text-center">
                    <div className="text-2xl font-bold">{sustainabilityData.carbon_footprint.toFixed(1)}</div>
                    <div className="text-sm text-muted-foreground">Carbon Footprint<br />(tons CO2/ton)</div>
                  </div>
                  <div className="p-4 bg-muted rounded-lg text-center">
                    <div className="text-2xl font-bold">{sustainabilityData.water_usage.toLocaleString()}</div>
                    <div className="text-sm text-muted-foreground">Water Usage<br />(L/ton)</div>
                  </div>
                  <div className="p-4 bg-muted rounded-lg text-center">
                    <div className="text-2xl font-bold">{sustainabilityData.energy_consumption.toFixed(1)}</div>
                    <div className="text-sm text-muted-foreground">Energy<br />(kWh/ton)</div>
                  </div>
                  <div className="p-4 bg-muted rounded-lg text-center">
                    <div className="text-2xl font-bold">{sustainabilityData.recycling_rate}%</div>
                    <div className="text-sm text-muted-foreground">Recycling Rate</div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* ESG Breakdown */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Award className="h-5 w-5" />
                  <span>ESG Category Breakdown</span>
                </CardTitle>
                <CardDescription>
                  Detailed scores across ESG dimensions
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {sustainabilityData.esg_breakdown.map((category, index) => (
                    <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex items-center space-x-3">
                        {category.category === 'Environmental' && <Leaf className="h-5 w-5 text-green-500" />}
                        {category.category === 'Social' && <Users className="h-5 w-5 text-blue-500" />}
                        {category.category === 'Governance' && <Globe className="h-5 w-5 text-purple-500" />}
                        <span className="font-medium">{category.category}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={getScoreColor(category.score)}>{category.score.toFixed(1)}</span>
                        <Badge className={getMetricLevelColor(category.score, category.category)}>
                          {category.score >= 8 ? 'Excellent' : 
                           category.score >= 6 ? 'Good' : 
                           category.score >= 4 ? 'Fair' : 'Poor'}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Recycle className="h-5 w-5" />
                  <span>Key Sustainability Metrics</span>
                </CardTitle>
                <CardDescription>
                  Performance indicators with trends
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {sustainabilityData.top_metrics.map((metric, index) => (
                    <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex items-center space-x-3">
                        <span className="font-medium">{metric.metric}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span>{metric.value}{metric.unit && ` ${metric.unit}`}</span>
                        {getTrendIcon(metric.trend)}
                        <Badge className={getMetricLevelColor(metric.value, metric.metric)}>
                          {metric.trend.charAt(0).toUpperCase() + metric.trend.slice(1)}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sustainability Timeline */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <TrendingUp className="h-5 w-5" />
                <span>Sustainability Improvements Over Time</span>
              </CardTitle>
              <CardDescription>
                Historical performance trends
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={sustainabilityData.sustainability_timeline}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis />
                  <Tooltip />
                  <Line 
                    type="monotone" 
                    dataKey="carbon" 
                    name="Carbon Footprint (tons CO2/ton)" 
                    stroke="#ef4444" 
                    strokeWidth={2}
                    dot={{ fill: '#ef4444' }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="water" 
                    name="Water Usage (L/ton)" 
                    stroke="#3b82f6" 
                    strokeWidth={2}
                    dot={{ fill: '#3b82f6' }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="energy" 
                    name="Energy Consumption (kWh/ton)" 
                    stroke="#f59e0b" 
                    strokeWidth={2}
                    dot={{ fill: '#f59e0b' }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="recycling" 
                    name="Recycling Rate (%)" 
                    stroke="#10b981" 
                    strokeWidth={2}
                    dot={{ fill: '#10b981' }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Top Producers Comparison */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Award className="h-5 w-5" />
                <span>Top Producers ESG Comparison</span>
              </CardTitle>
              <CardDescription>
                Sustainability performance by leading producers
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b">
                      <th className="text-left py-2">Producer</th>
                      <th className="text-left py-2">Location</th>
                      <th className="text-left py-2">ESG Score</th>
                      <th className="text-left py-2">Carbon (tons CO2/ton)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {sustainabilityData.top_producers.map((producer, index) => (
                      <tr key={index} className="border-b">
                        <td className="py-2 font-medium">{producer.producer}</td>
                        <td className="py-2">{producer.location}</td>
                        <td className="py-2">
                          <span className={getScoreColor(producer.esg_score)}>
                            {producer.esg_score.toFixed(1)}
                          </span>
                        </td>
                        <td className="py-2">
                          <span className={getMetricLevelColor(producer.carbon, 'Carbon Footprint')}>
                            {producer.carbon.toFixed(1)}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>

          {/* Sustainability Recommendations */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Zap className="h-5 w-5" />
                <span>Sustainability Recommendations</span>
              </CardTitle>
              <CardDescription>
                Actionable steps to improve sustainability performance
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div className="p-4 border rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <Wind className="h-5 w-5 text-blue-500" />
                    <h4 className="font-medium">Renewable Energy</h4>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Transition to renewable energy sources to reduce carbon footprint.
                  </p>
                  <Button size="sm" variant="outline" className="mt-2">
                    Explore Options
                  </Button>
                </div>
                <div className="p-4 border rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <Droplets className="h-5 w-5 text-cyan-500" />
                    <h4 className="font-medium">Water Efficiency</h4>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Implement water recycling systems to minimize consumption.
                  </p>
                  <Button size="sm" variant="outline" className="mt-2">
                    View Technologies
                  </Button>
                </div>
                <div className="p-4 border rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <Sun className="h-5 w-5 text-yellow-500" />
                    <h4 className="font-medium">Solar Integration</h4>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Install solar panels at mining sites for clean energy generation.
                  </p>
                  <Button size="sm" variant="outline" className="mt-2">
                    Calculate ROI
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
};

export default SustainabilityMetrics;