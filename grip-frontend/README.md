# GRIP Frontend

The frontend for the Global Resource Intelligence Platform (GRIP) is a modern React application built with Vite that provides a dashboard for visualizing and analyzing global resource data.

## Technologies

- **Framework**: React 18+
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI, Lucide React Icons
- **Charts**: Chart.js, Recharts
- **Routing**: React Router
- **API Client**: Axios

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Build for production:
   ```bash
   npm run build
   ```

## Development

### Running the Development Server
```bash
npm run dev
```
This starts the Vite development server with hot module replacement.

### Building for Production
```bash
npm run build
```
This creates an optimized production build in the `dist/` directory.

### Linting
```bash
npm run lint
```
Runs ESLint to check for code quality issues.

## Project Structure

```
grip-frontend/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/          # Page components
│   ├── hooks/          # Custom React hooks
│   ├── utils/          # Utility functions
│   ├── services/       # API service clients
│   ├── assets/         # Static assets
│   └── App.jsx         # Main application component
├── public/             # Static assets
├── index.html          # Main HTML file
└── vite.config.js      # Vite configuration
```

## Architecture

The frontend follows a component-based architecture with clear separation of concerns:

- **Components**: Reusable UI elements
- **Pages**: Top-level views that compose components
- **Services**: API clients for communicating with the backend
- **Hooks**: Custom React hooks for state and logic
- **Utils**: Helper functions and utilities

## Features

- Real-time visualization of commodity data
- Interactive charts and graphs
- Data filtering and search capabilities
- Responsive design for all device sizes
- Dark mode support