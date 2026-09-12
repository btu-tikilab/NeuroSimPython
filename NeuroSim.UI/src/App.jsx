import React, { useState } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Sidebar from "./components/Sidebar/Sidebar";
import Home from "./Pages/Home/Home";
import Wiki from "./Pages/Wiki/Wiki";
import BitGA from "./Pages/BitGA/BitGA";
import GraphGA from "./Pages/GraphGA/GraphGA";
import TSP from "./Pages/TSP/TSP";
import MazeNet from "./Pages/MazeNet/MazeNet";

import "./App.css";

export default function App() {
  const [theme, setTheme] = useState("dark");
  const [collapsed, setCollapsed] = useState(false);

  return (
    <BrowserRouter>
      <AppContent
        theme={theme}
        setTheme={setTheme}
        collapsed={collapsed}
        setCollapsed={setCollapsed}
      />
    </BrowserRouter>
  );
}

function AppContent({
  theme,
  setTheme,
  collapsed,
  setCollapsed,
}) {
  return (
    <div
      className={`app-layout ${
        theme === "dark"
          ? "app-layout--dark"
          : "app-layout--light"
      }`}
    >
      <Sidebar
        theme={theme}
        setTheme={setTheme}
        collapsed={collapsed}
        setCollapsed={setCollapsed}
      />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/wiki" element={<Wiki />} />
        <Route path="/bitga" element={<BitGA />} />
        <Route path="/graphga" element={<GraphGA />} />
        <Route path="/tsp" element={<TSP />} />
        <Route path="/maznet" element={<MazeNet />} />

        <Route
          path="/ga"
          element={<Wiki initialSection="ga" />}
        />
        <Route
          path="/gp"
          element={<Wiki initialSection="gp" />}
        />
        <Route
          path="/es"
          element={<Wiki initialSection="es" />}
        />
        <Route
          path="/ep"
          element={<Wiki initialSection="ep" />}
        />

        <Route
          path="*"
          element={<Navigate to="/" replace />}
        />
      </Routes>
    </div>
  );
}