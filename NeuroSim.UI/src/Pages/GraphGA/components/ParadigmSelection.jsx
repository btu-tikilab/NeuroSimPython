
import { useState } from "react";
import "./ParadigmSelection.css";

import { FaDna } from "react-icons/fa";
import { TbBinaryTree } from "react-icons/tb";
import { PiGraph } from "react-icons/pi";
import { BsHexagonFill } from "react-icons/bs";
import { HiOutlineInformationCircle } from "react-icons/hi";
import { MdOutlineExtension } from "react-icons/md";

const ParadigmSelection = ({ onSelect }) => {
  const [selectedParadigm, setSelectedParadigm] = useState("GA");

  const paradigms = [
    {
      id: "GA",
      title: "Genetic Algorithm",
      icon: <FaDna />,
      description:
        "Evolve a population using selection, crossover and mutation on graphs.",
      color: "#8B5CF6",
      available: true,
    },
    {
      id: "GP",
      title: "Genetic Programming",
      icon: <TbBinaryTree />,
      description:
        "Evolve programs or expressions represented as trees.",
      color: "#22C55E",
      available: false,
    },
    {
      id: "ES",
      title: "Evolution Strategy",
      icon: <PiGraph />,
      description:
        "Evolve solutions by strategically perturbing individuals.",
      color: "#3B82F6",
      available: false,
    },
    {
      id: "EP",
      title: "Evolutionary Programming",
      icon: <BsHexagonFill />,
      description:
        "Evolve populations using mutation-driven search without crossover.",
      color: "#F59E0B",
      available: false,
    },
  ];

  const handleSelection = (item) => {
    // Do not allow selection of modules under development.
    if (!item.available) return;

    setSelectedParadigm(item.id);

    if (onSelect) {
      onSelect(item.id);
    }
  };

  return (
    <div className="paradigm-selection">
      {/* Breadcrumb */}
      <div className="breadcrumb">
        Home &gt; <span>GraphGA</span> &gt; Select Paradigm
      </div>

      {/* Title */}
      <h1 className="page-title">GraphGA</h1>

      <p className="page-description">
        Graph-based evolutionary computation playground.
      </p>

      <div className="section-divider"></div>

      {/* Step */}
      <div className="step-section">
        <h2>Step 1: Select Paradigm</h2>

        <p>
          Choose an available evolutionary paradigm to configure and run
          your experiment.
        </p>
      </div>

      {/* Paradigm Cards */}
      <div className="cards-container">
        {paradigms.map((item) => (
          <div
            key={item.id}
            className={`paradigm-card ${
              selectedParadigm === item.id && item.available
                ? "selected-card"
                : ""
            } ${!item.available ? "module-in-development" : ""}`}
          >
            <div
              className="circle-icon"
              style={{ color: item.color }}
            >
              {item.icon}
            </div>

            <h2
              className="card-heading"
              style={{ color: item.color }}
            >
              {item.id}
            </h2>

            <h4>{item.title}</h4>

            <p>{item.description}</p>

            {item.available ? (
              <button
                onClick={() => handleSelection(item)}
              >
                Open {item.id}
              </button>
            ) : (
              <>
                <span className="development-badge">
                  In Development
                </span>

                <button
                  type="button"
                  disabled
                  className="development-button"
                >
                  Coming Soon
                </button>
              </>
            )}
          </div>
        ))}
      </div>

      {/* Bottom Section */}
      <div className="bottom-section">
        <div className="about-card">
          <div className="card-title">
            <HiOutlineInformationCircle />
            <h3>About GraphGA</h3>
          </div>

          <p>
            The current implementation focuses on the Genetic Algorithm
            (GA) module for graph-based optimization. Other evolutionary
            paradigms are displayed for reference and are still under
            development.
          </p>
        </div>

        <div className="problem-card">
          <div className="card-title">
            <MdOutlineExtension />
            <h3>Supported Problems</h3>
          </div>

          <div className="problem-item">
            <h4>Graph OneMax</h4>
            <p>
              Evaluate graph solutions using the implemented fitness
              function.
            </p>
          </div>

          <div className="problem-item">
            <h4>Graph Pathfinding</h4>
            <p>
              This problem is available only if its implementation is
              complete and integrated. Otherwise, mark it as In Development.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ParadigmSelection;
