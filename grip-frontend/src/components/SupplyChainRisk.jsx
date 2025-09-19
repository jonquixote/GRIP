import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { 
  AlertTriangle, 
  Shield, 
  MapPin, 
  Globe, 
  Factory, 
  Truck, 
  Anchor,
  Wifi,
  Zap,
  TrendingUp,
  TrendingDown
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { motion } from 'framer-motion';

const SupplyChainRisk = () => {
  const [selectedCommodity, setSelectedCommodity] = useState('copper');
  const [riskData, setRiskData] = useState(null);
  const [loading, setLoading] = useState(false);

  // Mock data for demonstration
  const mockRiskData = {
    overall_risk_score: 7.2,
    risk_level: 'High',
    top_risk_factors: [
      { factor: 'Geopolitical Tension', score: 8.5, impact: 'High' },
      { factor: 'Supply Concentration', score: 7.8, impact: 'High' },
      { factor: 'Infrastructure', score: 6.2, impact: 'Medium' },
      { factor: 'Regulatory', score: 5.9, impact: 'Medium' },
      { factor: 'Environmental', score: 4.3, impact: 'Low' }
    ],
    concentration_data: [
      { country: 'Chile', share: 25, risk: 'High' },
      { country: 'Peru', share: 18, risk: 'Medium' },
      { country: 'China', share: 15, risk: 'Medium' },
      { country: 'DRC', share: 12, risk: 'High' },
      { country: 'Other', share: 30, risk: 'Low' }
    ],
    risk_timeline: [
      { month: 'Jan', score: 6.2 },
      { month: 'Feb', score: 6.5 },
      { month: 'Mar', score: 6.8 },
      { month: 'Apr', score: 7.0 },
      { month: 'May', score: 7.2 },
      { month: 'Jun', score: 7.1 }
    ]
  };

  useEffect(() => {
    // Simulate API call
    const fetchData = async () => {
      setLoading(true);
      // In a real implementation, this would fetch from the backend
      setTimeout(() => {
        setRiskData(mockRiskData);
        setLoading(false);
      }, 800);
    };

    fetchData();
  }, [selectedCommodity]);

  const getRiskColor = (score) => {
    if (score >= 8) return 'text-red-500';
    if (score >= 6) return 'text-orange-500';
    if (score >= 4) return 'text-yellow-500';
    return 'text-green-500';
  };

  const getRiskLevelColor = (level) => {
    switch (level) {
      case 'High': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      case 'Medium': return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200';
      case 'Low': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
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
          <h2 className="text-2xl font-bold">Supply Chain Risk Assessment</h2>
          <p className="text-muted-foreground">Monitor and evaluate supply chain vulnerabilities</p>
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

      {riskData && (
        <>
          {/* Overall Risk Score */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Shield className="h-5 w-5" />
                <span>Overall Risk Assessment</span>
              </CardTitle>
              <CardDescription>
                Comprehensive supply chain risk evaluation
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col md:flex-row items-center justify-between gap-6">
                <div className="text-center">
                  <div className={`text-5xl font-bold ${getRiskColor(riskData.overall_risk_score)}`}>
                    {riskData.overall_risk_score.toFixed(1)}
                  </div>
                  <div className="text-lg mt-2">Risk Score</div>
                  <Badge className={`${getRiskLevelColor(riskData.risk_level)} mt-2 text-lg px-3 py-1`}>
                    {riskData.risk_level} Risk
                  </Badge>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  <div className="p-4 bg-muted rounded-lg text-center">
                    <div className="text-2xl font-bold">85%</div>
                    <div className="text-sm text-muted-foreground">Confidence</div>
                  </div>
                  <div className="p-4 bg-muted rounded-lg text-center">
                    <div className="text-2xl font-bold">24h</div>
                    <div className="text-sm text-muted-foreground">Last Updated</div>
                  </div>
                  <div className="p-4 bg-muted rounded-lg text-center">
                    <div className="text-2xl font-bold">3</div>
                    <div className="text-sm text-muted-foreground">Alerts</div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Risk Factors */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <AlertTriangle className="h-5 w-5" />
                  <span>Top Risk Factors</span>
                </CardTitle>
                <CardDescription>
                  Key factors contributing to supply chain risk
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {riskData.top_risk_factors.map((factor, index) => (
                    <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex items-center space-x-3">
                        <div className={`w-3 h-3 rounded-full ${
                          factor.score >= 8 ? 'bg-red-500' : 
                          factor.score >= 6 ? 'bg-orange-500' : 
                          factor.score >= 4 ? 'bg-yellow-500' : 'bg-green-500'
                        }`}></div>
                        <span className="font-medium">{factor.factor}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={getRiskColor(factor.score)}>{factor.score.toFixed(1)}</span>
                        <Badge className={getRiskLevelColor(factor.impact)}>
                          {factor.impact}
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
                  <Globe className="h-5 w-5" />
                  <span>Supply Concentration</span>
              </CardTitle>
                <CardDescription>
                  Geographic distribution of supply sources
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={riskData.concentration_data}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="share"
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    >
                      {riskData.concentration_data.map((entry, index) => (
                        <Cell 
                          key={`cell-${index}`} 
                          fill={
                            entry.risk === 'High' ? '#ef4444' :
                            entry.risk === 'Medium' ? '#f97316' : '#22c55e'
                          } 
                        />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Risk Timeline */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <TrendingUp className="h-5 w-5" />
                <span>Risk Trend Over Time</span>
              </CardTitle>
              <CardDescription>
                Historical risk score movement
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={riskData.risk_timeline}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis domain={[0, 10]} />
                  <Tooltip />
                  <Bar dataKey="score" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Risk Mitigation Recommendations */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Zap className="h-5 w-5" />
                <span>Risk Mitigation Recommendations</span>
              </CardTitle>
              <CardDescription>
                Actionable strategies to reduce supply chain risk
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div className="p-4 border rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <Factory className="h-5 w-5 text-blue-500" />
                    <h4 className="font-medium">Diversify Suppliers</h4>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Expand supplier base to reduce dependency on single sources.
                  </p>
                  <Button size="sm" variant="outline" className="mt-2">
                    View Suppliers
                  </Button>
                </div>
                <div className="p-4 border rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <Truck className="h-5 w-5 text-green-500" />
                    <h4 className="font-medium">Alternative Logistics</h4>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Identify backup transportation routes and methods.
                  </p>
                  <Button size="sm" variant="outline" className="mt-2">
                    Explore Options
                  </Button>
                </div>
                <div className="p-4 border rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <Anchor className="h-5 w-5 text-purple-500" />
                    <h4 className="font-medium">Strategic Stockpiles</h4>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Maintain buffer inventory for critical periods.
                  </p>
                  <Button size="sm" variant="outline" className="mt-2">
                    Calculate Needs
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

export default SupplyChainRisk;