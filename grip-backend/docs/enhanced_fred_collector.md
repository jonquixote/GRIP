# Enhanced FRED Collector Documentation

## Overview
The enhanced FRED collector now collects data for 25 commodities (previously 23) and 43 economic indicators (previously 38). The enhancements focused on adding new commodity series that are available through the FRED API and fixing issues with existing series.

## New Commodity Series Added

### Energy Commodities
1. **Propane** - `DPROPANEMBTX`
   - Title: Propane Prices: Mont Belvieu, Texas
   - Units: U.S. Dollars per Gallon
   - Frequency: Daily
   - Records: ~955

2. **Heating Oil** - `DHOILNYH`
   - Title: No. 2 Heating Oil Prices: New York Harbor
   - Units: U.S. Dollars per Gallon
   - Frequency: Daily
   - Records: ~954

3. **Diesel** - `GASDESW`
   - Title: US Diesel Sales Price
   - Units: U.S. Dollars per Gallon
   - Frequency: Weekly
   - Records: ~1000

4. **Gasoline** - `GASREGW`
   - Title: US Regular All Formulations Gas Price
   - Units: U.S. Dollars per Gallon
   - Frequency: Weekly
   - Records: ~1000

### Agricultural Commodities
5. **Palm Oil** - `PPOILUSDM`
   - Title: Global price of Palm Oil
   - Units: U.S. Dollars per Metric Ton
   - Frequency: Monthly
   - Records: ~426

## Updated/Fixed Commodity Series

1. **Cotton** - Updated from `PCOTTONBUSD` to `PCOTTINDUSDM`
   - Title: Global price of Cotton
   - Units: U.S. Cents per Pound
   - Frequency: Monthly
   - Records: ~426

2. **Sugar** - Updated from `PSUGAUSDM` to `PSUGAISAUSDM`
   - Title: Global price of Sugar, No. 11, World
   - Units: U.S. Cents per Pound
   - Frequency: Monthly
   - Records: ~426

3. **Cocoa** - Updated from `PCOCOUSD` to `PCOCOUSDM`
   - Title: Global price of Cocoa
   - Units: U.S. Dollars per Metric Ton
   - Frequency: Monthly
   - Records: ~426

## Removed Problematic Series
The following series were removed because they were not available or returned errors from the FRED API:
- Lumber (`PLUMMUSDM`)
- Rubber (`PRUBBRUSDM`)
- Fertilizer (`PFERTUSDM`)

## Enhanced Economic Indicators
The economic indicators collection was enhanced from 38 to 43 indicators by adding:
- 10Y Breakeven Inflation Rate
- High Yield Spread
- NASDAQ Composite Index
- Manufacturing PMI
- University of Michigan Inflation Expectations
- House Price Index
- Foreign Direct Investment

## Data Organization
All collected data continues to be stored in the organized directory structure:
- `grip-backend/data/fred/commodities/` - Commodity price data
- `grip-backend/data/fred/economic_indicators/` - Economic indicators
- `grip-backend/data/fred/metadata/` - Series metadata
- `grip-backend/data/fred/search_results/` - Search results for critical minerals

## Search Terms Expansion
The collector now searches for 60+ terms related to critical minerals and rare earth elements, including:
- Rare earth elements (neodymium, praseodymium, lanthanum, cerium, etc.)
- Critical minerals (lithium, cobalt, tantalum, etc.)
- Battery materials (lithium carbonate, cobalt sulfate, etc.)
- Additional energy and agricultural commodities

## Usage
The enhanced collector maintains full backward compatibility while providing expanded data coverage. All existing methods and interfaces continue to work as before.

```python
from src.data_collectors.fred_collector import FREDCollector

collector = FREDCollector()

# Collect data for all commodities
result = collector.collect_all_commodities_data()

# Collect data for specific new commodities
propane_data = collector.collect_price_data('propane')
diesel_data = collector.collect_price_data('diesel')

# Get enhanced economic indicators
indicators = collector.get_economic_indicators()
```

## Performance
The enhanced collector maintains the same rate limiting and error handling as the original implementation, with requests throttled to comply with FRED API limits (120 requests per minute).