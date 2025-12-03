import React from "react";
import Navigation from "./components/common/Navigation";
import Dashboard from "./pages/Dashboard";
import "./style/index.css";

function App() {
  return (
    <div className="app">
      <Navigation />
      <main className="main-content">
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
