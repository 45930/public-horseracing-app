import React from "react";
import { Link } from "react-router-dom";

class Header extends React.Component {
  render() {
    return (
      <div className="ui secondary grey inverted menu">
        <Link className="item" to="/">
          Home
        </Link>
        <Link className="item" to="/explore">
          Explore
        </Link>
        <Link className="item" to="/results">
          Results
        </Link>
        <Link className="item" to="/search">
          Search
        </Link>
        <Link className="item" to="/simulcast">
          Simulcast
        </Link>
        <Link className="item" to="/scratches">
          Enter Scratches
        </Link>
      </div>
    );
  }
}

export default Header;
