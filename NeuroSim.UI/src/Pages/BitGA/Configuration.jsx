import "./Configuration.css";
import { useState } from "react";
import { FaPlay, FaArrowLeft, FaDna, FaBoxOpen, FaRandom, FaUsers, FaExchangeAlt, FaChartLine } from "react-icons/fa";
import { MdSettings } from "react-icons/md";
import { HiOutlineInformationCircle } from "react-icons/hi";

const Configuration = ({ selectedParadigm, selectedProblem, back, onRun, savedConfig }) => {
  const [genomeLength,    setGenomeLength]    = useState(savedConfig?.genomeLength    ?? 20);
  const [randomSeed,      setRandomSeed]      = useState(savedConfig?.randomSeed      ?? 42);
  const [populationSize,  setPopulationSize]  = useState(savedConfig?.populationSize  ?? 50);
  const [generations,     setGenerations]     = useState(savedConfig?.generations     ?? 50);
  const [tournamentSize,  setTournamentSize]  = useState(savedConfig?.tournamentSize  ?? 3);
  const [crossoverType,   setCrossoverType]   = useState(savedConfig?.crossoverType   ?? "One Point");
  const [crossoverRate,   setCrossoverRate]   = useState(savedConfig?.crossoverRate   ?? 0.8);
  const [mutationType,    setMutationType]    = useState(savedConfig?.mutationType    ?? "Bit Flip");
  const [mutationRate,    setMutationRate]    = useState(savedConfig?.mutationRate    ?? 0.02);
  const [eliteCount,      setEliteCount]      = useState(savedConfig?.eliteCount      ?? 2);
  const [knapsackWeights,  setKnapsackWeights]  = useState(savedConfig?.knapsackWeights  ?? "5,10,15,20,25,8,12,18");
  const [knapsackValues,   setKnapsackValues]   = useState(savedConfig?.knapsackValues   ?? "10,20,30,40,50,15,25,35");
  const [knapsackCapacity, setKnapsackCapacity] = useState(savedConfig?.knapsackCapacity ?? 60);
  const [activeInfo, setActiveInfo] = useState(null);

  const isKnapsack = selectedProblem === "knapsack";

  const knapsackItemCount  = knapsackWeights.split(",").filter(Boolean).length;
  const knapsackValueCount = knapsackValues.split(",").filter(Boolean).length;

  const eliteTooHigh = Number(eliteCount) >= Number(populationSize);

  const showInfo = (name, text) => (
    <span className="info-wrapper">
      <HiOutlineInformationCircle
        className="info-icon"
        onClick={() => setActiveInfo(activeInfo === name ? null : name)}
      />
      {activeInfo === name && <div className="info-tooltip">{text}</div>}
    </span>
  );

  const randomizeKnapsack = () => {
    const itemCount = Math.floor(Math.random() * 8) + 8;

    const weights = Array.from({ length: itemCount }, () => Math.floor(Math.random() * 25) + 1);
    const values  = Array.from({ length: itemCount }, () => Math.floor(Math.random() * 50) + 5);

    const totalWeight = weights.reduce((sum, w) => sum + w, 0);

    setKnapsackWeights(weights.join(","));
    setKnapsackValues(values.join(","));
    setKnapsackCapacity(Math.max(1, Math.round(totalWeight * 0.5)));
  };

  const handleRun = () => {
    const crossoverTypeMap = {
      "One Point": "Single Point",
      "Two Point": "Two Point",
      "Uniform":   "Uniform",
    };

    const mappedCrossover = crossoverTypeMap[crossoverType];
    if (!mappedCrossover) {
      alert(`Unknown crossover type: ${crossoverType}`);
      return;
    }

    if (eliteTooHigh) {
      alert(`Elite Count (${eliteCount}) must be less than Population Size (${populationSize}).`);
      return;
    }

    const weights = isKnapsack
      ? knapsackWeights.split(",").map(Number).filter(n => !isNaN(n) && n > 0)
      : [];
    const payload = {
      problem:              selectedProblem,
      bitstringLength:      isKnapsack ? weights.length : Number(genomeLength) || 1,
      seed:                 Number(randomSeed) || 0,
      populationSize:       Number(populationSize) || 2,
      generations:          Number(generations) || 1,
      tournamentSize:       Number(tournamentSize) || 2,
      crossoverType:        mappedCrossover,
      crossoverProbability: Number(crossoverRate) || 0,
      mutationType:         mutationType,
      mutationRate:         Number(mutationRate) || 0,
      eliteCount:           Number(eliteCount) || 0,
    };
    if (isKnapsack) {
      const values = knapsackValues.split(",").map(Number).filter(n => !isNaN(n) && n >= 0);
      payload.weights  = weights;
      payload.values   = values;
      payload.capacity = Number(knapsackCapacity) || 1;
    }

    const uiState = {
      genomeLength,
      randomSeed,
      populationSize,
      generations,
      tournamentSize,
      crossoverType,
      crossoverRate,
      mutationType,
      mutationRate,
      eliteCount,
      knapsackWeights,
      knapsackValues,
      knapsackCapacity,
    };

    onRun(payload, uiState);
  };

  return (
    <div className="configuration-page">
      <div className="breadcrumb">Home &gt; BitGA &gt; Configuration</div>
      <h1 className="page-title">BitGA Configuration</h1>
      <p className="page-description">Configure {isKnapsack ? "Knapsack 0/1" : "OneMax"} before running the experiment.</p>
      <div className="section-divider"></div>

      <div className="progress-container">
        {["Paradigm","Problem","Configuration","Run","Results"].map((s,i) => (
          <div key={s} className={"progress-step"+(i<2?" completed":i===2?" active":"")}>
            <div className="progress-circle">{i<2?"✓":i+1}</div>
            <p>{s}</p>
          </div>
        ))}
      </div>

      <div className="configuration-layout">
        <div className="left-panel">

          <div className="config-card">
            <div className="card-title"><FaDna /><h2>Binary Genome</h2></div>
            <div className="config-grid">
              <div className="form-group">
                <label>Genome Length {showInfo("gl","Number of bits in each individual. For Knapsack this is set automatically from the number of items.")}</label>
                <input type="number" min="1"
                  value={isKnapsack ? knapsackItemCount : genomeLength}
                  disabled={isKnapsack}
                  onChange={e => setGenomeLength(e.target.value === "" ? "" : Number(e.target.value))}
                  onBlur={e => setGenomeLength(Math.max(1, Number(e.target.value) || 1))} />
              </div>
              <div className="form-group">
                <label>Random Seed {showInfo("seed","Same seed = reproducible results.")}</label>
                <input type="number" min="0" value={randomSeed}
                  onChange={e => setRandomSeed(e.target.value === "" ? "" : Number(e.target.value))}
                  onBlur={e => setRandomSeed(Math.max(0, Number(e.target.value) || 0))} />
              </div>
            </div>
          </div>

          <div className="config-card">
            <div className="card-title">
              {isKnapsack ? <FaBoxOpen /> : <FaDna />}
              <h2>Problem Configuration</h2>
            </div>
            <div className="selected-problem">
              <strong>Problem:</strong> {isKnapsack ? "Knapsack 0/1" : "OneMax"}
            </div>
            {isKnapsack ? (
              <div className="config-grid">
                <div className="form-group" style={{gridColumn:"1/-1"}}>
                  <label>Item Weights (comma-separated) {showInfo("kw","Weight of each item.")}</label>
                  <input type="text" value={knapsackWeights}
                    onChange={e => setKnapsackWeights(e.target.value)}
                    placeholder="5,10,15,20,25,8,12,18" />
                </div>
                <div className="form-group" style={{gridColumn:"1/-1"}}>
                  <label>Item Values (comma-separated) {showInfo("kv","Value of each item.")}</label>
                  <input type="text" value={knapsackValues}
                    onChange={e => setKnapsackValues(e.target.value)}
                    placeholder="10,20,30,40,50,15,25,35" />
                </div>
                {knapsackItemCount !== knapsackValueCount && (
                  <p style={{color:"#f87171", fontSize:"13px", gridColumn:"1/-1", margin:"0"}}>
                    {knapsackItemCount} weights but {knapsackValueCount} values — these must match.
                  </p>
                )}
                <div className="form-group">
                  <label>Capacity {showInfo("kc","Max weight the knapsack can hold.")}</label>
                  <input type="number" min="1" value={knapsackCapacity}
                    onChange={e => setKnapsackCapacity(e.target.value === "" ? "" : Number(e.target.value))}
                    onBlur={e => setKnapsackCapacity(Math.max(1, Number(e.target.value) || 1))} />
                </div>
                <div className="form-group" style={{gridColumn:"1/-1"}}>
                  <button type="button" onClick={randomizeKnapsack}
                    style={{padding:"8px 16px", cursor:"pointer"}}>
                    <FaRandom style={{marginRight:"6px"}} /> Generate random items
                  </button>
                </div>
              </div>
            ) : (
              <p className="problem-description">OneMax maximizes the number of 1s in the binary genome. fitness = ones_count.</p>
            )}
          </div>

          <div className="config-card">
            <div className="card-title"><MdSettings /><h2>GA Parameters</h2></div>
            <div className="config-grid">
              <div className="form-group">
                <label>Population Size {showInfo("pop","Number of individuals per generation.")}</label>
                <input type="number" min="2" value={populationSize}
                  onChange={e => setPopulationSize(e.target.value === "" ? "" : Number(e.target.value))}
                  onBlur={e => setPopulationSize(Math.max(2, Number(e.target.value) || 2))} />
              </div>
              <div className="form-group">
                <label>Max Generations {showInfo("gen","Maximum generations to run.")}</label>
                <input type="number" min="1" value={generations}
                  onChange={e => setGenerations(e.target.value === "" ? "" : Number(e.target.value))}
                  onBlur={e => setGenerations(Math.max(1, Number(e.target.value) || 1))} />
              </div>
              <div className="form-group">
                <label>Parent Selection {showInfo("sel","BitGA uses tournament selection.")}</label>
                <select value="Tournament" disabled>
                  <option>Tournament</option>
                </select>
              </div>
              <div className="form-group">
                <label>Tournament Size {showInfo("ts","Individuals per tournament.")}</label>
                <input type="number" min="2" value={tournamentSize}
                  onChange={e => setTournamentSize(e.target.value === "" ? "" : Number(e.target.value))}
                  onBlur={e => setTournamentSize(Math.max(2, Number(e.target.value) || 2))} />
              </div>
              <div className="form-group">
                <label>Crossover Type {showInfo("ct","Method to combine parent genomes.")}</label>
                <select value={crossoverType} onChange={e => setCrossoverType(e.target.value)}>
                  <option>One Point</option>
                  <option>Two Point</option>
                  <option>Uniform</option>
                </select>
              </div>
              <div className="form-group">
                <label>Crossover Rate {showInfo("cr","Probability a bit is inherited from parent 1 (Uniform crossover only).")}</label>
                <input type="number" min="0" max="1" step="0.05" value={crossoverRate}
                  onChange={e => setCrossoverRate(e.target.value === "" ? "" : Number(e.target.value))}
                  onBlur={e => setCrossoverRate(Math.min(1, Math.max(0, Number(e.target.value) || 0)))} />
              </div>
              <div className="form-group">
                <label>Mutation Type {showInfo("mt","Bit Flip flips individual bits. Swap exchanges two positions. Inversion reverses a segment.")}</label>
                <select value={mutationType} onChange={e => setMutationType(e.target.value)}>
                  <option>Bit Flip</option>
                  <option>Swap</option>
                  <option>Inversion</option>
                </select>
              </div>
              <div className="form-group">
                <label>Mutation Rate {showInfo("mr","Probability each bit is flipped. A good starting point is 1 divided by the genome length.")}</label>
                <input type="number" min="0" max="1" step="0.01" value={mutationRate}
                  onChange={e => setMutationRate(e.target.value === "" ? "" : Number(e.target.value))}
                  onBlur={e => setMutationRate(Math.min(1, Math.max(0, Number(e.target.value) || 0)))} />
              </div>
              <div className="form-group">
                <label>Elite Count {showInfo("ec","Best individuals carried unchanged into the next generation, so a good solution is never lost. Must be less than the population size.")}</label>
                <input type="number" min="0" value={eliteCount}
                  onChange={e => setEliteCount(e.target.value === "" ? "" : Number(e.target.value))}
                  onBlur={e => setEliteCount(Math.max(0, Number(e.target.value) || 0))} />
              </div>
              {eliteTooHigh && (
                <p style={{color:"#f87171", fontSize:"13px", gridColumn:"1/-1", margin:"0"}}>
                  Elite Count ({eliteCount}) must be less than Population Size ({populationSize}).
                </p>
              )}
            </div>
          </div>
        </div>

        <div className="right-panel">
          <div className="config-card">
            <div className="card-title"><FaDna /><h2>Binary Genome Preview</h2></div>
            <div className="genome-preview">
              {Array.from({length: Math.min(isKnapsack ? knapsackItemCount : (Number(genomeLength) || 0), 20)}, (_,i) => (
                <span className="genome-bit" key={i}>{i%2===0?"1":"0"}</span>
              ))}
            </div>
            <p className="preview-description">
              Genome length: <strong>{isKnapsack ? knapsackItemCount : genomeLength}</strong> bits
            </p>
          </div>

          <div className="config-card">
            <div className="card-title"><FaRandom /><h2>Configuration Summary</h2></div>
            <div className="stats-grid">
              <div className="stat-box"><FaDna className="stat-icon"/><h4>Genome</h4><p>{isKnapsack ? knapsackItemCount : genomeLength} bits</p></div>
              <div className="stat-box"><FaUsers className="stat-icon"/><h4>Population</h4><p>{populationSize}</p></div>
              <div className="stat-box"><FaExchangeAlt className="stat-icon"/><h4>Crossover</h4><p>{crossoverRate}</p></div>
              <div className="stat-box"><FaRandom className="stat-icon"/><h4>Mutation</h4><p>{mutationRate}</p></div>
              <div className="stat-box"><FaChartLine className="stat-icon"/><h4>Problem</h4><p>{isKnapsack?"Knapsack":"OneMax"}</p></div>
            </div>
          </div>

          <div className="config-card">
            <div className="card-title"><HiOutlineInformationCircle /><h2>Information</h2></div>
            <p style={{fontSize:"13px",color:"#94a3b8",lineHeight:"1.6"}}>
              BitGA uses a binary genome. Each individual is represented as a sequence of 0s and 1s.
              The genetic algorithm selects parents using tournament selection, applies crossover and
              mutation, preserves the best individuals through elitism, and continues until the
              maximum generation count is reached.
            </p>
          </div>
        </div>
      </div>

      <div className="button-section">
        <button className="back-btn" onClick={back}><FaArrowLeft /> Back</button>
        <button className="run-btn" onClick={handleRun}><FaPlay /> Run Experiment</button>
      </div>
    </div>
  );
};

export default Configuration;