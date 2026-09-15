import { useState } from "react";

import ParadigmSelection from "./ParadigmSelection";
import ProblemSelection from "./ProblemSelection";
import Configuration from "./Configuration";
import Results from "./Results";

const BitGA = () => {
  const [step, setStep] = useState(1);

  const [selectedParadigm, setSelectedParadigm] = useState("GA");
  const [selectedProblem, setSelectedProblem] = useState("onemax");
  const [results, setResults] = useState(null);

  // ------------------------------------------------------------
  // Step 1 → Paradigm
  // ------------------------------------------------------------

  const handleParadigmSelect = (paradigm) => {
    setSelectedParadigm(paradigm);
    setStep(2);
  };

  // ------------------------------------------------------------
  // Step 2 → Problem
  // ------------------------------------------------------------

  const handleProblemSelect = (problem) => {
    setSelectedProblem(problem);
    setStep(3);
  };

  // ------------------------------------------------------------
  // Step 3 → Configuration / Run
  // ------------------------------------------------------------

  const handleRun = async (config) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/bitga/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(config),
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error("BitGA run error:", errorData);
        throw new Error(JSON.stringify(errorData));
      }

      const data = await response.json();

      setResults(data);
      setStep(5);
    } catch (error) {
      console.error("BitGA run error:", error);
      alert("Failed to run BitGA experiment.Check the browser console.");
    }
  };

  // ------------------------------------------------------------
  // Back buttons
  // ------------------------------------------------------------

  const handleBackToParadigm = () => {
    setStep(1);
  };

  const handleBackToProblem = () => {
    setStep(2);
  };

  const handleBackToConfiguration = () => {
    setStep(3);
  };

  // ------------------------------------------------------------
  // Render current step
  // ------------------------------------------------------------

  return (
    <>
      {step === 1 && (
        <ParadigmSelection
          onSelect={handleParadigmSelect}
        />
      )}

      {step === 2 && (
        <ProblemSelection
          selectedParadigm={selectedParadigm}
          selectedProblem={selectedProblem}
          onSelect={handleProblemSelect}
          back={handleBackToParadigm}
        />
      )}

      {step === 3 && (
        <Configuration
          selectedParadigm={selectedParadigm}
          selectedProblem={selectedProblem}
          back={handleBackToProblem}
          onRun={handleRun}
        />
      )}

      {step === 5 && (
        <Results
          results={results}
          back={handleBackToConfiguration}
        />
      )}
    </>
  );
};

export default BitGA;