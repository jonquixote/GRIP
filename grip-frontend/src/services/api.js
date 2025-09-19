import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const commodityService = {
  // Get all commodities
  getAll: () => api.get('/commodities'),
  
  // Get a specific commodity by ID
  getById: (id) => api.get(`/commodities/${id}`),
  
  // Create a new commodity
  create: (commodity) => api.post('/commodities', commodity),
  
  // Update an existing commodity
  update: (id, commodity) => api.put(`/commodities/${id}`, commodity),
  
  // Delete a commodity
  delete: (id) => api.delete(`/commodities/${id}`),
};

export const dataIngestionService = {
  // Ingest data from files
  ingestFiles: (data) => api.post('/ingest/files', data),
  
  // Get ingestion status
  getStatus: () => api.get('/ingest/status'),
};

export const analyticsService = {
  // Get commodity overview
  getCommodityOverview: (params) => api.get('/analytics/commodity-overview', { params }),
  
  // Get country overview
  getCountryOverview: (params) => api.get('/analytics/country-overview', { params }),
  
  // Get market dashboard
  getMarketDashboard: (params) => api.get('/analytics/market-dashboard', { params }),
  
  // Get supply risk assessment
  getSupplyRiskAssessment: (params) => api.get('/analytics/supply-risk', { params }),
  
  // Get time series data
  getTimeSeriesData: (params) => api.get('/analytics/time-series', { params }),
};

export default api;