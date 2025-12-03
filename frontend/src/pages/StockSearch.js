import React, { useState } from "react";
import StockCard from "../components/stocks/StockCard";

const StockSearch = () => {
  const [searchSymbol, setSearchSymbol] = useState("");
  const [searchedStock, setSearchedStock] = useState(null);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchSymbol.trim()) {
      setSearchedStock(searchSymbol.toUpperCase());
    }
  };

  return (
    <div className="stock-search">
      <h1>Search Stocks</h1>

      <form onSubmit={handleSearch} className="search-form">
        <div className="search-input-group">
          <input
            type="text"
            placeholder="Enter stock symbol (e.g., AAPL, GOOGL)"
            value={searchSymbol}
            onChange={(e) => setSearchSymbol(e.target.value)}
            className="search-input"
          />
          <button type="submit" className="search-button">
            Search
          </button>
        </div>
      </form>

      {searchedStock && (
        <div className="search-results">
          <h2>Search Results</h2>
          <StockCard symbol={searchedStock} />
        </div>
      )}

      <div className="popular-stocks">
        <h2>Popular Stocks</h2>
        <div className="stock-grid">
          <StockCard symbol="AAPL" />
          <StockCard symbol="GOOGL" />
          <StockCard symbol="MSFT" />
          <StockCard symbol="TSLA" />
          <StockCard symbol="AMZN" />
          <StockCard symbol="NVDA" />
        </div>
      </div>
    </div>
  );
};

export default StockSearch;
