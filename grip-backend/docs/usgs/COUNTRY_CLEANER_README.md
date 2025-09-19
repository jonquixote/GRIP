# GRIP Country Name Cleaner

A comprehensive tool to clean and standardize country names in USGS mineral commodity data files.

## Purpose

This script automatically cleans country names by:
- Fixing partial names and parsing errors
- Consolidating duplicate entries for the same countries
- Standardizing alternative country names
- Removing extraneous technical text
- Preserving all data records

## Usage

```bash
# Clean data in the default 'comprehensive_data' directory
python3 country_cleaner.py

# Clean data in a specific directory
python3 country_cleaner.py /path/to/your/data
```

## Features

- **Non-destructive**: Preserves all data records while cleaning country names
- **Comprehensive**: Handles 100+ common country name issues
- **Reusable**: Can be run on new data as it's collected
- **Self-reporting**: Provides detailed statistics on cleaning results

## What It Fixes

- Partial country names: "Chil" → "Chile"
- Names with extra text: "Australia not available Th" → "Australia"
- Duplicate variants: "Brazil Moderat" + "Brazil demand" → "Brazil"
- Alternative spellings: "Burma" → "Myanmar"
- Technical artifacts: "World total (rounded *" → "World total"

## Results

Typically reduces country name variants by 50-60% while preserving 100% of data records.