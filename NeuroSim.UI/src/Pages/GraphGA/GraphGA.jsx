import { useState } from "react";

import ParadigmSelection from "./components/ParadigmSelection";
import ProblemSelection from "./components/ProblemSelection";

export default function GraphGA() {

  const [step, setStep] = useState(1);
  const [selectedParadigm, setSelectedParadigm] = useState("");

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
/>
      )}
    </>
  );
}