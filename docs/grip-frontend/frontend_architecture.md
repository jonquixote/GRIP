# GRIP Frontend Architecture

## Overview

The Global Resource Intelligence Platform (GRIP) frontend is a modern, responsive dashboard application built with React and Vite. It provides an intuitive interface for visualizing global mineral resource data, market trends, and predictive analytics. The application features a sleek dark theme with vibrant accent colors and smooth animations.

## Main Pages and Components

### Dashboard (Main Page)

The dashboard serves as the primary interface and is organized into several key sections:

1. **Header Section**
   - Platform title with branding
   - Live data indicator
   - Manual refresh button

2. **Key Metrics Cards**
   - Total Commodities Tracked: Shows the number of commodities being monitored
   - Positive Outlook: Number of commodities with bullish trends
   - High Risk: Commodities requiring attention due to market volatility or supply issues
   - Market Sentiment: Overall market mood (Bullish/Bearish/Mixed)

3. **Risk Alerts Panel**
   - Displays critical alerts about supply disruptions, geopolitical tensions, or market volatility

4. **Tabbed Navigation**
   The dashboard features four main tabs for different types of analysis:

   **a. Overview Tab**
   - Interactive grid of all tracked commodities
   - Filtering and search capabilities
   - Quick access to detailed commodity information

   **b. Analytics Tab**
   - Data visualization panels with multiple chart types:
     * Bar charts for production volumes by commodity
     * Line charts for historical price trends
     * Pie charts for reserve distribution by region
   - Time range selectors (7 days, 30 days, 90 days, 1 year, all time)
   - Chart type selection
   - Export functionality
   - Key market insights with trend indicators

   **c. Predictions Tab**
   - AI-powered forecasts for commodity prices and production
   - Confidence scoring for predictions
   - Model performance metrics
   - Forecast visualization with trend lines

   **d. Trends Tab**
   - Regional market analysis
   - Global trend visualization
   - Volatility indicators
   - Supply chain risk assessments

### Layout Components

1. **Sidebar Navigation**
   - Collapsible navigation menu
   - Links to main sections of the application
   - Dark/light mode toggle
   - User profile access

2. **Header Bar**
   - Top-level navigation controls
   - Search functionality
   - Notification indicators
   - User settings access

## Frontend Technical Architecture

- **Framework**: React 18 with Vite for fast development
- **Styling**: Tailwind CSS with custom dark theme
- **UI Components**: Shadcn UI components for consistent design
- **Charts**: Chart.js with react-chartjs-2 for data visualization
- **Icons**: Lucide React for consistent iconography
- **State Management**: React hooks and context API
- **Performance**: 
  - Skeleton loaders for improved perceived performance
  - Memoized components to reduce unnecessary re-renders
  - Optimized data filtering and search functions

## Backend Interaction

The frontend communicates with the backend through a RESTful API built with Flask. All data exchanges use JSON format over HTTP/HTTPS.

### API Endpoints Used

1. **Commodity Data**
   - `GET /api/commodities` - Retrieve all commodities
   - `GET /api/commodities/{id}` - Get specific commodity details

2. **Analytics Services**
   - `GET /api/analytics/market-overview` - Get overall market analysis
   - `GET /api/analytics/commodity/{id}` - Analyze a specific commodity
   - `GET /api/analytics/commodity/{id}/price` - Get price analysis for a commodity
   - `GET /api/analytics/commodity/{id}/production` - Get production analysis for a commodity
   - `GET /api/analytics/commodity/{id}/ml` - Get machine learning analysis for a commodity
   - `GET /api/analytics/predict/{id}` - Get predictions for a commodity
   - `GET /api/analytics/trends` - Get current market trends

3. **Data Management**
   - `POST /api/commodities` - Create new commodity entries
   - `PUT /api/commodities/{id}` - Update existing commodities
   - `DELETE /api/commodities/{id}` - Remove commodities

### Data Flow

1. **Initial Load**: When the dashboard loads, it makes API calls to fetch:
   - Market overview data
   - List of tracked commodities
   - Initial analytics data

2. **User Interaction**: As users navigate between tabs or adjust filters:
   - Additional API calls are made to fetch specific data subsets
   - Chart components update with new data
   - UI components re-render with fresh information

3. **Real-time Updates**: 
   - Users can manually refresh data using the refresh button
   - Risk alerts are periodically updated
   - Market trends are regularly refreshed

### Error Handling

The frontend implements comprehensive error handling:
- Network error detection and user-friendly error messages
- Loading states with skeleton screens during data fetch
- Fallback UI components when data is unavailable
- Retry mechanisms for failed API calls

## Responsive Design

The application is fully responsive and works across all device sizes:
- Mobile-first design approach
- Adaptive grid layouts that adjust based on screen size
- Touch-friendly controls and navigation elements
- Optimized data visualization for smaller screens
- Collapsible sidebar on mobile devices

## Performance Considerations

- Lazy loading of components where appropriate
- Memoization of expensive calculations and components
- Skeleton loaders for improved perceived performance
- Optimized rendering with React.memo
- Efficient data fetching with minimal API calls