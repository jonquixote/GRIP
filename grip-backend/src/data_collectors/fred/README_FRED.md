# FRED Data Collector

This module collects commodity price data and economic indicators from the Federal Reserve Economic Data (FRED) API.

## Setup

1. Obtain a FRED API key from https://fred.stlouisfed.org/docs/api/fred/
2. Set the API key as an environment variable:
   ```bash
   export FRED_API_KEY=your_api_key_here
   ```
   Or add it to your `.env` file:
   ```
   FRED_API_KEY=your_api_key_here
   ```

## Usage

### Collect all FRED data
```bash
cd grip-backend
python3 collect_fred_data.py
```

### Test the collector
```bash
cd grip-backend
python3 src/data_collectors/test_fred_collector.py
```

## Data Organization

The collector organizes data in the following structure:
```
src/data/fred/
├── commodities/
│   ├── copper/
│   │   ├── copper_data.json
│   │   └── copper_metadata.json
│   └── ... (other commodities)
├── economic_indicators/
│   └── economic_indicators.json
├── metadata/
│   ├── all_series_metadata.json
│   ├── copper_metadata.json
│   └── ... (metadata for other series)
├── search_results/
│   ├── search_results_gold.json
│   └── ... (other search results)
└── all_commodities_data.json
```

## Available Commodities

The following commodities are currently tracked:
- Base metals: copper, aluminum, nickel, zinc, lead, tin
- Energy: oil_wti, oil_brent, natural_gas, coal
- Other: iron_ore

## Methods

### collect_all_fred_data()
Performs a comprehensive collection of all FRED data including commodities, economic indicators, metadata, and search results.

### collect_all_commodities_data()
Collects price data for all available commodities.

### get_economic_indicators()
Collects relevant economic indicators that affect commodity prices.

### search_commodity_series(search_term)
Searches for FRED series related to a commodity.

### collect_price_data(commodity_name)
Collects price data for a specific commodity.

### test_connection()
Tests the FRED API connection.