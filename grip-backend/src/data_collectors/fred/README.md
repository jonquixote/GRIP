# FRED Data Collector

This directory contains the FRED data collector script that collects commodity price data and economic indicators from the Federal Reserve Economic Data (FRED) API.

## Usage

To run the FRED collector and collect all available data:

```bash
cd /path/to/grip-backend
python3 src/data_collectors/fred/collect_fred_data.py
```

## Directory Structure

The collector saves data to the following organized structure in `grip-backend/data/fred/`:
```
grip-backend/data/fred/
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

## Requirements

- FRED API key set in environment variable `FRED_API_KEY`
- Python dependencies installed (see grip-backend/requirements.txt)