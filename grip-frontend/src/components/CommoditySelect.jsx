import React, { useState, useEffect } from 'react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Layers } from 'lucide-react';
import { commodityService } from '../services/api';

const CommoditySelect = ({ value, onValueChange, placeholder = "Select a commodity" }) => {
  const [commodities, setCommodities] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchCommodities();
  }, []);

  const fetchCommodities = async () => {
    try {
      setLoading(true);
      const response = await commodityService.getAll();
      setCommodities(response.data);
    } catch (error) {
      console.error('Error fetching commodities:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Select value={value} onValueChange={onValueChange} disabled={loading}>
      <SelectTrigger className="w-full">
        {loading ? (
          <div className="flex items-center space-x-2">
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary border-t-transparent"></div>
            <span>Loading commodities...</span>
          </div>
        ) : (
          <>
            <Layers className="h-4 w-4 text-muted-foreground" />
            <SelectValue placeholder={placeholder} />
          </>
        )}
      </SelectTrigger>
      <SelectContent>
        {commodities.map((commodity) => (
          <SelectItem key={commodity.id} value={commodity.id.toString()}>
            <div className="flex items-center space-x-2">
              <div className="w-6 h-6 bg-gradient-to-br from-primary to-blue-600 rounded flex items-center justify-center text-white text-xs font-bold">
                {commodity.symbol?.substring(0, 2) || 'N/A'}
              </div>
              <div>
                <div className="font-medium">{commodity.name}</div>
                <div className="text-xs text-muted-foreground">{commodity.symbol}</div>
              </div>
            </div>
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
};

export default CommoditySelect;