import React from "react";
import "./Home.css";
import brainImage from "../../assets/brain.png";

import {FaArrowRight,FaBookOpen,FaMicrochip,FaProjectDiagram,
  FaRoute,
  FaDna,
  FaCodeBranch
} from "react-icons/fa";

import { FaSquareBinary } from "react-icons/fa6";
import { GiMaze, GiDiceTarget } from "react-icons/gi";
import { SlGraph } from "react-icons/sl";

const playgrounds = [
  {
    id: "bitga",
    name: "BitGA",
    description: "Binary Genetic Algorithm Playground",
    status: "Available",
    icon: <FaSquareBinary />,
  },
  {
    id: "graphga",
    name: "GraphGA",
    description: "Graph Based Genetic Algorithm",
    status: "Available",
    icon: <FaProjectDiagram />,
  },
  {
    id: "tsp",
    name: "TSP",
    description: "Travelling Salesman Problem",
    status: "Coming Soon",
    icon: <FaRoute />,
  },
  {
    id: "maze",
    name: "MazeNet",
    description: "Neuroevolution Maze Solver",
    status: "Coming Soon",
    icon: <GiMaze />,
  },
];

const paradigms = [
  {
    id: "ga",
    name: "Genetic Algorithms",
    short: "GA",
    icon: <FaDna />,
  },
  {
    id: "gp",
    name: "Genetic Programming",
    short: "GP",
    icon: <FaCodeBranch />,
  },
  {
    id: "es",
    name: "Evolution Strategies",
    short: "ES",
    icon: <SlGraph />,
  },
  {
    id: "ep",
    name: "Evolutionary Programming",
    short: "EP",
    icon: <GiDiceTarget />,
  },
];

export default function Home({onNavigate}) {
  return (
    <main className="home">

      {/* ================= HERO ================= */}

      <section className="home__hero">

        <div className="home__hero-content">

          <p className="home__hero-tag">
    Evolutionary Computation Framework
</p>

<h1 className="home__hero-title">
    NeuroSim
</h1>

<h2 className="home__hero-heading">
    Explore the Future of
    <br />
    Evolutionary Computing
</h2>

<p className="home__hero-description">
    Learn, experiment and visualize powerful
    evolutionary algorithms through interactive
    playgrounds. Explore Genetic Algorithms,
    Genetic Programming, Evolution Strategies
    and Evolutionary Programming in one
    unified platform.
</p>

<div className="home__hero-buttons">

    <button
        className="home__primary-btn"
        onClick={() => onNavigate("Wiki")}
    >
        <FaBookOpen />
        Open Wiki
    </button>

</div>

        </div>

        <div className="home__hero-image">
          <img
            src={brainImage}
            alt="NeuroSim"
          />

        </div>

      </section>
            {/* ================= PLAYGROUNDS ================= */}

      <section className="home__section">

        <div className="home__section-header">
          <h2>Explore Playgrounds</h2>
          <p>Experiment with different evolutionary algorithms.</p>
        </div>

        <div className="home__grid">

          {playgrounds.map((item) => (

            <div
              key={item.id}
              className="home__card"
              onClick={() => onNavigate(item.name)}
            >

              <div className="home__card-top">

                <div className="home__card-icon">
                  {item.icon}
                </div>

                <div
                  className={`home__status ${
                    item.status === "Available"
                      ? "available"
                      : "coming"
                  }`}
                >
                  {item.status}
                </div>

              </div>

              <h3 className="home__card-title">
                {item.name}
              </h3>

              <p className="home__card-description">
                {item.description}
              </p>

              <button className="home__card-button">

                Open Playground

                <FaArrowRight className="home__arrow" />

              </button>

            </div>

          ))}

        </div>

      </section>

      {/* ================= PARADIGMS ================= */}

      <section className="home__section">

        <div className="home__section-header">
          <h2>Evolutionary Paradigms</h2>
          <p>
            Core paradigms currently supported in NeuroSim.
          </p>
        </div>

        <div className="home__grid">

          {paradigms.map((item) => (

            <div
              key={item.id}
              className="home__card"
              onClick={() => onNavigate(item.short)}
            >

              <div className="home__card-top">

                <div className="home__card-icon">
                  {item.icon}
                </div>

                <div className="home__status available">
                  Supported
                </div>

              </div>

              <h3 className="home__card-title">

                {item.short}

              </h3>

              <p className="home__card-description">

                {item.name}

              </p>

              <button className="home__card-button">

                Learn More

                <FaArrowRight className="home__arrow" />

              </button>

            </div>

          ))}

        </div>

      </section>
            {/* ================= FOOTER ================= */}

      <footer className="home__footer">

        <div className="home__footer-left">
          <h3>NeuroSim</h3>

          <p>
            A Modern Evolutionary Computation Framework
          </p>
        </div>

        <div className="home__footer-right">

          <span>© Neurosim | 1.0</span>


        </div>

      </footer>

    </main>
  );
}