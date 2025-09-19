import React from 'react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Database, BarChart3, Layers } from 'lucide-react';

const DataSourceSelector = ({ value, onChange }) => {
  return (
    <Select value={value} onValueChange={onChange}>
      <SelectTrigger className="w-full">
        <SelectValue placeholder="Select data source" />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="usgs">
          <div className="flex items-center space-x-2">
            <Database className="h-4 w-4 text-blue-500" />
            <span>USGS Data</span>
          </div>
        </SelectItem>
        <SelectItem value="fred">
          <div className="flex items-center space-x-2">
            <BarChart3 className="h-4 w-4 text-indigo-500" />
            <span>FRED Data</span>
          </div>
        </SelectItem>
        <SelectItem value="both">
          <div className="flex items-center space-x-2">
            <Layers className="h-4 w-4 text-green-500" />
            <span>Both Sources</span>
          </div>
        </SelectItem>
      </SelectContent>
    </Select>
  );
};

export default DataSourceSelector;