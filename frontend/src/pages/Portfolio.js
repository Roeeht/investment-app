import React from "react";

const Portfolio = () => {
  return (
    <div className="portfolio">
      <h1>My Portfolio</h1>
      <div className="portfolio-content">
        <div className="portfolio-summary">
          <div className="summary-card">
            <h3>Portfolio Summary</h3>
            <p>
              <strong>Total Value:</strong> $0.00
            </p>
            <p>
              <strong>Today's Change:</strong> $0.00 (0%)
            </p>
            <p>
              <strong>Total Gain/Loss:</strong> $0.00 (0%)
            </p>
          </div>
        </div>

        <div className="holdings">
          <h2>Your Holdings</h2>
          <div className="holdings-list">
            <p>
              No stocks in portfolio yet. Start by searching for stocks to buy!
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Portfolio;
