import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          GRIP Dashboard
        </Link>
        <ul className="nav-menu">
          <li className="nav-item">
            <Link to="/" className="nav-link">
              Commodities
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/commodities/new" className="nav-link">
              Add Commodity
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;