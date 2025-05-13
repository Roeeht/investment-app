import React, { useEffect, useState } from "react";
import axios from "axios";

const Card = ({ title }) => {
  const [added, setAdded] = useState(false);
  const [stock, setStock] = useState({});

  useEffect(() => {
    console.log(`Has ${title} been added? ${added}`);
  }, [title, added]);

  useEffect(() => {
    axios
      .get(
        "https://financialmodelingprep.com/stable/quote?symbol=^GSPC&apikey=4cDgO8QI4anGo1puGjCsXj0xRS62Tiyd"
      )
      .then((response) => {
        setStock(response);
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

function App() {
  const [title, setTitle] = useState("");

  return (
    <div className="card-container">
      <h1>{title}</h1>
      <Card title="s&p500" />
    </div>
  );
}

export default App;
