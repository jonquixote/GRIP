import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { commodityService } from '../services/api';
import './CommodityForm.css';

const CommodityForm = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  
  const [formData, setFormData] = useState({
    name: '',
    symbol: '',
    category: '',
    strategic_importance: ''
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (id) {
      fetchCommodity(id);
    }
  }, [id]);

  const fetchCommodity = async (commodityId) => {
    try {
      setLoading(true);
      const response = await commodityService.getById(commodityId);
      // Convert strategic_importance to string for the form
      const commodityData = {
        ...response.data,
        strategic_importance: response.data.strategic_importance?.toString() || ''
      };
      setFormData(commodityData);
    } catch (err) {
      setError('Failed to fetch commodity');
      console.error('Error fetching commodity:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      setError(null);
      
      // Convert strategic_importance to integer if provided
      const dataToSubmit = {
        ...formData,
        strategic_importance: formData.strategic_importance ? parseInt(formData.strategic_importance, 10) : null
      };
      
      if (id) {
        // Update existing commodity
        await commodityService.update(id, dataToSubmit);
      } else {
        // Create new commodity
        await commodityService.create(dataToSubmit);
      }
      
      // Redirect to commodities list
      navigate('/commodities');
    } catch (err) {
      setError('Failed to save commodity');
      console.error('Error saving commodity:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading && id) return <div className="loading">Loading...</div>;

  return (
    <div className="commodity-form">
      <h2>{id ? 'Edit Commodity' : 'Add New Commodity'}</h2>
      
      {error && <div className="error">Error: {error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="symbol">Symbol:</label>
          <input
            type="text"
            id="symbol"
            name="symbol"
            value={formData.symbol}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="category">Category:</label>
          <input
            type="text"
            id="category"
            name="category"
            value={formData.category}
            onChange={handleChange}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="strategic_importance">Strategic Importance (1-10):</label>
          <input
            type="number"
            id="strategic_importance"
            name="strategic_importance"
            value={formData.strategic_importance}
            onChange={handleChange}
            min="1"
            max="10"
          />
        </div>
        
        <div className="form-actions">
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Saving...' : 'Save Commodity'}
          </button>
          <button 
            type="button" 
            className="btn btn-secondary" 
            onClick={() => navigate('/commodities')}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default CommodityForm;