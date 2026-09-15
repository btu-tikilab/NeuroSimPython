import "./Configuration.css";
import { useState } from "react";

import {
  FaPlay,
  FaArrowLeft,
  FaDna,
  FaChartLine,
  FaRandom,
  FaUsers,
  FaExchangeAlt,
} from "react-icons/fa";

import { MdSettings } from "react-icons/md";
import { HiOutlineInformationCircle } from "react-icons/hi";

const Configuration = ({
  selectedParadigm,
  selectedProblem,
  back,
  onRun,
}) => {
  // ============================================================
  // Problem / Genome Configuration
  // ============================================================

  const [genomeLength, setGenomeLength] = useState(20);
  const [randomSeed, setRandomSeed] = useState(42);

  // ============================================================
  // Regression Linear specific parameters
  // ============================================================

  const [wMin, setWMin] = useState(-10);
  const [wMax, setWMax] = useState(10);
  const [dataSeed, setDataSeed] = useState(42);
  const [nPoints, setNPoints] = useState(20);

  // ============================================================
  // GA Parameters
  // ============================================================

  const [populationSize, setPopulationSize] = useState(100);
  const [generations, setGenerations] = useState(250);

  const [parentSelection, setParentSelection] = useState("Tournament");
  const [tournamentSize, setTournamentSize] = useState(5);

  const [crossoverType, setCrossoverType] = useState("One Point");
  const [crossoverRate, setCrossoverRate] = useState(0.8);

  const [mutationType, setMutationType] = useState("Flip Bit");
  const [mutationRate, setMutationRate] = useState(0.02);

  const [eliteCount, setEliteCount] = useState(2);
  const [targetFitness, setTargetFitness] = useState(100);

  // ============================================================
  // Information tooltip
  // ============================================================

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

  // ============================================================
  // Detect selected problem
  // ============================================================

  const isRegression =
    selectedProblem === "regression_linear" ||
    selectedProblem === "Regression Linear";

  // ============================================================
  // Run experiment
  // ============================================================

  const handleRun = () => {
    onRun({
      problem: selectedProblem,

      bitstringLength: genomeLength,
      randomSeed,

      populationSize,
      generations,

      parentSelection,
      tournamentSize,

      crossoverType,
      crossoverRate,

      mutationType,
      mutationRate,

      eliteCount,
      targetFitness,

      ...(isRegression && {
        wMin,
        wMax,
        dataSeed,
        nPoints,
      }),
    });
  };

  return (
    <div className="configuration-page">

      {/* ========================================================
          Breadcrumb
      ======================================================== */}

      <div className="breadcrumb">
        Home &gt; BitGA &gt; Configuration
      </div>

      {/* ========================================================
          Title
      ======================================================== */}

      <h1 className="page-title">
        BitGA Configuration
      </h1>

      <p className="page-description">
        Configure the binary genetic algorithm before running the experiment.
      </p>

      <div className="section-divider"></div>

      {/* ========================================================
          Progress
      ======================================================== */}

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

      {/* ========================================================
          Main Layout
      ======================================================== */}

      <div className="configuration-layout">

        {/* ======================================================
            LEFT PANEL
        ====================================================== */}

        <div className="left-panel">

          {/* ====================================================
              Binary Genome
          ==================================================== */}

          <div className="config-card">

            <div className="card-title">
              <FaDna />
              <h2>Binary Genome</h2>
            </div>

            <div className="config-grid">

              {/* Genome Length */}

              <div className="form-group">

                <label>
                  Genome Length

                  {showInfo(
                    "genomeLength",
                    "Number of bits in each individual binary genome."
                  )}
                </label>

                <input
                  type="number"
                  min="1"
                  value={genomeLength}
                  onChange={(e) =>
                    setGenomeLength(
                      Math.max(1, Number(e.target.value))
                    )
                  }
                />

              </div>

              {/* Random Seed */}

              <div className="form-group">

                <label>
                  Random Seed

                  {showInfo(
                    "randomSeed",
                    "Seed used by the random number generator. Using the same seed makes the experiment reproducible."
                  )}
                </label>

                <input
                  type="number"
                  min="0"
                  value={randomSeed}
                  onChange={(e) =>
                    setRandomSeed(
                      Math.max(0, Number(e.target.value))
                    )
                  }
                />

              </div>

            </div>
          </div>


          {/* ====================================================
              Problem Configuration
          ==================================================== */}

          <div className="config-card">

            <div className="card-title">

              {isRegression ? (
                <FaChartLine />
              ) : (
                <FaDna />
              )}

              <h2>Problem Configuration</h2>

            </div>

            {/* Show selected problem */}

            <div className="selected-problem">

              <strong>Problem:</strong>{" "}
              {isRegression
                ? "Regression Linear"
                : "OneMax"}

            </div>


            {/* ==================================================
                Regression Linear parameters
            ================================================== */}

            {isRegression && (
              <div className="config-grid">

                {/* w_min */}

                <div className="form-group">

                  <label>
                    w Min

                    {showInfo(
                      "wMin",
                      "Minimum value of the regression parameter w."
                    )}
                  </label>

                  <input
                    type="number"
                    step="0.1"
                    value={wMin}
                    onChange={(e) =>
                      setWMin(Number(e.target.value))
                    }
                  />

                </div>


                {/* w_max */}

                <div className="form-group">

                  <label>
                    w Max

                    {showInfo(
                      "wMax",
                      "Maximum value of the regression parameter w."
                    )}
                  </label>

                  <input
                    type="number"
                    step="0.1"
                    value={wMax}
                    onChange={(e) =>
                      setWMax(Number(e.target.value))
                    }
                  />

                </div>


                {/* Data Seed */}

                <div className="form-group">

                  <label>
                    Data Seed

                    {showInfo(
                      "dataSeed",
                      "Seed used to generate the regression data."
                    )}
                  </label>

                  <input
                    type="number"
                    min="0"
                    value={dataSeed}
                    onChange={(e) =>
                      setDataSeed(
                        Math.max(0, Number(e.target.value))
                      )
                    }
                  />

                </div>


                {/* Number of Points */}

                <div className="form-group">

                  <label>
                    Number of Points

                    {showInfo(
                      "nPoints",
                      "Number of data points used for the regression problem."
                    )}
                  </label>

                  <input
                    type="number"
                    min="1"
                    value={nPoints}
                    onChange={(e) =>
                      setNPoints(
                        Math.max(1, Number(e.target.value))
                      )
                    }
                  />

                </div>

              </div>
            )}

            {/* ==================================================
                OneMax information
            ================================================== */}

            {!isRegression && (
              <div className="problem-description">

                <p>
                  OneMax maximizes the number of 1s in the binary
                  genome.
                </p>

              </div>
            )}

          </div>


          {/* ====================================================
              GA Parameters
          ==================================================== */}

          <div className="config-card">

            <div className="card-title">
              <MdSettings />
              <h2>GA Parameters</h2>
            </div>

            <div className="config-grid">

              {/* Population Size */}

              <div className="form-group">

                <label>
                  Population Size

                  {showInfo(
                    "populationSize",
                    "Number of individuals in each generation."
                  )}
                </label>

                <input
                  type="number"
                  min="2"
                  value={populationSize}
                  onChange={(e) =>
                    setPopulationSize(
                      Math.max(2, Number(e.target.value))
                    )
                  }
                />

              </div>


              {/* Generations */}

              <div className="form-group">

                <label>
                  Max Generations

                  {showInfo(
                    "generations",
                    "Maximum number of generations the genetic algorithm can run."
                  )}
                </label>

                <input
                  type="number"
                  min="1"
                  value={generations}
                  onChange={(e) =>
                    setGenerations(
                      Math.max(1, Number(e.target.value))
                    )
                  }
                />

              </div>


              {/* Parent Selection */}

              <div className="form-group">

                <label>
                  Parent Selection

                  {showInfo(
                    "parentSelection",
                    "Method used to select individuals that become parents."
                  )}
                </label>

                <select
                  value={parentSelection}
                  onChange={(e) =>
                    setParentSelection(e.target.value)
                  }
                >
                  <option>Tournament</option>
                  <option>Roulette Wheel</option>
                  <option>Rank</option>
                </select>

              </div>


              {/* Tournament Size */}

              {parentSelection === "Tournament" && (
                <div className="form-group">

                  <label>
                    Tournament Size

                    {showInfo(
                      "tournamentSize",
                      "Number of individuals competing in each tournament."
                    )}
                  </label>

                  <input
                    type="number"
                    min="2"
                    max={populationSize}
                    value={tournamentSize}
                    onChange={(e) =>
                      setTournamentSize(
                        Math.min(
                          populationSize,
                          Math.max(2, Number(e.target.value))
                        )
                      )
                    }
                  />

                </div>
              )}


              {/* Crossover Type */}

              <div className="form-group">

                <label>
                  Crossover Type

                  {showInfo(
                    "crossoverType",
                    "Method used to combine two parent binary genomes."
                  )}
                </label>

                <select
                  value={crossoverType}
                  onChange={(e) =>
                    setCrossoverType(e.target.value)
                  }
                >
                  <option>One Point</option>
                  <option>Two Point</option>
                  <option>Uniform</option>
                </select>

              </div>


              {/* Crossover Rate */}

              <div className="form-group">

                <label>
                  Crossover Rate

                  {showInfo(
                    "crossoverRate",
                    "Probability that crossover is performed on a pair of parents."
                  )}
                </label>

                <input
                  type="number"
                  min="0"
                  max="1"
                  step="0.05"
                  value={crossoverRate}
                  onChange={(e) =>
                    setCrossoverRate(
                      Math.min(
                        1,
                        Math.max(0, Number(e.target.value))
                      )
                    )
                  }
                />

              </div>


              {/* Mutation Type */}

              <div className="form-group">

                <label>
                  Mutation Type

                  {showInfo(
                    "mutationType",
                    "Mutation operator applied to offspring. Bit Flip independently flips genome bits according to the mutation rate."
                  )}
                </label>

                <select
                  value={mutationType}
                  onChange={(e) =>
                    setMutationType(e.target.value)
                  }
                >
                  <option>Flip Bit</option>
                </select>

              </div>


              {/* Mutation Rate */}

              <div className="form-group">

                <label>
                  Mutation Rate

                  {showInfo(
                    "mutationRate",
                    "Probability used by the Flip Bit mutation operator for each bit."
                  )}
                </label>

                <input
                  type="number"
                  min="0"
                  max="1"
                  step="0.01"
                  value={mutationRate}
                  onChange={(e) =>
                    setMutationRate(
                      Math.min(
                        1,
                        Math.max(0, Number(e.target.value))
                      )
                    )
                  }
                />

              </div>


              {/* Elite Count */}

              <div className="form-group">

                <label>
                  Elite Count

                  {showInfo(
                    "eliteCount",
                    "Number of best individuals preserved when moving to the next generation."
                  )}
                </label>

                <input
                  type="number"
                  min="0"
                  max={populationSize}
                  value={eliteCount}
                  onChange={(e) =>
                    setEliteCount(
                      Math.min(
                        populationSize,
                        Math.max(0, Number(e.target.value))
                      )
                    )
                  }
                />

              </div>


              {/* Target Fitness */}

              <div className="form-group">

                <label>
                  Target Fitness

                  {showInfo(
                    "targetFitness",
                    "Optional fitness target. The run can stop early when the target is reached."
                  )}
                </label>

                <input
                  type="number"
                  min="0"
                  step="0.01"
                  value={targetFitness}
                  onChange={(e) =>
                    setTargetFitness(
                      Math.max(0, Number(e.target.value))
                    )
                  }
                />

              </div>

            </div>
          </div>

        </div>


        {/* ======================================================
            RIGHT PANEL
        ====================================================== */}

        <div className="right-panel">

          {/* ====================================================
              Genome Preview
          ==================================================== */}

          <div className="config-card">

            <div className="card-title">
              <FaDna />
              <h2>Binary Genome Preview</h2>
            </div>

            <div className="genome-preview">

              {Array.from(
                { length: Math.min(genomeLength, 20) },
                (_, index) => (
                  <span
                    className="genome-bit"
                    key={index}
                  >
                    {index % 2 === 0 ? "1" : "0"}
                  </span>
                )
              )}

              {genomeLength > 20 && (
                <span className="genome-more">
                  ...
                </span>
              )}

            </div>

            <p className="preview-description">
              Genome length: <strong>{genomeLength}</strong> bits
            </p>

          </div>


          {/* ====================================================
              Configuration Summary
          ==================================================== */}

          <div className="config-card">

            <div className="card-title">
              <FaRandom />
              <h2>Configuration Summary</h2>
            </div>

            <div className="stats-grid">

              <div className="stat-box">
                <FaDna className="stat-icon" />
                <h4>Genome</h4>
                <p>{genomeLength} bits</p>
              </div>

              <div className="stat-box">
                <FaUsers className="stat-icon" />
                <h4>Population</h4>
                <p>{populationSize}</p>
              </div>

              <div className="stat-box">
                <FaExchangeAlt className="stat-icon" />
                <h4>Crossover</h4>
                <p>{crossoverRate}</p>
              </div>

              <div className="stat-box">
                <FaRandom className="stat-icon" />
                <h4>Mutation</h4>
                <p>{mutationRate}</p>
              </div>

              <div className="stat-box">
                <FaChartLine className="stat-icon" />
                <h4>Problem</h4>
                <p>
                  {isRegression
                    ? "Regression"
                    : "OneMax"}
                </p>
              </div>

            </div>

          </div>


          {/* ====================================================
              Information
          ==================================================== */}

          <div className="config-card">

            <div className="card-title">
              <HiOutlineInformationCircle />
              <h2>Information</h2>
            </div>

            <p>
              BitGA uses a binary genome. Each individual is
              represented as a sequence of 0s and 1s.
            </p>

            <p>
              The genetic algorithm selects parents, applies
              crossover and mutation, preserves elite individuals,
              and continues until the maximum generation count or
              target fitness is reached.
            </p>

          </div>

        </div>

      </div>


      {/* ========================================================
          Buttons
      ======================================================== */}

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
          onClick={handleRun}
        >
          <FaPlay />
          Run Experiment
        </button>

      </div>

    </div>
  );
};

export default Configuration;