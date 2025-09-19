// Mock data service for testing when backend is not available
const mockCommodities = [
  { id: 1, name: 'Copper', symbol: 'COP', category: 'base metal' },
  { id: 2, name: 'Gold', symbol: 'GOLD', category: 'precious metal' },
  { id: 3, name: 'Lithium', symbol: 'LIT', category: 'critical metal' },
  { id: 4, name: 'Iron Ore', symbol: 'IRO', category: 'base metal' },
  { id: 5, name: 'Silver', symbol: 'SIL', category: 'precious metal' },
  { id: 6, name: 'Nickel', symbol: 'NIC', category: 'base metal' },
  { id: 7, name: 'Cobalt', symbol: 'COB', category: 'critical metal' },
  { id: 8, name: 'Platinum', symbol: 'PLA', category: 'precious metal' },
  { id: 9, name: 'Palladium', symbol: 'PAL', category: 'precious metal' },
  { id: 10, name: 'Zinc', symbol: 'ZIN', category: 'base metal' }
];

const mockMarketData = {
  total_commodities: 10,
  market_summary: {
    positive_outlook: 6,
    high_risk_commodities: 3,
    market_sentiment: 'Bullish'
  },
  risk_alerts: [
    "Copper supply disruption in Chile",
    "Lithium price volatility in Australia",
    "Gold reserves declining in South Africa"
  ]
};

export const mockDataService = {
  getCommodities: () => Promise.resolve({ data: mockCommodities }),
  getMarketOverview: () => Promise.resolve({ data: mockMarketData })
};