import { Link } from "react-router-dom";
import "./Navbar.css"; // Importing the CSS file for styling

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <h1>Make it Yourself</h1>
      </div>
      <ul className="navbar-links">
        <li>
          <Link to="/home" className="nav-link">
            Home
          </Link>
        </li>
        <li>
          <Link to="/build" className="nav-link">
            Build
          </Link>
        </li>
        <li>
          <Link to="/test" className="nav-link">
            Test
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
