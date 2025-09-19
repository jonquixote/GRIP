import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { commodityService } from '../services/api';
import './CommodityList.css';

const CommodityList = () => {
  const [commodities, setCommodities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCommodities();
  }, []);

  const fetchCommodities = async () => {
    try {
      setLoading(true);
      const response = await commodityService.getAll();
      setCommodities(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch commodities');
      console.error('Error fetching commodities:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await commodityService.delete(id);
      // Remove the deleted commodity from the state
      setCommodities(commodities.filter(commodity => commodity.id !== id));
    } catch (err) {
      setError('Failed to delete commodity');
      console.error('Error deleting commodity:', err);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="commodity-list">
      <div className="header">
        <h2>Commodities</h2>
        <Link to="/commodities/new" className="btn btn-primary">
          Add New Commodity
        </Link>
      </div>
      
      {commodities.length === 0 ? (
        <p>No commodities found.</p>
      ) : (
        <table className="commodities-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Symbol</th>
              <th>Category</th>
              <th>Strategic Importance</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {commodities.map(commodity => (
              <tr key={commodity.id}>
                <td>{commodity.name}</td>
                <td>{commodity.symbol}</td>
                <td>{commodity.category}</td>
                <td>{commodity.strategic_importance || 'N/A'}</td>
                <td>
                  <Link to={`/commodities/${commodity.id}/edit`} className="btn btn-secondary">
                    Edit
                  </Link>
                  <button 
                    onClick={() => handleDelete(commodity.id)} 
                    className="btn btn-danger"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default CommodityList;