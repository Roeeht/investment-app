import React, { useEffect, useState } from "react";
import axios from "axios";

const Card = ({ title }) => {
  return (
    <div className='card'>
      <h1>{title}</h1>
      <button></button>
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
      <Card title='Hi' />
    </div>
  );
}

export default App;
