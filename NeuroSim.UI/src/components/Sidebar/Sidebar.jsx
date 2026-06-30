import React from 'react';
import './Sidebar.css';

import {FaHome,FaBookOpen,FaProjectDiagram,FaRoute,FaDna,FaCodeBranch,FaBrain,FaInfoCircle,FaMoon,FaSun} from 'react-icons/fa';
import { FaSquareBinary } from "react-icons/fa6";
import { GiMaze, GiDiceTarget } from "react-icons/gi";
import { SlGraph } from "react-icons/sl";

const navItems = [
  {
    label: 'Home',
    icon: <FaHome />,
  },
  {
    label: 'Wiki',
    icon: <FaBookOpen />,
  },
];

const playgrounds = [
  {
    label: 'BitGA',
    icon: <FaSquareBinary />,
  },
  {
    label: 'GraphGA',
    icon: <FaProjectDiagram />,
  },
  {
    label: 'TSP',
    icon: <FaRoute />,
  },
  {
    label: 'MazeNet',
    icon: <GiMaze />,
  },
];

const paradigms = [
  {
    label: 'GA',
    icon: <FaDna />,
  },
  {
    label: 'GP',
    icon: <FaCodeBranch />,
  },
  {
    label: 'ES',
    icon: <SlGraph />,
  },
  {
    label: 'EP',
    icon: <GiDiceTarget />,
  },
];

export default function Sidebar({activeItem,onNavigate,theme,setTheme,}) {
  return (
    <aside className="sidebar">
      <div className="sidebar_logo">
        <div className="sidebar_icon">
          <FaBrain className="brain-icon" />
        </div>

        <div className="sidebar__logo-text">
          <strong>NeuroSim</strong>
          <span>Evolutionary Computation Framework</span>
        </div>

      </div>

      <div className="sidebar__divider" />
      <nav className="sidebar__nav">
        {navItems.map((item) => (
          <button key={item.label} className={`sidebar__nav-item ${activeItem === item.label ? 'sidebar__nav-item--active' : ''}`} onClick={() =>
              onNavigate && onNavigate(item.label)
            }
          >
            <span className="sidebar__nav-icon">
              {item.icon}
            </span>

            {item.label}
          </button>
        ))}

        <div className="sidebar__divider" />
        <p className="sidebar__section-label">
          Playgrounds
        </p>

        {playgrounds.map((item) => (
          <button
            key={item.label} className={`sidebar__nav-item ${ activeItem === item.label ? 'sidebar__nav-item--active' : ''}`} onClick={() =>
              onNavigate && onNavigate(item.label)
            }>
            <span className="sidebar__nav-icon">{item.icon}</span>
            {item.label}
          </button>
        ))}

        <div className="sidebar__divider" />

        <p className="sidebar__section-label">
          Paradigms
        </p>
        {paradigms.map((item) => (
          <button
            key={item.label}
            className={`sidebar__nav-item ${ activeItem === item.label ? 'sidebar__nav-item--active' : '' }`} onClick={() =>
              onNavigate && onNavigate(item.label)
            }>
            <span className="sidebar__nav-icon"> {item.icon} </span>
            {item.label}
          </button>
        ))}
        </nav>
      <div className="sidebar__footer">
        <div className="sidebar__divider" />
        <button className="sidebar__about-btn">
          <FaInfoCircle />
          About NeuroSim
        </button>

        <button
          className="sidebar__theme-btn"
          onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
        >
          {theme === 'dark' ? (
            <>
              <FaSun />
              Light Theme
            </>
          ) : (
            <>
              <FaMoon />
              Dark Theme
            </>
          )}
        </button>

      </div>
    </aside>
  );
}