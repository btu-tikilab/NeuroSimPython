import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./Sidebar.css";

import {
  FaHome,
  FaBookOpen,
  FaProjectDiagram,
  FaRoute,
  FaDna,
  FaCodeBranch,
  FaBrain,
  FaInfoCircle,
  FaMoon,
  FaSun,
} from "react-icons/fa";

import { FaSquareBinary } from "react-icons/fa6";
import { GiMaze, GiDiceTarget } from "react-icons/gi";
import { SlGraph } from "react-icons/sl";

const navItems = [
  {
    label: "Home",
    path: "/",
    icon: <FaHome />,
  },
  {
    label: "Wiki",
    path: "/wiki",
    icon: <FaBookOpen />,
  },
];

const playgrounds = [
  {
    label: "BitGA",
    path: "/bitga",
    icon: <FaSquareBinary />,
  },
  {
    label: "GraphGA",
    path: "/graphga",
    icon: <FaProjectDiagram />,
  },
  {
    label: "TSP",
    path: "/tsp",
    icon: <FaRoute />,
  },
  {
    label: "MazeNet",
    path: "/maznet",
    icon: <GiMaze />,
  },
];

const paradigms = [
  {
    label: "GA",
    path: "/ga",
    icon: <FaDna />,
  },
  {
    label: "GP",
    path: "/gp",
    icon: <FaCodeBranch />,
  },
  {
    label: "ES",
    path: "/es",
    icon: <SlGraph />,
  },
  {
    label: "EP",
    path: "/ep",
    icon: <GiDiceTarget />,
  },
];

export default function Sidebar({
  theme,
  setTheme,
  collapsed,
  setCollapsed,
}) {
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path) => {
    if (path === "/") {
      return location.pathname === "/";
    }

    return location.pathname === path;
  };

  const renderItem = (item) => (
    <button
      key={item.label}
      className={`sidebar__nav-item ${
        isActive(item.path)
          ? "sidebar__nav-item--active"
          : ""
      }`}
      onClick={() => navigate(item.path)}
    >
      <span className="sidebar__nav-icon">
        {item.icon}
      </span>

      {!collapsed && item.label}
    </button>
  );

  return (
    <aside className={`sidebar ${collapsed ? "collapsed" : ""}`}>
      {/* ---------- Logo ---------- */}

      <div
        className="sidebar_logo"
        onClick={() => {
          setCollapsed(!collapsed);
        }}
      >
        <div className="sidebar_icon">
          <FaBrain className="brain-icon" />
        </div>

        {!collapsed && (
          <div className="sidebar__logo-text">
            <strong>NeuroSim</strong>
            <span>
              Evolutionary Computation Framework
            </span>
          </div>
        )}
      </div>

      <div className="sidebar__divider" />

      {/* ---------- Navigation ---------- */}

      <nav className="sidebar__nav">
        {navItems.map(renderItem)}

        <div className="sidebar__divider" />

        {!collapsed && (
          <p className="sidebar__section-label">
            Playgrounds
          </p>
        )}

        {playgrounds.map(renderItem)}

        <div className="sidebar__divider" />

        {!collapsed && (
          <p className="sidebar__section-label">
            Paradigms
          </p>
        )}

        {paradigms.map(renderItem)}
      </nav>

      {/* ---------- Footer ---------- */}

      <div className="sidebar__footer">
        <div className="sidebar__divider" />

        <button className="sidebar__about-btn">
          <FaInfoCircle />
          {!collapsed && "About NeuroSim"}
        </button>

        <button
          className="sidebar__theme-btn"
          onClick={() =>
            setTheme(
              theme === "dark"
                ? "light"
                : "dark"
            )
          }
        >
          {theme === "dark" ? (
            <>
              <FaSun />
              {!collapsed && "Light Theme"}
            </>
          ) : (
            <>
              <FaMoon />
              {!collapsed && "Dark Theme"}
            </>
          )}
        </button>
      </div>
    </aside>
  );
}