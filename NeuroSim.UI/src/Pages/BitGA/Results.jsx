import "./Results.css";
import { useState } from "react";

import {
  FaArrowLeft,
  FaCheckCircle,
  FaDna,
  FaChartLine,
} from "react-icons/fa";

const Results = ({ results, back }) => {
  const [showOnlyChanges, setShowOnlyChanges] = useState(true);

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

  const history = results.convergenceHistory || [];

  // Table rows: all generations, or only ones where best fitness improved
  const visibleRows = showOnlyChanges
    ? history.filter((h, i) => i === 0 || h.bestFitness !== history[i - 1].bestFitness)
    : history;

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
            {results.bestFitness ?? "-"}
          </div>
        </div>

        <div className="result-card">
          <div className="result-card-title">
            <FaDna />
            <h2>Best Solution</h2>
          </div>

          <div className="best-solution">
            {Array.isArray(results.bestSolution)
              ? results.bestSolution.map((bit, index) => (
                  <span
                    className="solution-bit"
                    key={index}
                  >
                    {bit}
                  </span>
                ))
              : results.bestSolution ?? "-"}
          </div>
        </div>

        <div className="result-card">
          <div className="result-card-title">
            <FaChartLine />
            <h2>Generations</h2>
          </div>

          <div className="result-value">
            {results.totalGenerations ??
              results.generationsToConvergence ??
              "-"}
          </div>
        </div>

      </div>

      <div className="result-card experiment-card">
        <div className="result-card-title">
          <FaChartLine />
          <h2>Generation History</h2>
        </div>

        {history.length > 0 ? (
          <>
            <label style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "12px", fontSize: "14px", cursor: "pointer" }}>
              <input
                type="checkbox"
                checked={showOnlyChanges}
                onChange={(e) => setShowOnlyChanges(e.target.checked)}
              />
              Show only generations where best fitness improved
              {showOnlyChanges && ` (${visibleRows.length} of ${history.length})`}
            </label>

            <div style={{ maxHeight: "400px", overflowY: "auto" }}>
              <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "14px" }}>
                <thead>
                  <tr style={{ textAlign: "left", borderBottom: "2px solid #334155" }}>
                    <th style={{ padding: "8px" }}>Generation</th>
                    <th style={{ padding: "8px" }}>Best</th>
                    <th style={{ padding: "8px" }}>Average</th>
                    <th style={{ padding: "8px" }}>Worst</th>
                  </tr>
                </thead>
                <tbody>
                  {visibleRows.map((h) => (
                    <tr key={h.generation} style={{ borderBottom: "1px solid #1e293b" }}>
                      <td style={{ padding: "8px" }}>{h.generation}</td>
                      <td style={{ padding: "8px", fontWeight: "600" }}>{h.bestFitness}</td>
                      <td style={{ padding: "8px" }}>{h.avgFitness.toFixed(2)}</td>
                      <td style={{ padding: "8px" }}>{h.worstFitness}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        ) : (
          <p>No generation data available.</p>
        )}
      </div>

      <div className="result-card experiment-card">
        <div className="result-card-title">
          <FaChartLine />
          <h2>Experiment Information</h2>
        </div>

        <div className="experiment-grid">

          <div>
            <strong>Run ID</strong>
            <p>{results.runId ?? "-"}</p>
          </div>

          <div>
            <strong>Generations to Convergence</strong>
            <p>
              {results.generationsToConvergence ?? "-"}
            </p>
          </div>

          <div>
            <strong>Total Generations</strong>
            <p>
              {results.totalGenerations ?? "-"}
            </p>
          </div>

          <div>
            <strong>Execution Time</strong>
            <p>
              {results.executionTimeSeconds != null
                ? results.executionTimeSeconds.toFixed(3)
                : "-"} seconds
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