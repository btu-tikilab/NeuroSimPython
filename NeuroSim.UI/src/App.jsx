import React, { useState } from 'react';
import Sidebar from './components/Sidebar/Sidebar';
import Home from './Pages/Home/Home';
import Wiki from "./Pages/Wiki/Wiki";
import BitGA from "./Pages/BitGA/BitGA";
import GraphGA from "./Pages/GraphGA/GraphGA";
import TSP from "./Pages/TSP/TSP";
import MazeNet from "./Pages/MazeNet/MazeNet";
import './App.css';

export default function App() {
  const [activeItem, setActiveItem] = useState("Home");
  const [theme, setTheme] = useState("dark");
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div
      className={`app-layout ${
        theme === "dark"
          ? "app-layout--dark"
          : "app-layout--light"
      }`}
    >
      <Sidebar
        activeItem={activeItem}
        onNavigate={setActiveItem}
        theme={theme}
        setTheme={setTheme}
        collapsed={collapsed}
        setCollapsed={setCollapsed}
      />

      {activeItem === "Home" && (
        <Home onNavigate={setActiveItem} />
      )}

      {activeItem === "Wiki" && (
        <Wiki onNavigate={setActiveItem} />
      )}

      {activeItem === "BitGA" && <BitGA />}
      {activeItem === "GraphGA" && <GraphGA />}
      {activeItem === "TSP" && <TSP onNavigate={setActiveItem} />}
      {activeItem === "MazeNet" && <MazeNet onNavigate={setActiveItem} />}
      {activeItem === "GA" && <Wiki onNavigate={setActiveItem} initialSection="ga" />}
      {activeItem === "GP" && <Wiki onNavigate={setActiveItem} initialSection="gp" />}
      {activeItem === "ES" && <Wiki onNavigate={setActiveItem} initialSection="es" />}
      {activeItem === "EP" && <Wiki onNavigate={setActiveItem} initialSection="ep" />}
    </div>
  );
}