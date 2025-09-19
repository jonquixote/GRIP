import React, { useState, useEffect } from 'react';
import Autosuggest from 'react-autosuggest';
import { Search, Layers } from 'lucide-react';
import { commodityService } from '../services/api';

// Teach Autosuggest how to calculate suggestions for any given input value.
const getSuggestions = (value, commodities) => {
  const inputValue = value.trim().toLowerCase();
  const inputLength = inputValue.length;

  return inputLength === 0 ? [] : commodities.filter(commodity =>
    commodity.name.toLowerCase().includes(inputValue) ||
    commodity.symbol.toLowerCase().includes(inputValue)
  );
};

// When suggestion is clicked, Autosuggest needs to populate the input
// based on the clicked suggestion. Teach Autosuggest how to calculate the
// input value for every given suggestion.
const getSuggestionValue = suggestion => suggestion.name;

// Use your imagination to render suggestions.
const renderSuggestion = suggestion => (
  <div className="flex items-center space-x-2 p-2 hover:bg-muted cursor-pointer">
    <Layers className="h-4 w-4 text-muted-foreground" />
    <div>
      <div className="font-medium">{suggestion.name}</div>
      <div className="text-sm text-muted-foreground">{suggestion.symbol}</div>
    </div>
  </div>
);

const CommoditySearch = ({ onCommoditySelect, onSearchChange, searchValue }) => {
  const [value, setValue] = useState(searchValue || '');
  const [suggestions, setSuggestions] = useState([]);
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

  const onChange = (event, { newValue }) => {
    setValue(newValue);
    if (onSearchChange) {
      onSearchChange({ target: { value: newValue } });
    }
  };

  const onSuggestionsFetchRequested = ({ value }) => {
    setSuggestions(getSuggestions(value, commodities));
  };

  const onSuggestionsClearRequested = () => {
    setSuggestions([]);
  };

  const onSuggestionSelected = (event, { suggestion }) => {
    if (onCommoditySelect) {
      onCommoditySelect(suggestion);
    }
    setValue('');
  };

  const inputProps = {
    placeholder: 'Search commodities...',
    value,
    onChange,
    className: 'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 pl-10'
  };

  return (
    <div className="relative">
      <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
      <Autosuggest
        suggestions={suggestions}
        onSuggestionsFetchRequested={onSuggestionsFetchRequested}
        onSuggestionsClearRequested={onSuggestionsClearRequested}
        onSuggestionSelected={onSuggestionSelected}
        getSuggestionValue={getSuggestionValue}
        renderSuggestion={renderSuggestion}
        inputProps={inputProps}
        theme={{
          container: 'relative',
          suggestionsContainer: 'absolute z-50 mt-1 w-full rounded-md border bg-popover text-popover-foreground shadow-md',
          suggestionsList: 'p-1',
          suggestion: 'cursor-pointer',
          suggestionHighlighted: 'bg-accent text-accent-foreground'
        }}
      />
      {loading && (
        <div className="absolute right-3 top-3">
          <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary border-t-transparent"></div>
        </div>
      )}
    </div>
  );
};

export default CommoditySearch;