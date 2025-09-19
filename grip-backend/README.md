# GRIP Backend

The backend for the Global Resource Intelligence Platform (GRIP) is a Python/Flask application that collects and processes data from authoritative sources like the USGS and FRED.

## Technologies

- **Framework**: Python/Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Data Processing**: Pandas, pdfplumber
- **API Client**: requests, fredapi
- **Task Scheduling**: schedule

## Directory Structure

```
grip-backend/
├── src/
│   ├── data_collectors/
│   │   ├── fred/
│   │   ├── usgs/
│   │   ├── fred_collector.py
│   │   ├── usgs_collector.py
│   │   └── base_collector.py
│   ├── models/
│   ├── routes/
│   ├── analytics/
│   └── main.py
├── data/
│   ├── fred/
│   └── usgs/
├── docs/
├── tests/
└── requirements.txt
```

## Data Collectors

### FRED Collector
Collects commodity price data and economic indicators from the Federal Reserve Economic Data (FRED) API.

See [FRED Collector Documentation](src/data_collectors/README_FRED.md) for detailed information.

### USGS Collector
Collects mineral commodity data from the United States Geological Survey reports. Supports historical data collection going back to 1900 and parses PDF documents to extract production and reserves data.

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   export FRED_API_KEY=your_fred_api_key
   export DATABASE_URL=your_database_url
   ```

## Usage

### Start the Application
```bash
python3 src/main.py
```

### Collect FRED Data
```bash
python3 collect_fred_data.py
```

### Collect USGS Data
```bash
python3 src/main.py collect-usgs
```

## API Endpoints

- `/api/commodities` - Commodity management
- `/api/countries` - Country data
- `/api/data` - Data points (production, reserves, prices)
- `/api/analytics` - Analysis functions
- `/api/predictions` - Predictive models
- `/api/collection` - Data collection endpoints

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Linting
```bash
flake8 src/
```

## Data Models

- **Commodity** - Represents a mineral commodity
- **Country** - Represents a country with resource data
- **ProductionData** - Production volume data
- **ReservesData** - Reserves volume data
- **PriceData** - Price data points
- **DataSource** - Information about data sources
- **APIKey** - API key management

## Architecture

The backend follows a modular architecture with clear separation of concerns:

- **Data Collectors**: Responsible for fetching data from external sources
- **Models**: Database models using SQLAlchemy ORM
- **Routes**: API endpoints organized by resource type
- **Analytics**: Business logic for data analysis and processing
- **Database**: SQLite database with SQLAlchemy ORM

## Features

- Automated data collection from USGS and FRED
- RESTful API for data access
- Historical data support
- PDF parsing capabilities
- Data validation and quality control
- Scheduled data collection tasks