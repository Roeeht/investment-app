import React, { useEffect, useState } from "react";
import { stockAPI } from "../../services/api";

const StockCard = ({ symbol }) => {
  const [loading, setLoading] = useState(true);
  const [stock, setStock] = useState(null);
  const [error, setError] = useState(null);
  const [isInPortfolio, setIsInPortfolio] = useState(false);

  useEffect(() => {
    const fetchStock = async () => {
      try {
        setLoading(true);
        const response = await stockAPI.getStock(symbol);
        setStock(response.data[0]); // Based on your current API response structure
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error("Error fetching stock:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchStock();
  }, [symbol]);

  const handleAddToPortfolio = () => {
    setIsInPortfolio(!isInPortfolio);
    // TODO: Implement actual add to portfolio API call
  };

  if (loading) return <div className="card">Loading...</div>;
  if (error) return <div className="card error">Error: {error}</div>;
  if (!stock) return <div className="card">No stock data found</div>;

  return (
    <div className="card">
      <h2>{stock.name}</h2>
      <p>
        <strong>Symbol:</strong> {stock.symbol}
      </p>
      <p>
        <strong>Price:</strong> ${stock.price?.toFixed(2) || "N/A"}
      </p>
      <p>
        <strong>Change:</strong> {stock.change || "N/A"}
      </p>
      <button
        className={`button ${isInPortfolio ? "added" : ""}`}
        onClick={handleAddToPortfolio}
      >
        {isInPortfolio ? "In Portfolio" : "Add to Portfolio"}
      </button>
    </div>
  );
};

export default StockCard;
