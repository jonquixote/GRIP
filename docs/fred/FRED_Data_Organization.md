# FRED Data Organization

This document describes how FRED data is organized within the GRIP platform.

## Directory Structure

```
grip-backend/data/fred/
├── commodities/
│   ├── copper/
│   │   ├── copper_data.json
│   │   └── copper_metadata.json
│   ├── aluminum/
│   │   ├── aluminum_data.json
│   │   └── aluminum_metadata.json
│   └── ... (other commodities)
├── economic_indicators/
│   ├── economic_indicators.json
│   └── ... (individual indicator files)
├── metadata/
│   ├── all_series_metadata.json
│   ├── copper_metadata.json
│   ├── aluminum_metadata.json
│   └── ... (metadata for other series)
├── search_results/
│   ├── search_results_gold.json
│   ├── search_results_silver.json
│   └── ... (other search results)
└── all_commodities_data.json
```

## Data Types

### 1. Commodity Price Data
Stored in `commodities/{commodity_name}/{commodity_name}_data.json`

Format:
```json
{
  "success": true,
  "data": [
    {
      "date": "2023-01-01",
      "price": 8500.50,
      "commodity": "copper",
      "source": "FRED",
      "series_id": "PCOPPUSDM",
      "realtime_start": "2023-01-01",
      "realtime_end": "2023-01-01"
    }
  ],
  "series_id": "PCOPPUSDM",
  "count": 1,
  "commodity": "copper",
  "series_info": {
    "id": "PCOPPUSDM",
    "title": "Global price of Copper",
    "units": "U.S. Dollars per Metric Ton",
    ...
  }
}
```

### 2. Economic Indicators
Stored in `economic_indicators/economic_indicators.json`

Format:
```json
{
  "collected_at": "2023-01-01T12:00:00Z",
  "indicators": {
    "GDP": {
      "value": 21000.5,
      "date": "2022-10-01",
      "series_id": "GDPC1"
    },
    "CPI": {
      "value": 296.8,
      "date": "2022-12-01",
      "series_id": "CPIAUCSL"
    }
  },
  "count": 8
}
```

### 3. Series Metadata
Stored in `metadata/{commodity_name}_metadata.json` and `metadata/all_series_metadata.json`

Format:
```json
{
  "id": "PCOPPUSDM",
  "realtime_start": "2023-01-01",
  "realtime_end": "2023-01-01",
  "title": "Global price of Copper",
  "observation_start": "1996-01-01",
  "observation_end": "2022-12-01",
  "frequency": "Monthly",
  "frequency_short": "M",
  "units": "U.S. Dollars per Metric Ton",
  "units_short": "USD/M.Ton",
  "seasonal_adjustment": "Not Seasonally Adjusted",
  "seasonal_adjustment_short": "NSA",
  "last_updated": "2023-01-05 07:46:11-06",
  "popularity": 99,
  "notes": "Global price of Copper. Data is sourced from the World Bank and International Monetary Fund (IMF)."
}
```

### 4. Search Results
Stored in `search_results/search_results_{term}.json`

Format:
```json
{
  "search_term": "gold",
  "collected_at": "2023-01-01T12:00:00Z",
  "series": [
    {
      "id": "GOLDAMGBD228NLBM",
      "title": "Gold Fixing Price 10:30 A.M. (London Gold Market) in London/British Pound",
      "frequency": "Daily, Close",
      "units": "British Pound per Troy Ounce",
      "seasonal_adjustment": "Not Seasonally Adjusted",
      "popularity": 85,
      "observation_start": "1968-01-02",
      "observation_end": "2022-12-30"
    }
  ],
  "total_found": 45,
  "filtered_count": 12
}
```

## Available Commodities

The following commodities are currently tracked from FRED:

- Base metals: copper, aluminum, nickel, zinc, lead, tin
- Energy: oil_wti, oil_brent, natural_gas, coal
- Other: iron_ore

## Collection Methods

### collect_all_commodities_data()
Collects price data for all available commodities and saves them in organized directories.

### get_economic_indicators()
Collects relevant economic indicators that affect commodity prices.

### search_commodity_series(search_term)
Searches for FRED series related to a commodity and saves the results.

### collect_all_fred_data()
Performs a comprehensive collection of all FRED data including commodities, economic indicators, metadata, and search results.