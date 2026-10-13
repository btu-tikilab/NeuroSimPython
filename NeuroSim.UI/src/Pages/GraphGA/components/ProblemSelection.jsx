
import { useState } from "react";
import "./ProblemSelection.css";

import { FaProjectDiagram, FaRoute } from "react-icons/fa";
import { HiOutlineInformationCircle } from "react-icons/hi";

const ProblemSelection = ({ selectedParadigm, back, next }) => {
  const [selectedProblem, setSelectedProblem] = useState("");

  const problems = [
    {
      id: "graph_onemax",
      name: "Graph OneMax",
      icon: <FaProjectDiagram />,
      description: "Maximize the number of edges in the graph.",
      color: "#8B5CF6",
      available: true,
    },
    {
      id: "graph_pathfinding",
      name: "Graph Pathfinding",
      icon: <FaRoute />,
      description: "Find the shortest path between nodes.",
      color: "#3B82F6",
      available: false,
    },
  ];

  const handleProblemSelection = (problem) => {
    if (!problem.available) return;

    setSelectedProblem(problem.id);

    if (next) {
      next(problem.id);
    }
  };

  return (
    <div className="problem-selection">
      <div className="problem-container">
        {/* Breadcrumb */}
        <div className="breadcrumb">
          Home &gt; GraphGA &gt; Problem Selection
        </div>

        <h1 className="page-title">GraphGA</h1>

        <p className="page-description">
          Selected Paradigm: <strong>{selectedParadigm}</strong>
        </p>

        <div className="section-divider"></div>

        {/* Step */}
        <div className="step-section">
          <h2>Step 2: Select Problem</h2>
          <p>Choose an available graph optimization problem.</p>
        </div>

        {/* Problem Cards */}
        <div className="cards-container">
          {problems.map((problem) => (
            <div
              key={problem.id}
              className={`problem-card ${
                selectedProblem === problem.id && problem.available
                  ? "selected-card"
                  : ""
              } ${
                !problem.available ? "problem-in-development" : ""
              }`}
            >
              <div
                className="circle-icon"
                style={{ color: problem.color }}
              >
                {problem.icon}
              </div>

              <h2
                className="card-heading"
                style={{ color: problem.color }}
              >
                {problem.name}
              </h2>

              <p>{problem.description}</p>

              {problem.available ? (
                <button
                  type="button"
                  onClick={() => handleProblemSelection(problem)}
                >
                  Select
                </button>
              ) : (
                <>
                  <span className="development-badge">
                    In Development
                  </span>

                  <button
                    type="button"
                    className="development-button"
                    disabled
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
              <h3>Problem Description</h3>
            </div>

            <p>
              Select an implemented optimization problem for the
              Genetic Algorithm to solve on graph structures.
            </p>
          </div>

          <div className="about-card">
            <div className="card-title">
              <FaProjectDiagram />
              <h3>Selected Paradigm</h3>
            </div>

            <h2>{selectedParadigm}</h2>

            <p>
              The selected paradigm will be used in the next
              configuration step.
            </p>
          </div>
        </div>

        {/* Navigation */}
        <div className="button-section">
          <button
            type="button"
            className="back-btn"
            onClick={back}
          >
            ← Back
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProblemSelection;
