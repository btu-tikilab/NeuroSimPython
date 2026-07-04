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
    },
    {
      id: "GP",
      title: "Genetic Programming",
      icon: <TbBinaryTree />,
      description:
        "Evolve programs or expressions represented as trees.",
      color: "#22C55E",
    },
    {
      id: "ES",
      title: "Evolution Strategy",
      icon: <PiGraph />,
      description:
        "Evolve solutions by strategically perturbing individuals.",
      color: "#3B82F6",
    },
    {
      id: "EP",
      title: "Evolutionary Programming",
      icon: <BsHexagonFill />,
      description:
        "Evolve populations using mutation-driven search without crossover.",
      color: "#F59E0B",
    },
  ];

  const handleSelection = (id) => {
    setSelectedParadigm(id);

    if (onSelect) {
      onSelect(id);
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

        <h2>Step 1 : Select Paradigm</h2>

        <p>
          Choose an evolutionary paradigm to configure and run your
          experiment.
        </p>

      </div>

      {/* Cards */}

      <div className="cards-container">

        {paradigms.map((item) => (

          <div
            key={item.id}
            className={`paradigm-card ${
              selectedParadigm === item.id
                ? "selected-card"
                : ""
            }`}
            onClick={() => handleSelection(item.id)}
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

            <button
              onClick={(e) => {
                e.stopPropagation();
                handleSelection(item.id);
              }}
            >
              Select {item.id}
            </button>

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
            GraphGA applies evolutionary algorithms on graph-structured
            solutions. Select a paradigm to configure graph settings,
            GA parameters and run experiments.
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
              Maximize the number of edges in the graph.
            </p>

          </div>

          <div className="problem-item">

            <h4>Graph Pathfinding</h4>

            <p>
              Find the optimal/shortest path between nodes.
            </p>

          </div>

        </div>

      </div>

    </div>
  );
};

export default ParadigmSelection;