import React from "react";

const Navigation = () => {
  return (
    <nav className="navigation">
      <div className="nav-brand">
        <h1>Investment App</h1>
      </div>
      <ul className="nav-links">
        <li>
          <a href="/">Dashboard</a>
        </li>
        <li>
          <a href="/portfolio">Portfolio</a>
        </li>
        <li>
          <a href="/stocks">Stocks</a>
        </li>
        <li>
          <a href="/transactions">Transactions</a>
        </li>
      </ul>
      <div className="nav-auth">
        <button className="btn-login">Login</button>
        <button className="btn-register">Register</button>
      </div>
    </nav>
  );
};

export default Navigation;
