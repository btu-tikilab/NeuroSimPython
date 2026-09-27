import "./Results.css";

import {
  FaArrowLeft,
  FaCheckCircle,
  FaDna,
  FaChartLine,
} from "react-icons/fa";

const Results = ({ results, back }) => {
  if (!results) {
    return (
      <div className="results-page">
        <h1>No Results</h1>

        <button
          className="back-btn"
          onClick={back}
        >
          <FaArrowLeft />
          Back
        </button>
      </div>
    );
  }

  return (
    <div className="results-page">
      <div className="breadcrumb">
        Home &gt; BitGA &gt; Results
      </div>

      <h1 className="page-title">
        BitGA Results
      </h1>

      <p className="page-description">
        Results from the binary genetic algorithm experiment.
      </p>

      <div className="section-divider"></div>

      <div className="progress-container">
        <div className="progress-step completed">
          <div className="progress-circle">✓</div>
          <p>Paradigm</p>
        </div>

        <div className="progress-step completed">
          <div className="progress-circle">✓</div>
          <p>Problem</p>
        </div>

        <div className="progress-step completed">
          <div className="progress-circle">✓</div>
          <p>Configuration</p>
        </div>

        <div className="progress-step completed">
          <div className="progress-circle">✓</div>
          <p>Run</p>
        </div>

        <div className="progress-step active">
          <div className="progress-circle">5</div>
          <p>Results</p>
        </div>
      </div>

      <div className="results-grid">

        <div className="result-card">
          <div className="result-card-title">
            <FaCheckCircle />
            <h2>Best Fitness</h2>
          </div>

          <div className="result-value">
            {results.best_fitness ?? "-"}
          </div>
        </div>

        <div className="result-card">
          <div className="result-card-title">
            <FaDna />
            <h2>Best Solution</h2>
          </div>

          <div className="best-solution">
            {Array.isArray(results.best_solution)
              ? results.best_solution.map((bit, index) => (
                  <span
                    className="solution-bit"
                    key={index}
                  >
                    {bit}
                  </span>
                ))
              : results.best_solution ?? "-"}
          </div>
        </div>

        <div className="result-card">
          <div className="result-card-title">
            <FaChartLine />
            <h2>Generations</h2>
          </div>

          <div className="result-value">
            {results.total_generations ??
              results.generations_to_convergence ??
              "-"}
          </div>
        </div>

      </div>

      <div className="result-card experiment-card">
        <div className="result-card-title">
          <FaChartLine />
          <h2>Experiment Information</h2>
        </div>

        <div className="experiment-grid">

          <div>
            <strong>Run ID</strong>
            <p>{results.problem_id ?? "-"}</p>
          </div>

          <div>
            <strong>Generations to Convergence</strong>
            <p>
              {results.generations_to_convergence ?? "-"}
            </p>
          </div>

          <div>
            <strong>Total Generations</strong>
            <p>
              {results.total_generations ?? "-"}
            </p>
          </div>

          <div>
            <strong>Execution Time</strong>
            <p>
              {results.execution_time_seconds ?? "-"} seconds
            </p>
          </div>

        </div>
      </div>

      <div className="button-section">
        <button
          className="back-btn"
          onClick={back}
        >
          <FaArrowLeft />
          Back to Configuration
        </button>
      </div>
    </div>
  );
};

export default Results;