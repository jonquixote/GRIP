# GRIP - Global Resource Intelligence Platform

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

GRIP (Global Resource Intelligence Platform) is a comprehensive resource intelligence platform that collects, processes, and analyzes data from authoritative sources like the USGS (United States Geological Survey) and FRED (Federal Reserve Economic Data). The platform provides real-time insights into global mineral resources and commodity markets.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Technologies](#technologies)
- [Setup](#setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Overview

GRIP aims to transform global resource intelligence from reactive historical analysis to proactive strategic advantage by providing:

- Real-time global resource pulse monitoring
- AI-powered predictive forecasting
- Automated supply chain risk assessment
- Data integration across 400+ authoritative sources
- Transparency through data validation and quality control

## Architecture

GRIP follows a modern full-stack architecture:

```
┌─────────────────┐    ┌──────────────────┐
│   Frontend      │    │   Backend        │
│   (React/Vite)  │◄──►│   (Python/Flask) │
└─────────────────┘    └──────────────────┘
                              │
                              ▼
                       ┌─────────────┐
                       │   SQLite    │
                       │  Database   │
                       └─────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Data Sources     │
                    │ - USGS           │
                    │ - FRED           │
                    │ - ...            │
                    └──────────────────┘
```

## Features

- **Data Collection**: Automated collection from USGS and FRED APIs
- **Data Processing**: PDF parsing, data validation, and quality control
- **API**: RESTful API for data access and management
- **Visualization**: Interactive charts and dashboards
- **Analytics**: Business intelligence and predictive modeling
- **Historical Data**: Support for historical data going back to 1900
- **Responsive UI**: Mobile-friendly interface with dark mode support

## Technologies

### Backend
- Python 3.8+
- Flask web framework
- SQLAlchemy ORM
- SQLite database
- Pandas for data processing
- pdfplumber for PDF parsing
- BeautifulSoup4 for web scraping
- fredapi for FRED API access

### Frontend
- React 18+
- Vite build tool
- Tailwind CSS for styling
- Radix UI components
- Chart.js and Recharts for data visualization
- React Router for navigation
- Axios for HTTP requests

## Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd grip-backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   export FRED_API_KEY=your_fred_api_key
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd grip-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Usage

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

### Collecting Data

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

## Project Structure

```
GRIP/
├── grip-backend/
│   ├── src/
│   │   ├── data_collectors/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── analytics/
│   │   └── main.py
│   ├── data/
│   ├── docs/
│   ├── tests/
│   └── requirements.txt
├── grip-frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── utils/
│   ├── public/
│   └── package.json
└── docs/
```

## Development

### Backend Development

#### Running Tests
```bash
cd grip-backend
python -m pytest tests/
```

#### Linting
```bash
cd grip-backend
flake8 src/
```

### Frontend Development

#### Running Tests
```bash
cd grip-frontend
npm run test
```

#### Linting
```bash
cd grip-frontend
npm run lint
```

## Contributing

We welcome contributions to GRIP! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more information.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Future Vision (GAIA)

GRIP is evolving toward GAIA (Global Automated Intelligence Architecture), which aims to:

- Provide real-time global resource pulse monitoring
- Implement AI-powered predictive forecasting with 99.7% accuracy
- Enable autonomous supply chain risk assessment
- Integrate data from 500+ sources
- Offer blockchain-verified transparency