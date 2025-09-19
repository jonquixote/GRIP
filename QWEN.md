# GRIP (Global Resource Intelligence Platform) - Project Context

## Project Overview

GRIP is a comprehensive resource intelligence platform that collects, processes, and analyzes data from authoritative sources like the USGS (United States Geological Survey) and FRED (Federal Reserve Economic Data). The platform aims to provide real-time insights into global mineral resources and commodity markets.

The project consists of a Python/Flask backend and a React/Vite frontend, with a SQLite database for local development.

## Architecture

### Backend (grip-backend)
- **Framework**: Python/Flask
- **Database**: SQLite (with SQLAlchemy ORM)
- **Key Components**:
  - Data collectors for USGS and FRED APIs
  - RESTful API endpoints for commodities, countries, data points, and analytics
  - Data models for commodities, countries, production data, reserves data, and price data

### Frontend (grip-frontend)
- **Framework**: React with Vite
- **UI Library**: Tailwind CSS with Radix UI components
- **Charting**: Chart.js and Recharts
- **Routing**: React Router
- **API Client**: Axios

## Key Technologies

### Backend Dependencies
- Flask (web framework)
- SQLAlchemy (ORM)
- Requests (HTTP library)
- Pandas (data processing)
- pdfplumber (PDF parsing)
- BeautifulSoup4 (HTML parsing)
- fredapi (FRED API client)

### Frontend Dependencies
- React 18+
- Vite (build tool)
- Tailwind CSS (styling)
- Radix UI (accessible UI components)
- Chart.js & Recharts (data visualization)
- Lucide React (icons)

## Setup and Configuration

### Environment Variables
The project requires the following environment variables:
- `FRED_API_KEY`: API key for accessing FRED data

### Backend Setup
1. Install Python dependencies:
   ```bash
   pip install -r grip-backend/requirements.txt
   ```
2. Set up environment variables:
   ```bash
   export FRED_API_KEY=your_fred_api_key
   ```

### Frontend Setup
1. Install Node.js dependencies:
   ```bash
   cd grip-frontend
   npm install
   ```

## Development Workflow

### Running the Backend
```bash
cd grip-backend
python3 src/main.py
```

### Running the Frontend
```bash
cd grip-frontend
npm run dev
```

### Data Collection

#### FRED Data Collection
```bash
cd grip-backend
python3 collect_fred_data.py
```

#### USGS Data Collection
```bash
cd grip-backend
python3 src/main.py collect-usgs
```

## API Endpoints

### Backend API Routes
- `/api/commodities` - Commodity management
- `/api/countries` - Country data
- `/api/data` - Data points (production, reserves, prices)
- `/api/analytics` - Analysis functions
- `/api/predictions` - Predictive models
- `/api/collection` - Data collection endpoints

## Testing

### Backend Testing
```bash
cd grip-backend
python -m pytest tests/
```

### Backend Linting
```bash
cd grip-backend
flake8 src/
```

## Data Models

### Core Entities
1. **Commodity** - Represents a mineral commodity
2. **Country** - Represents a country with resource data
3. **ProductionData** - Production volume data
4. **ReservesData** - Reserves volume data
5. **PriceData** - Price data points
6. **DataSource** - Information about data sources

## Development Conventions

### Backend
- Follow PEP 8 Python style guide
- Use SQLAlchemy for database operations
- Implement proper error handling and logging
- Use Flask blueprints for organizing routes

### Frontend
- Use functional components with React hooks
- Follow Tailwind CSS utility-first approach
- Use TypeScript for type safety
- Organize components in a logical folder structure

## Project Structure

```
GRIP/
├── grip-backend/
│   ├── src/
│   │   ├── data_collectors/
│   │   ├── models/
│   │   ├── routes/
│   │   └── main.py
│   ├── tests/
│   ├── data/
│   └── docs/
├── grip-frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── utils/
│   └── public/
└── docs/
```

## Data Collection Process

### USGS Collector
- Collects mineral commodity data from USGS reports
- Supports historical data collection going back to 1900
- Parses PDF documents to extract production and reserves data
- Handles various commodity types (copper, gold, silver, aluminum, etc.)

### FRED Collector
- Collects commodity price data and economic indicators
- Uses the FRED API for data access
- Tracks base metals, energy commodities, and other resources
- Organizes data by commodity type with metadata

## Future Vision (GAIA)
The project is evolving toward GAIA (Global Automated Intelligence Architecture), which aims to:
- Provide real-time global resource pulse monitoring
- Implement AI-powered predictive forecasting
- Enable autonomous supply chain risk assessment
- Integrate data from 500+ sources
- Offer blockchain-verified transparency