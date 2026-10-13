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

const Configuration = ({ selectedParadigm, selectedProblem, back, onRun }) => {
  const [allowSelfLoop, setAllowSelfLoop] = useState(false);
  const [nodeCount, setNodeCount] = useState(20);
  const [graphMode, setGraphMode] = useState("Directed");
  const [randomSeed, setRandomSeed] = useState(42);
  const [graphVersion, setGraphVersion] = useState(0);

  // Added States for API binding
  const [connectivityBonus, setConnectivityBonus] = useState(10);
  const [sparsityPenalty, setSparsityPenalty] = useState(2);
  
  const [populationSize, setPopulationSize] = useState(100);
  const [generations, setGenerations] = useState(250);
  const [parentSelection, setParentSelection] = useState("Tournament");
  const [tournamentSize, setTournamentSize] = useState(5);
  const [crossoverType, setCrossoverType] = useState("One Point");
  const [crossoverRate, setCrossoverRate] = useState(0.80);
  const [mutationType, setMutationType] = useState("Bit Flip");
  const [mutationRate, setMutationRate] = useState(0.02);
  const [eliteCount, setEliteCount] = useState(2);
  const [targetFitness, setTargetFitness] = useState(100);
  const [validationErrors, setValidationErrors] = useState({});
  
const validateConfiguration = () => {
  const errors = {};

  // Required values and integer validation
  const integerFields = [
    ["Node Count", nodeCount, 1],
    ["Population Size", populationSize, 2],
    ["Max Generations", generations, 1],
    ["Random Seed", randomSeed, 0],
    ["Elite Count", eliteCount, 0],
  ];

  integerFields.forEach(([name, value, minimum]) => {
    if (
      value === "" ||
      value === null ||
      !Number.isFinite(Number(value)) ||
      !Number.isInteger(Number(value)) ||
      Number(value) < minimum
    ) {
      errors[name] =
        `${name} must be an integer greater than or equal to ${minimum}.`;
    }
  });

  // Tournament size is relevant only for Tournament selection
  if (parentSelection === "Tournament") {
    if (
      tournamentSize === "" ||
      !Number.isFinite(Number(tournamentSize)) ||
      !Number.isInteger(Number(tournamentSize)) ||
      Number(tournamentSize) < 1
    ) {
      errors["Tournament Size"] =
        "Tournament size must be a positive integer.";
    } else if (Number(tournamentSize) > Number(populationSize)) {
      errors["Tournament Size"] =
        "Tournament size cannot exceed population size.";
    }
  }

  // Elitism must fit within the population
  if (
    Number.isInteger(Number(populationSize)) &&
    Number(populationSize) >= 2 &&
    Number.isInteger(Number(eliteCount)) &&
    Number(eliteCount) > Number(populationSize)
  ) {
    errors["Elite Count"] =
      "Elite count cannot exceed population size.";
  }

  // Probability values
  if (
    !Number.isFinite(Number(crossoverRate)) ||
    Number(crossoverRate) < 0 ||
    Number(crossoverRate) > 1
  ) {
    errors["Crossover Rate"] =
      "Crossover rate must be between 0 and 1.";
  }

  if (
    !Number.isFinite(Number(mutationRate)) ||
    Number(mutationRate) < 0 ||
    Number(mutationRate) > 1
  ) {
    errors["Mutation Rate"] =
      "Mutation rate must be between 0 and 1.";
  }

  // Non-negative fitness parameters
  if (
    !Number.isFinite(Number(connectivityBonus)) ||
    Number(connectivityBonus) < 0
  ) {
    errors["Connectivity Bonus"] =
      "Connectivity bonus must be non-negative.";
  }

  if (
    !Number.isFinite(Number(sparsityPenalty)) ||
    Number(sparsityPenalty) < 0
  ) {
    errors["Sparsity Penalty"] =
      "Sparsity penalty must be non-negative.";
  }

  // Non-negative target fitness
  if (
    !Number.isFinite(Number(targetFitness)) ||
    Number(targetFitness) < 0
  ) {
    errors["Target Fitness"] =
      "Target fitness must be a non-negative number.";
  }

  setValidationErrors(errors);
  return Object.keys(errors).length === 0;
};
const renderError = (field) =>
  validationErrors[field] ? (
    <p className="validation-error" role="alert">
      {validationErrors[field]}
    </p>
  ) : null;



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
                  min="1"
                  value={nodeCount}
                  onChange={(e) => setNodeCount(Math.max(1, Number(e.target.value)))}
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
                      onChange={() => setAllowSelfLoop(!allowSelfLoop)}
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
                  min="0"
                  value={randomSeed}
                  onChange={(e) => setRandomSeed(Math.max(0, Number(e.target.value)))}
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
                <input 
                  type="number" 
                  min="0"
                  value={connectivityBonus} 
                  onChange={(e) => setConnectivityBonus(Math.max(0, Number(e.target.value)))}
                />
              </div>

              <div className="form-group">
                <label>Sparsity Penalty</label>
                <input 
                  type="number" 
                  min="0"
                  value={sparsityPenalty} 
                  onChange={(e) => setSparsityPenalty(Math.max(0, Number(e.target.value)))}
                />
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
                <input 
                  type="number" 
                  min="2"
                  value={populationSize} 
                  onChange={(e) => setPopulationSize(Math.max(2, Number(e.target.value)))}
                />
                {renderError("Population Size")}
              </div>

              <div className="form-group">
                <label>
                  Max Generations
                  <HiOutlineInformationCircle className="info-icon" />
                </label>
                <input 
                  type="number" 
                  min="1"
                  value={generations} 
                  onChange={(e) => setGenerations(Math.max(1, Number(e.target.value)))}
                />
                {renderError("Max Generations")}
              </div>

              <div className="form-group">
                <label>
                  Parent Selection
                  <HiOutlineInformationCircle className="info-icon" />
                </label>
                <select 
                  value={parentSelection} 
                  onChange={(e) => setParentSelection(e.target.value)}
                >
                  <option>Tournament</option>
                  <option>Roulette Wheel</option>
                  <option>Rank</option>
                </select>
              </div>

              {parentSelection === "Tournament" && (
                <div className="form-group">
                  <label>
                    Tournament Size
                    <HiOutlineInformationCircle className="info-icon" />
                  </label>
                  <input 
                    type="number" 
                    min="1"
                    value={tournamentSize} 
                    onChange={(e) => setTournamentSize(Math.max(1, Number(e.target.value)))}
                  />
                  {renderError("Tournament Size")}
                </div>
              )}

              <div className="form-group">
                <label>
                  Crossover Type
                  <HiOutlineInformationCircle className="info-icon" />
                </label>
                <select 
                  value={crossoverType} 
                  onChange={(e) => setCrossoverType(e.target.value)}
                >
                  <option>One Point</option>
                  <option>Two Point</option>
                  <option>Uniform</option>
                  <option>Edge Swap</option>
                  <option>Subgraph Swap</option>
                </select>
              </div>

              <div className="form-group">
                <label>
                  Crossover Rate
                  <HiOutlineInformationCircle className="info-icon" />
                </label>
                <input 
                  type="number" 
                  step="0.05"
                  min="0"
                  max="1"
                  value={crossoverRate} 
                  onChange={(e) => setCrossoverRate(Math.max(0, Math.min(1, Number(e.target.value))))}
                />
                {renderError("Crossover Rate")}
              </div>

              <div className="form-group">
                <label>
                  Mutation Type
                  <HiOutlineInformationCircle className="info-icon" />
                </label>
                <select 
                  value={mutationType} 
                  onChange={(e) => setMutationType(e.target.value)}
                >
                  <option>Bit Flip</option>
                  <option>Swap</option>
                  <option>Edge Flip</option>
                  <option>Node Attr Flip</option>
                </select>
              </div>

              <div className="form-group">
                <label>
                  Mutation Rate
                  <HiOutlineInformationCircle className="info-icon" />
                </label>
                <input 
                  type="number" 
                  step="0.01"
                  min="0"
                  max="1"
                  value={mutationRate} 
                  onChange={(e) => setMutationRate(Math.max(0, Math.min(1, Number(e.target.value))))}
                />
                {renderError("Mutation Rate")}
              </div>

              <div className="form-group">
                <label>
                  Elite Count
                  <HiOutlineInformationCircle className="info-icon" />
                </label>
                <input 
                  type="number" 
                  min="0"
                  value={eliteCount} 
                  onChange={(e) => setEliteCount(Math.max(0, Number(e.target.value)))}
                />
                {renderError("Elite Count")}
              </div>

              <div className="form-group">
                <label>
                  Target Fitness
                  <HiOutlineInformationCircle className="info-icon" />
                </label>
                <input 
                  type="number" 
                  min="0"
                  value={targetFitness} 
                  onChange={(e) => setTargetFitness(Math.max(0, Number(e.target.value)))}
                />
                {renderError("Target Fitness")}
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

        <button
          className="run-btn"
          onClick={() => {
            if (!validateConfiguration()) {
              return;
            }
            onRun({
              problem: selectedProblem,
              populationSize,
              generations,
              mutationRate,
              crossoverRate,
              seed: randomSeed,
              nodeCount,
              graphMode,
              allowSelfLoop,
              parentSelection,
              tournamentSize,
              crossoverType,
              mutationType,
              eliteCount,
              targetFitness,
              connectivityBonus,
              sparsityPenalty
            });
          }}
        >
          <FaPlay />
          Run Experiment
        </button>
      </div>

    </div>
  );
};

export default Configuration;