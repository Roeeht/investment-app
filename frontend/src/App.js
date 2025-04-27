import React, { useEffect, useState } from "react";
import axios from "axios";

const Card = ({ title }) => {
  const [added, setAdded] = useState(false);
  useEffect(() => {
    console.log(`${title} has been ${added}`);
  }, [added]);

  return (
    <div className='card'>
      <h1>{title}</h1>
      <button onClick={() => setAdded(!added)}>
        {added ? "added" : "not added"}
      </button>
    </div>
  );
};

function App() {
  const [title, setTitle] = useState("");
  useEffect(() => {
    axios.get("http://127.0.0.1:8000/").then((response) => {
      setTitle(response.data.message);
    });
  }, []);

  return (
    <div className='card-container'>
      <h1>{title}</h1>
      <Card title='Stock Name1' />
      <Card title='Stock Name2' />
      <Card title='Stock Name3' />
      <Card title='Stock Name4' />
    </div>
  );
}

export default App;
