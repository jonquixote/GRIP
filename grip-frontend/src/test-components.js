// Test file to verify all components can be imported
console.log('Testing component imports...');

try {
  import('../components/Dashboard.jsx');
  console.log('✓ Dashboard imported successfully');
} catch (error) {
  console.error('✗ Error importing Dashboard:', error);
}

try {
  import('../components/MarketTrends.jsx');
  console.log('✓ MarketTrends imported successfully');
} catch (error) {
  console.error('✗ Error importing MarketTrends:', error);
}

try {
  import('../components/AnalyticsPanel.jsx');
  console.log('✓ AnalyticsPanel imported successfully');
} catch (error) {
  console.error('✗ Error importing AnalyticsPanel:', error);
}

try {
  import('../components/PredictionsPanel.jsx');
  console.log('✓ PredictionsPanel imported successfully');
} catch (error) {
  console.error('✗ Error importing PredictionsPanel:', error);
}

try {
  import('../components/DataIngestionPanel.jsx');
  console.log('✓ DataIngestionPanel imported successfully');
} catch (error) {
  console.error('✗ Error importing DataIngestionPanel:', error);
}

console.log('Component import test completed.');