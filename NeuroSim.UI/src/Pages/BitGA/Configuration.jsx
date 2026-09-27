import "./Configuration.css";
import { useState } from "react";
import { FaPlay, FaArrowLeft, FaDna, FaBoxOpen, FaRandom, FaUsers, FaExchangeAlt, FaChartLine } from "react-icons/fa";
import { MdSettings } from "react-icons/md";
import { HiOutlineInformationCircle } from "react-icons/hi";

const Configuration = ({ selectedParadigm, selectedProblem, back, onRun }) => {
  const [genomeLength,    setGenomeLength]    = useState(20);
  const [randomSeed,      setRandomSeed]      = useState(42);
  const [populationSize,  setPopulationSize]  = useState(100);
  const [generations,     setGenerations]     = useState(250);
  const [parentSelection, setParentSelection] = useState("Tournament");
  const [tournamentSize,  setTournamentSize]  = useState(5);
  const [crossoverType,   setCrossoverType]   = useState("One Point");
  const [crossoverRate,   setCrossoverRate]   = useState(0.8);
  const [mutationType,    setMutationType]    = useState("Flip Bit");
  const [mutationRate,    setMutationRate]    = useState(0.02);
  const [eliteCount,      setEliteCount]      = useState(2);
  const [targetFitness,   setTargetFitness]   = useState(100);
  const [knapsackWeights,  setKnapsackWeights]  = useState("2,3,6,7,5,9,4,3,8,5");
  const [knapsackValues,   setKnapsackValues]   = useState("6,5,8,9,6,7,3,4,8,5");
  const [knapsackCapacity, setKnapsackCapacity] = useState(20);
  const [activeInfo, setActiveInfo] = useState(null);

  const isKnapsack = selectedProblem === "knapsack";

  const showInfo = (name, text) => (
    <span className="info-wrapper">
      <HiOutlineInformationCircle
        className="info-icon"
        onClick={() => setActiveInfo(activeInfo === name ? null : name)}
      />
      {activeInfo === name && <div className="info-tooltip">{text}</div>}
    </span>
  );

  const handleRun = () => {
    const crossoverTypeMap = {
      "One Point": "single_point",
      "Two Point": "two_point",
      "Uniform":   "uniform",
    };
    const weights = isKnapsack
      ? knapsackWeights.split(",").map(Number).filter(n => !isNaN(n) && n > 0)
      : [];
    const payload = {
      problem_id:      selectedProblem,
      genome_length:   isKnapsack ? weights.length : genomeLength,
      seed:            randomSeed,
      population_size: populationSize,
      generations:     generations,
      tournament_size: tournamentSize,
      crossover_type:  crossoverTypeMap[crossoverType] || "single_point",
      crossover_rate:  crossoverRate,
      mutation_rate:   mutationRate,
      elite_count:     eliteCount,
      target_fitness:  targetFitness,
    };
    if (isKnapsack) {
      const values = knapsackValues.split(",").map(Number).filter(n => !isNaN(n) && n >= 0);
      payload.knapsack_weights  = weights;
      payload.knapsack_values   = values;
      payload.knapsack_capacity = knapsackCapacity;
    }
    onRun(payload);
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
                <label>Genome Length {showInfo("gl","Number of bits in each individual.")}</label>
                <input type="number" min="1" value={genomeLength} disabled={isKnapsack}
                  onChange={e => setGenomeLength(Math.max(1, Number(e.target.value)))} />
              </div>
              <div className="form-group">
                <label>Random Seed {showInfo("seed","Same seed = reproducible results.")}</label>
                <input type="number" min="0" value={randomSeed}
                  onChange={e => setRandomSeed(Math.max(0, Number(e.target.value)))} />
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
                    placeholder="2,3,6,7,5,9,4,3,8,5" />
                </div>
                <div className="form-group" style={{gridColumn:"1/-1"}}>
                  <label>Item Values (comma-separated) {showInfo("kv","Value of each item.")}</label>
                  <input type="text" value={knapsackValues}
                    onChange={e => setKnapsackValues(e.target.value)}
                    placeholder="6,5,8,9,6,7,3,4,8,5" />
                </div>
                <div className="form-group">
                  <label>Capacity {showInfo("kc","Max weight the knapsack can hold.")}</label>
                  <input type="number" min="1" value={knapsackCapacity}
                    onChange={e => setKnapsackCapacity(Math.max(1, Number(e.target.value)))} />
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
                  onChange={e => setPopulationSize(Math.max(2, Number(e.target.value)))} />
              </div>
              <div className="form-group">
                <label>Max Generations {showInfo("gen","Maximum generations to run.")}</label>
                <input type="number" min="1" value={generations}
                  onChange={e => setGenerations(Math.max(1, Number(e.target.value)))} />
              </div>
              <div className="form-group">
                <label>Parent Selection {showInfo("sel","Method to select parents.")}</label>
                <select value={parentSelection} onChange={e => setParentSelection(e.target.value)}>
                  <option>Tournament</option>
                  <option>Roulette Wheel</option>
                  <option>Rank</option>
                </select>
              </div>
              <div className="form-group">
                <label>Tournament Size {showInfo("ts","Individuals per tournament.")}</label>
                <input type="number" min="2" value={tournamentSize}
                  onChange={e => setTournamentSize(Math.max(2, Number(e.target.value)))} />
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
                <label>Crossover Rate {showInfo("cr","Probability crossover is performed.")}</label>
                <input type="number" min="0" max="1" step="0.05" value={crossoverRate}
                  onChange={e => setCrossoverRate(Math.min(1, Math.max(0, Number(e.target.value))))} />
              </div>
              <div className="form-group">
                <label>Mutation Type {showInfo("mt","Mutation operator for offspring.")}</label>
                <select value={mutationType} onChange={e => setMutationType(e.target.value)}>
                  <option>Flip Bit</option>
                </select>
              </div>
              <div className="form-group">
                <label>Mutation Rate {showInfo("mr","Probability each bit is flipped.")}</label>
                <input type="number" min="0" max="1" step="0.01" value={mutationRate}
                  onChange={e => setMutationRate(Math.min(1, Math.max(0, Number(e.target.value))))} />
              </div>
              <div className="form-group">
                <label>Elite Count {showInfo("ec","Best individuals preserved each generation.")}</label>
                <input type="number" min="0" value={eliteCount}
                  onChange={e => setEliteCount(Math.max(0, Number(e.target.value)))} />
              </div>
              <div className="form-group">
                <label>Target Fitness {showInfo("tf","Stop when this fitness is reached.")}</label>
                <input type="number" min="0" step="0.01" value={targetFitness}
                  onChange={e => setTargetFitness(Math.max(0, Number(e.target.value)))} />
              </div>
            </div>
          </div>
        </div>

        <div className="right-panel">
          <div className="config-card">
            <div className="card-title"><FaDna /><h2>Binary Genome Preview</h2></div>
            <div className="genome-preview">
              {Array.from({length: Math.min(isKnapsack
                ? knapsackWeights.split(",").filter(Boolean).length
                : genomeLength, 20)}, (_,i) => (
                <span className="genome-bit" key={i}>{i%2===0?"1":"0"}</span>
              ))}
            </div>
            <p className="preview-description">
              Genome length: <strong>{isKnapsack ? knapsackWeights.split(",").filter(Boolean).length : genomeLength}</strong> bits
            </p>
          </div>

          <div className="config-card">
            <div className="card-title"><FaRandom /><h2>Configuration Summary</h2></div>
            <div className="stats-grid">
              <div className="stat-box"><FaDna className="stat-icon"/><h4>Genome</h4><p>{isKnapsack ? knapsackWeights.split(",").filter(Boolean).length : genomeLength} bits</p></div>
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
              The genetic algorithm selects parents, applies crossover and mutation, preserves elite
              individuals, and continues until the maximum generation count or target fitness is reached.
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
