import "./Configuration.css";
import LiveGraphPreview from "./LiveGraphPreview";
import { useState } from "react";

import {
  FaProjectDiagram,
  FaPlay,
  FaArrowLeft,
  FaRandom,
  FaNetworkWired,
  FaCircle,
  FaLink,
  FaChartPie,
} from "react-icons/fa";

import { MdSettings } from "react-icons/md";
import { HiOutlineInformationCircle } from "react-icons/hi";

const Configuration = ({ back }) => {
  const [allowSelfLoop, setAllowSelfLoop] = useState(false);

  const [nodeCount, setNodeCount] = useState(20);
  const [graphMode, setGraphMode] = useState("Directed");
  const [randomSeed, setRandomSeed] = useState(42);
  const [graphVersion, setGraphVersion] = useState(0);

  return (
    <div className="configuration-page">

      {/* Breadcrumb */}

      <div className="breadcrumb">
        Home &gt; GraphGA &gt; Configuration
      </div>

      {/* Title */}

      <h1 className="page-title">
        GraphGA Configuration
      </h1>

      <p className="page-description">
        Configure Graph OneMax before running the experiment.
      </p>

      <div className="section-divider"></div>

      {/* Progress */}

      <div className="progress-container">

        <div className="progress-step completed">
          <div className="progress-circle">✓</div>
          <p>Paradigm</p>
        </div>

        <div className="progress-step completed">
          <div className="progress-circle">✓</div>
          <p>Problem</p>
        </div>

        <div className="progress-step active">
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

      {/* Main Layout */}

      <div className="configuration-layout">

        {/* LEFT PANEL */}

        <div className="left-panel">

          {/* Graph Configuration */}

          <div className="config-card">

            <div className="card-title">
              <FaNetworkWired />
              <h2>Graph Configuration</h2>
            </div>

            <div className="config-grid">

              <div className="form-group">

                <label>
                  Node Count
                  <HiOutlineInformationCircle className="info-icon" />
                </label>

                <input
                  type="number"
                  value={nodeCount}
                  onChange={(e) => setNodeCount(Number(e.target.value))}
                />

              </div>

              <div className="form-group">

                <label>
                  Graph Mode
                  <HiOutlineInformationCircle className="info-icon" />
                </label>

                <select
                  value={graphMode}
                  onChange={(e) => setGraphMode(e.target.value)}
                >
                  <option>Directed</option>
                  <option>Undirected</option>
                </select>

              </div>

              <div className="form-group">

                <label>
                  Allow Self Loop
                  <HiOutlineInformationCircle className="info-icon" />
                </label>

                <div className="toggle-container">

                  <label className="switch">

                    <input
                      type="checkbox"
                      checked={allowSelfLoop}
                      onChange={() =>
                        setAllowSelfLoop(!allowSelfLoop)
                      }
                    />

                    <span className="slider"></span>

                  </label>

                  <span className="toggle-text">
                    {allowSelfLoop ? "Yes" : "No"}
                  </span>

                </div>

              </div>

              <div className="form-group">

                <label>
                  Random Seed
                  <HiOutlineInformationCircle className="info-icon" />
                </label>

                <input
                  type="number"
                  value={randomSeed}
                  onChange={(e) => setRandomSeed(Number(e.target.value))}
                />

              </div>

            </div>

          </div>

          {/* Problem Configuration */}

          <div className="config-card">

            <div className="card-title">
              <HiOutlineInformationCircle />
              <h2>Problem Configuration</h2>
            </div>

            <div className="config-grid">

              <div className="form-group">
                <label>Connectivity Bonus</label>
                <input type="number" placeholder="10" />
              </div>

              <div className="form-group">
                <label>Sparsity Penalty</label>
                <input type="number" placeholder="2" />
              </div>

            </div>

          </div>

          {/* GA Parameters */}

          <div className="config-card">

            <div className="card-title">
              <MdSettings />
              <h2>GA Parameters</h2>
            </div>

            <div className="config-grid">
                              <div className="form-group">
                <label>
                  Population Size
                  <HiOutlineInformationCircle className="info-icon" />
                </label>
                <input type="number" placeholder="100" />
              </div>

              <div className="form-group">
                <label>
                  Max Generations
                  <HiOutlineInformationCircle className="info-icon" />
                </label>
                <input type="number" placeholder="250" />
              </div>

              <div className="form-group">
                <label>
                  Parent Selection
                  <HiOutlineInformationCircle className="info-icon" />
                </label>
                <select>
                  <option>Tournament</option>
                  <option>Roulette Wheel</option>
                  <option>Rank</option>
                </select>
              </div>

              <div className="form-group">
                <label>
                  Tournament Size
                  <HiOutlineInformationCircle className="info-icon" />
                </label>
                <input type="number" placeholder="5" />
              </div>

              <div className="form-group">
                <label>
                  Crossover Type
                  <HiOutlineInformationCircle className="info-icon" />
                </label>
                <select>
                  <option>One Point</option>
                  <option>Two Point</option>
                  <option>Uniform</option>
                </select>
              </div>

              <div className="form-group">
                <label>
                  Crossover Rate
                  <HiOutlineInformationCircle className="info-icon" />
                </label>
                <input type="number" placeholder="0.80" />
              </div>

              <div className="form-group">
                <label>
                  Mutation Type
                  <HiOutlineInformationCircle className="info-icon" />
                </label>
                <select>
                  <option>Bit Flip</option>
                  <option>Swap</option>
                </select>
              </div>

              <div className="form-group">
                <label>
                  Mutation Rate
                  <HiOutlineInformationCircle className="info-icon" />
                </label>
                <input type="number" placeholder="0.02" />
              </div>

              <div className="form-group">
                <label>
                  Elite Count
                  <HiOutlineInformationCircle className="info-icon" />
                </label>
                <input type="number" placeholder="2" />
              </div>

              <div className="form-group">
                <label>
                  Target Fitness
                  <HiOutlineInformationCircle className="info-icon" />
                </label>
                <input type="number" placeholder="100" />
              </div>

            </div>

          </div>

        </div>

        {/* ================= RIGHT PANEL ================= */}

        <div className="right-panel">

          {/* Live Graph Preview */}

          <div className="config-card">

            <div className="preview-header">

              <div className="card-title">
                <FaProjectDiagram />
                <h2>Live Graph Preview</h2>
              </div>

              <button className="refresh-btn" onClick={() => setGraphVersion(v => v + 1)}>
                <FaRandom />
                Regenerate
              </button>

            </div>

            <div className="graph-preview">

              <LiveGraphPreview
                nodeCount={nodeCount}
                graphMode={graphMode}
                allowSelfLoop={allowSelfLoop}
                graphVersion={graphVersion}
              />

            </div>

          </div>

          {/* Graph Statistics */}

          <div className="config-card">

            <div className="card-title">
              <FaRandom />
              <h2>Graph Statistics</h2>
            </div>

            <div className="stats-grid">

              <div className="stat-box">
                <FaCircle className="stat-icon" />
                <h4>Nodes</h4>
                <p>{nodeCount}</p>
              </div>

              <div className="stat-box">
                <FaLink className="stat-icon" />
                <h4>Edges</h4>
                <p>0</p>
              </div>

              <div className="stat-box">
                <FaChartPie className="stat-icon" />
                <h4>Density</h4>
                <p>0.00</p>
              </div>

              <div className="stat-box">
                <FaNetworkWired className="stat-icon" />
                <h4>Mode</h4>
                <p>{graphMode}</p>
              </div>

              <div className="stat-box">
                <FaRandom className="stat-icon" />
                <h4>Self Loop</h4>
                <p>{allowSelfLoop ? "Yes" : "No"}</p>
              </div>

            </div>

          </div>

          {/* Information */}

          <div className="config-card">

            <div className="card-title">
              <HiOutlineInformationCircle />
              <h2>Information</h2>
            </div>

            <p>
              Configure the graph and genetic algorithm parameters.
              The graph preview and statistics will update automatically
              as the configuration changes.
            </p>

          </div>

        </div>
              </div>

      {/* ================= Buttons ================= */}

      <div className="button-section">

        <button
          className="back-btn"
          onClick={back}
        >
          <FaArrowLeft />
          Back
        </button>

        <button className="run-btn">
          <FaPlay />
          Run Experiment
        </button>

      </div>

    </div>
  );
};

export default Configuration;