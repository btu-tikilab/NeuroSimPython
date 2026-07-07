import { useState } from "react";

import ParadigmSelection from "./components/ParadigmSelection";
import ProblemSelection from "./components/ProblemSelection";
import Configuration from "./components/Configuration";

export default function GraphGA() {

  const [step, setStep] = useState(1);
  const [selectedParadigm, setSelectedParadigm] = useState("");
  const [selectedProblem, setSelectedProblem] = useState("");

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
        />
      )}
    </>
  );
}