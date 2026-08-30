import { useState, useEffect } from "react";

import ParadigmSelection from "./components/ParadigmSelection";
import ProblemSelection from "./components/ProblemSelection";
import Configuration from "./components/Configuration";
import Results from "./components/Results";
import { FaSpinner } from "react-icons/fa";

export default function GraphGA() {
  const [step, setStep] = useState(1);
  const [selectedParadigm, setSelectedParadigm] = useState("");
  const [selectedProblem, setSelectedProblem] = useState("");
  
  // Running state and API result states
  const [config, setConfig] = useState(null);
  const [runResult, setRunResult] = useState(null);
  const [bestGenome, setBestGenome] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const executeExperiment = async (payload) => {
    setConfig(payload);
    setStep(4); // transition to Running step
    setLoading(true);
    setError(null);

    try {
      // 1. Run the GraphGA experiment
      const runRes = await fetch("http://localhost:8000/api/graphga/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!runRes.ok) {
        throw new Error(`Failed to run experiment: ${runRes.statusText}`);
      }

      const runData = await runRes.json();
      setRunResult(runData);

      // 2. Fetch the best genome
      const bestRes = await fetch("http://localhost:8000/api/graphga/best");
      if (!bestRes.ok) {
        throw new Error(`Failed to fetch best genome: ${bestRes.statusText}`);
      }
      const bestData = await bestRes.json();
      setBestGenome(bestData);

      // 3. Fetch the evolution history
      const histRes = await fetch("http://localhost:8000/api/graphga/history");
      if (!histRes.ok) {
        throw new Error(`Failed to fetch history: ${histRes.statusText}`);
      }
      const histData = await histRes.json();
      setHistory(histData);

      // Transition to Results step
      setStep(5);
    } catch (err) {
      console.error(err);
      setError(err.message || "An unexpected error occurred while running the experiment.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {step === 1 && (
        <ParadigmSelection
          onSelect={(paradigm) => {
            setSelectedParadigm(paradigm);
            setStep(2);
          }}
        />
      )}

      {step === 2 && (
        <ProblemSelection
          selectedParadigm={selectedParadigm}
          back={() => setStep(1)}
          next={(problem) => {
            setSelectedProblem(problem);
            setStep(3);
          }}
        />
      )}

      {step === 3 && (
        <Configuration
          selectedParadigm={selectedParadigm}
          selectedProblem={selectedProblem}
          back={() => setStep(2)}
          onRun={executeExperiment}
        />
      )}

      {step === 4 && (
        <div style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          height: "80vh",
          color: "#F8FAFC",
          fontFamily: "Inter, sans-serif"
        }}>
          {loading ? (
            <>
              <FaSpinner className="spinner-icon" style={{
                fontSize: "48px",
                color: "#6366F1",
                animation: "spin 1s linear infinite",
                marginBottom: "20px"
              }} />
              <style>{`
                @keyframes spin {
                  0% { transform: rotate(0deg); }
                  100% { transform: rotate(360deg); }
                }
              `}</style>
              <h2>Evolving Populations...</h2>
              <p style={{ color: "#64748B", marginTop: "8px" }}>
                Running Graph GA optimization on backend server.
              </p>
            </>
          ) : error ? (
            <div style={{ textAlign: "center", maxWidth: "500px", padding: "20px" }}>
              <h2 style={{ color: "#EF4444" }}>Experiment Failed</h2>
              <p style={{ color: "#94A3B8", marginTop: "12px", marginBottom: "20px" }}>{error}</p>
              <button 
                onClick={() => setStep(3)}
                style={{
                  background: "#6366F1",
                  color: "#FFFFFF",
                  border: "none",
                  padding: "10px 20px",
                  borderRadius: "8px",
                  cursor: "pointer",
                  fontWeight: "600"
                }}
              >
                Return to Configuration
              </button>
            </div>
          ) : null}
        </div>
      )}

      {step === 5 && runResult && (
        <Results
          runResult={runResult}
          bestGenome={bestGenome}
          history={history}
          config={config}
          back={() => setStep(3)}
        />
      )}
    </>
  );
}