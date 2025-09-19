import React, { useState, useEffect } from 'react';

const ApiTest = () => {
  const [testResult, setTestResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const testApiConnection = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/health');
      const data = await response.json();
      setTestResult({ success: true, data, status: response.status });
    } catch (error) {
      setTestResult({ success: false, error: error.message });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    testApiConnection();
  }, []);

  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4">API Connection Test</h2>
      {loading && <p>Testing connection...</p>}
      {testResult && (
        <div>
          <p className={`font-semibold ${testResult.success ? 'text-green-600' : 'text-red-600'}`}>
            Status: {testResult.success ? 'Success' : 'Failed'}
          </p>
          {testResult.success ? (
            <div>
              <p>Status Code: {testResult.status}</p>
              <pre className="bg-gray-100 p-2 mt-2 rounded">
                {JSON.stringify(testResult.data, null, 2)}
              </pre>
            </div>
          ) : (
            <p>Error: {testResult.error}</p>
          )}
        </div>
      )}
      <button 
        onClick={testApiConnection}
        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Retest Connection
      </button>
    </div>
  );
};

export default ApiTest;