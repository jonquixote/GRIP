import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { 
  Globe, 
  MapPin, 
  Flag, 
  Users, 
  TrendingUp, 
  TrendingDown, 
  AlertTriangle,
  Shield,
  Zap,
  Target,
  Eye
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, AreaChart, Area } from 'recharts';
import { motion } from 'framer-motion';

const GeopoliticalIntelligence = () => {
  const [selectedRegion, setSelectedRegion] = useState('global');
  const [geoData, setGeoData] = useState(null);
  const [loading, setLoading] = useState(false);

  // Mock data for demonstration
  const mockGeoData = {
    stability_index: 6.8,
    risk_level: 'Medium',
    top_regions: [
      { region: 'Middle East', stability: 3.2, risk: 'High' },
      { region: 'Africa', stability: 4.5, risk: 'Medium' },
      { region: 'Asia-Pacific', stability: 7.1, risk: 'Low' },
      { region: 'Latin America', stability: 5.8, risk: 'Medium' },
      { region: 'Europe', stability: 8.9, risk: 'Low' },
      { region: 'North America', stability: 9.2, risk: 'Low' }
    ],
    commodity_exposure: [
      { commodity: 'Oil', exposure: 85, risk: 'High' },
      { commodity: 'Natural Gas', exposure: 72, risk: 'High' },
      { commodity: 'Lithium', exposure: 68, risk: 'Medium' },
      { commodity: 'Copper', exposure: 55, risk: 'Medium' },
      { commodity: 'Rare Earths', exposure: 42, risk: 'Medium' }
    ],
    recent_events: [
      { date: '2025-09-15', event: 'New sanctions imposed', region: 'Middle East', impact: 'High', category: 'Political' },
      { date: '2025-09-12', event: 'Trade agreement signed', region: 'Asia-Pacific', impact: 'Positive', category: 'Economic' },
      { date: '2025-09-10', event: 'Mining strike begins', region: 'Latin America', impact: 'Medium', category: 'Social' },
      { date: '2025-09-08', event: 'New regulations announced', region: 'Europe', impact: 'Low', category: 'Regulatory' },
      { date: '2025-09-05', event: 'Infrastructure investment', region: 'Africa', impact: 'Positive', category: 'Economic' }
    ],
    stability_timeline: [
      { month: 'Jan', stability: 6.5 },
      { month: 'Feb', stability: 6.7 },
      { month: 'Mar', stability: 6.9 },
      { month: 'Apr', stability: 6.8 },
      { month: 'May', stability: 7.0 },
      { month: 'Jun', stability: 6.9 }
    ]
  };

  useEffect(() => {
    // Simulate API call
    const fetchData = async () => {
      setLoading(true);
      // In a real implementation, this would fetch from the backend
      setTimeout(() => {
        setGeoData(mockGeoData);
        setLoading(false);
      }, 800);
    };

    fetchData();
  }, [selectedRegion]);

  const getStabilityColor = (score) => {
    if (score >= 8) return 'text-green-500';
    if (score >= 6) return 'text-yellow-500';
    if (score >= 4) return 'text-orange-500';
    return 'text-red-500';
  };

  const getRiskLevelColor = (level) => {
    switch (level) {
      case 'High': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      case 'Medium': return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200';
      case 'Low': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'Positive': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
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
          <h2 className="text-2xl font-bold">Geopolitical Intelligence</h2>
          <p className="text-muted-foreground">Monitor political and regional risks affecting resource supply chains</p>
        </div>
        <Select value={selectedRegion} onValueChange={setSelectedRegion}>
          <SelectTrigger className="w-[200px]">
            <SelectValue placeholder="Select region" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="global">Global</SelectItem>
            <SelectItem value="middle-east">Middle East</SelectItem>
            <SelectItem value="africa">Africa</SelectItem>
            <SelectItem value="asia-pacific">Asia-Pacific</SelectItem>
            <SelectItem value="latin-america">Latin America</SelectItem>
            <SelectItem value="europe">Europe</SelectItem>
            <SelectItem value="north-america">North America</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {geoData && (
        <>
          {/* Overall Stability Score */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Shield className="h-5 w-5" />
                <span>Regional Stability Index</span>
              </CardTitle>
              <CardDescription>
                Comprehensive geopolitical stability assessment
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col md:flex-row items-center justify-between gap-6">
                <div className="text-center">
                  <div className={`text-5xl font-bold ${getStabilityColor(geoData.stability_index)}`}>
                    {geoData.stability_index.toFixed(1)}
                  </div>
                  <div className="text-lg mt-2">Stability Score</div>
                  <Badge className={`${getRiskLevelColor(geoData.risk_level)} mt-2 text-lg px-3 py-1`}>
                    {geoData.risk_level} Risk
                  </Badge>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  <div className="p-4 bg-muted rounded-lg text-center">
                    <div className="text-2xl font-bold">78%</div>
                    <div className="text-sm text-muted-foreground">Accuracy</div>
                  </div>
                  <div className="p-4 bg-muted rounded-lg text-center">
                    <div className="text-2xl font-bold">12h</div>
                    <div className="text-sm text-muted-foreground">Last Updated</div>
                  </div>
                  <div className="p-4 bg-muted rounded-lg text-center">
                    <div className="text-2xl font-bold">5</div>
                    <div className="text-sm text-muted-foreground">Active Events</div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Regional Stability */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Globe className="h-5 w-5" />
                  <span>Regional Stability Scores</span>
                </CardTitle>
                <CardDescription>
                  Comparative stability across key regions
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {geoData.top_regions.map((region, index) => (
                    <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex items-center space-x-3">
                        <Flag className="h-5 w-5 text-muted-foreground" />
                        <span className="font-medium">{region.region}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={getStabilityColor(region.stability)}>{region.stability.toFixed(1)}</span>
                        <Badge className={getRiskLevelColor(region.risk)}>
                          {region.risk}
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
                  <Target className="h-5 w-5" />
                  <span>Commodity Exposure</span>
                </CardTitle>
                <CardDescription>
                  Risk exposure by critical commodities
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {geoData.commodity_exposure.map((commodity, index) => (
                    <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex items-center space-x-3">
                        <div className="w-3 h-3 rounded-full bg-primary"></div>
                        <span className="font-medium">{commodity.commodity}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span>{commodity.exposure}%</span>
                        <Badge className={getRiskLevelColor(commodity.risk)}>
                          {commodity.risk}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Stability Timeline */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <TrendingUp className="h-5 w-5" />
                <span>Stability Trend Over Time</span>
              </CardTitle>
              <CardDescription>
                Historical stability score movement
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={geoData.stability_timeline}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis domain={[0, 10]} />
                  <Tooltip />
                  <Line 
                    type="monotone" 
                    dataKey="stability" 
                    stroke="#8884d8" 
                    strokeWidth={2}
                    dot={{ fill: '#8884d8' }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Recent Events */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Eye className="h-5 w-5" />
                <span>Recent Geopolitical Events</span>
              </CardTitle>
              <CardDescription>
                Latest developments affecting resource markets
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {geoData.recent_events.map((event, index) => (
                  <div key={index} className="flex flex-col sm:flex-row sm:items-center justify-between p-4 border rounded-lg gap-2">
                    <div className="flex items-start space-x-3">
                      <Calendar className="h-5 w-5 text-muted-foreground mt-0.5" />
                      <div>
                        <div className="font-medium">{event.event}</div>
                        <div className="text-sm text-muted-foreground flex items-center space-x-2 mt-1">
                          <MapPin className="h-4 w-4" />
                          <span>{event.region}</span>
                          <Users className="h-4 w-4 ml-2" />
                          <span>{event.category}</span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm">{event.date}</span>
                      <Badge className={getRiskLevelColor(event.impact)}>
                        {event.impact}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Intelligence Recommendations */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Zap className="h-5 w-5" />
                <span>Intelligence Recommendations</span>
              </CardTitle>
              <CardDescription>
                Actionable insights based on geopolitical analysis
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 border rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <Shield className="h-5 w-5 text-blue-500" />
                    <h4 className="font-medium">Risk Mitigation</h4>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Diversify suppliers in high-risk regions to reduce exposure.
                  </p>
                  <Button size="sm" variant="outline" className="mt-2">
                    View Recommendations
                  </Button>
                </div>
                <div className="p-4 border rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <Target className="h-5 w-5 text-green-500" />
                    <h4 className="font-medium">Opportunity Identification</h4>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Monitor emerging markets with improving stability scores.
                  </p>
                  <Button size="sm" variant="outline" className="mt-2">
                    Explore Opportunities
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

export default GeopoliticalIntelligence;