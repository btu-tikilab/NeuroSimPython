import "./ProblemSelection.css";

import {
  FaArrowLeft,
  FaArrowRight,
  FaChartLine,
  FaDna,
} from "react-icons/fa";

const ProblemSelection = ({
  selectedParadigm,
  selectedProblem,
  onSelect,
  back,
}) => {
  const problems = [
    {
      id: "onemax",
      name: "OneMax",
      description:
        "Maximize the number of 1s in a binary genome.",
      icon: <FaDna />,
    },
    {
      id: "regression_linear",
      name: "Regression Linear",
      description:
        "Find the best binary-encoded parameter for a linear regression problem.",
      icon: <FaChartLine />,
    },
  ];

  return (
    <div className="problem-selection-page">
      <div className="breadcrumb">
        Home &gt; BitGA &gt; Problem Selection
      </div>

      <h1 className="page-title">
        Select Problem
      </h1>

      <p className="page-description">
        Choose the optimization problem you want BitGA to solve.
      </p>

      <div className="section-divider"></div>

      <div className="progress-container">
        <div className="progress-step completed">
          <div className="progress-circle">✓</div>
          <p>Paradigm</p>
        </div>

        <div className="progress-step active">
          <div className="progress-circle">2</div>
          <p>Problem</p>
        </div>

        <div className="progress-step">
          <div className="progress-circle">3</div>
          <p>Configuration</p>
        </div>

        <div className="progress-step">
          <div className="progress-circle">4</div>
          <p>Run</p>
        </div>

        <div className="progress-step">
          <div className="progress-circle">5</div>
          <p>Results</p>
        </div>
      </div>

      <div className="problem-grid">
        {problems.map((problem) => (
          <div
            className={`problem-card ${
              selectedProblem === problem.id
                ? "selected"
                : ""
            }`}
            key={problem.id}
            onClick={() => onSelect(problem.id)}
          >
            <div className="problem-icon">
              {problem.icon}
            </div>

            <h2>{problem.name}</h2>

            <p>{problem.description}</p>

            <button
              type="button"
              onClick={(event) => {
                event.stopPropagation();
                onSelect(problem.id);
              }}
            >
              Select
              <FaArrowRight />
            </button>
          </div>
        ))}
      </div>

      <div className="button-section">
        <button
          className="back-btn"
          onClick={back}
        >
          <FaArrowLeft />
          Back
        </button>
      </div>
    </div>
  );
};

export default ProblemSelection;