import "./ParadigmSelection.css";

import {
  FaArrowRight,
  FaDna,
} from "react-icons/fa";

const ParadigmSelection = ({ onSelect }) => {
  return (
    <div className="paradigm-selection-page">
      <div className="breadcrumb">
        Home &gt; BitGA &gt; Paradigm Selection
      </div>

      <h1 className="page-title">
        Select Paradigm
      </h1>

      <p className="page-description">
        Choose the optimization paradigm you want to use.
      </p>

      <div className="section-divider"></div>

      <div className="progress-container">
        <div className="progress-step active">
          <div className="progress-circle">1</div>
          <p>Paradigm</p>
        </div>

        <div className="progress-step">
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

      <div className="paradigm-grid">
        <div
          className="paradigm-card selected"
          onClick={() => onSelect("GA")}
        >
          <div className="paradigm-icon">
            <FaDna />
          </div>

          <h2>Genetic Algorithm</h2>

          <p>
            Use a binary genetic algorithm to evolve
            solutions through selection, crossover,
            mutation, and elitism.
          </p>

          <button
            type="button"
            onClick={() => onSelect("GA")}
          >
            Continue
            <FaArrowRight />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ParadigmSelection;