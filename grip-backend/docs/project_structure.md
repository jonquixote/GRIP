# GRIP Project Structure

This document describes the current organization of the GRIP backend project.

## Directory Structure

```
grip-backend/
├── data/
│   ├── fred/                 # FRED economic data
│   └── usgs/                 # USGS mineral commodity data
├── docs/
│   ├── usgs/                 # USGS-specific documentation
│   └── COUNTRY_CLEANER_README.md
├── src/
│   ├── analytics/            # Data analysis modules
│   ├── data_collectors/      # Data collection modules
│   │   ├── usgs/             # USGS data collection tools
│   │   ├── base_collector.py
│   │   ├── data_collection_service.py
│   │   ├── fred_collector.py
│   │   ├── usgs_collector.py
│   │   ├── usgs_commodity_codes.py
│   │   └── worldbank_collector.py
│   ├── database/             # Database models and connections
│   ├── models/               # Data models
│   ├── routes/               # API endpoints
│   ├── static/               # Static files
│   └── main.py               # Main application entry point
├── tests/                    # Test files and utilities
├── requirements.txt          # Python dependencies
└── venv/                     # Python virtual environment
```

## Key Directories

### data/usgs/
Contains all USGS mineral commodity data files in JSON format:
- Individual commodity data files (e.g., `copper_data_1996_2025.json`)
- `collection_summary.json` - Summary of collected data
- `usgs_mineral_commodities.json` - List of USGS tracked commodities
- `usgs_collector.log` - Log file for USGS data collection

### src/data_collectors/usgs/
Contains all USGS-specific data collection and processing scripts:
- `collect_commodity_data.py` - Collect data for a specific commodity
- `collect_comprehensive_data.py` - Collect data for all commodities
- `country_cleaner.py` - Clean and standardize country names
- `create_commodities_list.py` - Create list of commodities
- `extract_commodity_codes.py` - Extract commodity codes
- `extract_usgs_commodities.py` - Extract USGS commodities
- `find_commodity_codes.py` - Find commodity codes
- `parse_mineral_commodities.py` - Parse mineral commodities
- `scrape_usgs_commodities.py` - Scrape USGS commodities
- `verify_commodity_codes.py` - Verify commodity codes

### tests/
Contains test files and utility scripts:
- `test_comprehensive_collection.py` - Test comprehensive data collection
- `test_data_collection.py` - Test data collection
- `test_pdf_parsing.py` - Test PDF parsing
- `test_updated_codes.py` - Test updated codes
- `final_verification_test.py` - Final verification test
- `find_missing_years.py` - Find missing years in data

### docs/
Contains project documentation:
- `COUNTRY_CLEANER_README.md` - Documentation for country cleaner
- `usgs/` - USGS-specific documentation
  - `final_usgs_report.md` - Final USGS report

## File Path References

All scripts have been updated to use the new directory structure:
- Data files are saved to `../data/usgs/` relative to the scripts
- Documentation files are in `../docs/usgs/`
- Test files are in `../tests/`

## Usage

To run data collection:
```bash
cd grip-backend
source venv/bin/activate
python src/data_collectors/usgs/collect_comprehensive_data.py
```

To clean country names:
```bash
cd grip-backend
source venv/bin/activate
python src/data_collectors/usgs/country_cleaner.py
```