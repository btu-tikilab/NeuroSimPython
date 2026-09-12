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
  const [activeInfo, setActiveInfo] = useState(null);
  const showInfo = (name, text) => (
  <span className="info-wrapper">
    <HiOutlineInformationCircle
      className="info-icon"
      onClick={() =>
        setActiveInfo(activeInfo === name ? null : name)
      }
    />

    {activeInfo === name && (
      <div className="info-tooltip">
        {text}
      </div>
    )}
  </span>
);

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
                  {showInfo("nodeCount","Number of nodes in the graph. The maximum is 100 because increasing the number of nodes greatly increases the number of possible connections and makes the genetic search more computationally expensive.")}
                </label>
                <input
                  type="number"
                  min="1"
                  max="100"
                  value={nodeCount}
                  onChange={(e) => setNodeCount(Math.min(100, Math.max(1, Number(e.target.value))))}
                />
              </div>

              <div className="form-group">
                <label>
                  Graph Mode
                  {showInfo("graphMode","Select whether the graph is directed or undirected. In a directed graph, edges have a direction, while in an undirected graph, edges do not have a direction.")}
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
                  {showInfo("allowSelfLoop","Determines whether self-loops are allowed in the graph.")}
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
                  {showInfo("randomSeed","Seed for the random number generator. Setting this to a specific value ensures reproducible results.")}
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
                <label>Connectivity Bonus
                  {showInfo("connectivityBonus","A bonus score added to the fitness of individuals based on their connectivity. Higher values encourage more connected graphs.")}
                </label>
                <input 
                  type="number" 
                  min="0"
                  max="100"
                  step="1"
                  value={connectivityBonus} 
                  onChange={(e) => setConnectivityBonus(Math.min(100, Math.max(0, Number(e.target.value))))}
                />
              </div>

              <div className="form-group">
                <label>Sparsity Penalty
                  {showInfo("sparsityPenalty","A penalty score subtracted from the fitness of individuals based on their sparsity. Higher values encourage denser graphs.")}
                </label>
                <input 
                  type="number" 
                  min="0"
                  max="100"
                  step="1"
                  value={sparsityPenalty} 
                  onChange={(e) => setSparsityPenalty(Math.min(100, Math.max(0, Number(e.target.value))))}  
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
                  {showInfo("populationSize","The number of individuals in each generation.")}
                </label>
                <input 
                  type="number" 
                  value={populationSize} 
                  onChange={(e) => setPopulationSize(Math.max(2, Number(e.target.value)))}
                />
              </div>

              <div className="form-group">
                <label>
                  Max Generations
                  {showInfo("generations","The maximum number of generations to run the genetic algorithm.")}
                </label>
                <input 
                  type="number" 
                  value={generations} 
                  onChange={(e) => setGenerations(Math.max(1, Number(e.target.value)))}
                />
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
                    {showInfo("tournamentSize","Number of individuals competing in each tournament selection. Must be less than or equal to the population size.")}
                  </label>
                <input 
                  type="number" 
                  min="1"
                  value={tournamentSize} 
                  onChange={(e) => setTournamentSize(Math.min(populationSize, Math.max(1, Number(e.target.value))))}
                />
              </div>
              )}

              <div className="form-group">
                <label>
                  Crossover Type
                  {showInfo("crossoverType","The type of crossover operation to use for generating offspring.")}
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
                  {showInfo("crossoverRate","The probability of performing crossover between two parent individuals.")}
                </label>
                <input 
                  type="number" 
                  min="0"
                  max="1"
                  step="0.05"
                  value={crossoverRate} 
                  onChange={(e) => setCrossoverRate(Math.min(1, Math.max(0, Number(e.target.value))))}
                />
              </div>

              <div className="form-group">
                <label>
                  Mutation Type
                  {showInfo("mutationType","The type of mutation operation to use for generating offspring.")}
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
                  {showInfo("mutationRate","The probability of performing mutation on an individual.")}
                </label>
                <input 
                  type="number" 
                  min="0"
                  max="1"
                  step="0.01"
                  value={mutationRate} 
                  onChange={(e) => setMutationRate(Math.min(1, Math.max(0, Number(e.target.value))))}
                />
              </div>

              <div className="form-group">
                <label>
                  Elite Count
                  {showInfo("eliteCount","The number of top-performing individuals to carry over to the next generation.")}
                </label>
                <input 
                  type="number" 
                  min="0"
                  max={populationSize}
                  value={eliteCount} 
                  onChange={(e) => setEliteCount(Math.min(populationSize, Math.max(0, Number(e.target.value))))}
                />
              </div>

              <div className="form-group">
                <label>
                  Target Fitness
                  {showInfo("targetFitness","The desired fitness level that the genetic algorithm aims to achieve.")}
                </label>
                <input 
                  type="number" 
                  min="0"
                  value={targetFitness} 
                  onChange={(e) => setTargetFitness(Math.max(0, Number(e.target.value)))}
                />
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
            onRun({
              problem: selectedProblem,
              populationSize,
              generations,
              mutationRate,
              crossoverRate,
              randomSeed: randomSeed,
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