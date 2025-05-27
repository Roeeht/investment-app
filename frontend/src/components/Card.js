import React, { useEffect, useState } from "react";
import axios from "axios";

const Card = () => {
  const [added, setAdded] = useState(false);
  const [stock, setStock] = useState({});
  const [title, setTitle] = useState("");

  useEffect(() => {
    console.log(`Has ${title} been added? ${added}`);
  }, [title, added]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/api/stock?symbol=AAPL")
      //change symbol to index instead of stock
      .then((response) => {
        setStock(response);
        setTitle(response?.data?.[0]?.name);
        console.log(response);
      });
  }, []);

  return (
    <div className="card">
      <h1>{title}</h1>
      <h2>Stock : {JSON.stringify(stock?.data?.[0]?.name || "Loading...")} </h2>
      <button className="button" onClick={() => setAdded(!added)}>
        {added ? "added" : "not added"}
      </button>
    </div>
  );
};

export default Card;
