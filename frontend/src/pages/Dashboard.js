import React from "react";
import StockCard from "../components/stocks/StockCard";

const Dashboard = () => {
  return (
    <div className="dashboard">
      <h1>Investment Dashboard</h1>
      <div className="dashboard-content">
        <section className="stock-overview">
          <h2>Featured Stocks</h2>
          <div className="stock-grid">
            <StockCard symbol="AAPL" />
            <StockCard symbol="GOOGL" />
            <StockCard symbol="TSLA" />
          </div>
        </section>

        <section className="portfolio-summary">
          <h2>Portfolio Summary</h2>
          <div className="summary-card">
            <p>Total Value: $0.00</p>
            <p>Today's Change: $0.00 (0%)</p>
            <p>Cash Balance: $0.00</p>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Dashboard;
