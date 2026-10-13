
import "./ParadigmSelection.css";
import { FaArrowRight } from "react-icons/fa";

const PARADIGMS = [
  {
    id: "GA",
    label: "GA",
    name: "Genetic Algorithm",
    color: "#a855f7",
    icon: "⬡",
    desc: "Use a binary genetic algorithm to evolve solutions through selection, crossover, mutation, and elitism.",
    available: true,
  },
  {
    id: "GP",
    label: "GP",
    name: "Genetic Programming",
    color: "#22c55e",
    icon: "⬡",
    desc: "Evolve programs or expressions represented as trees.",
    available: false,
  },
  {
    id: "ES",
    label: "ES",
    name: "Evolution Strategy",
    color: "#3b82f6",
    icon: "⬡",
    desc: "Evolve solutions by strategically perturbing individuals.",
    available: false,
  },
  {
    id: "EP",
    label: "EP",
    name: "Evolutionary Programming",
    color: "#f59e0b",
    icon: "⬡",
    desc: "Evolve populations using mutation-driven search without crossover.",
    available: false,
  },
];

const ParadigmSelection = ({ onSelect }) => {
  const handleSelection = (paradigm) => {
    if (!paradigm.available) return;

    if (onSelect) {
      onSelect(paradigm.id);
    }
  };

  return (
    <div className="paradigm-selection-page">
      <div className="breadcrumb">
        Home &gt; BitGA &gt; Select Paradigm
      </div>

      <h1 className="page-title">BitGA</h1>

      <p className="page-description">
        Graph-based evolutionary computation playground.
      </p>

      <div className="section-divider"></div>

      <h2 className="step-heading">Step 1 : Select Paradigm</h2>

      <p className="step-subheading">
        Choose an evolutionary paradigm to configure and run your experiment.
      </p>

      <div className="paradigm-grid">
        {PARADIGMS.map((p) => (
          <div
            key={p.id}
            className="paradigm-card"
            onClick={() => handleSelection(p)}
          >
            <div
              className="paradigm-icon"
              style={{ color: p.color }}
            >
              {p.id === "GA" && (
                <svg
                  width="48"
                  height="48"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.5"
                >
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z" />
                  <path d="M8 12h8M12 8v8" />
                </svg>
              )}

              {p.id === "GP" && (
                <svg
                  width="48"
                  height="48"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.5"
                >
                  <circle cx="12" cy="5" r="2" />
                  <circle cx="5" cy="19" r="2" />
                  <circle cx="19" cy="19" r="2" />
                  <path d="M12 7v4M12 11l-5 6M12 11l5 6" />
                </svg>
              )}

              {p.id === "ES" && (
                <svg
                  width="48"
                  height="48"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.5"
                >
                  <circle cx="5" cy="12" r="2" />
                  <circle cx="12" cy="12" r="2" />
                  <circle cx="19" cy="12" r="2" />
                  <path d="M7 12h3M14 12h3M5 10V7a2 2 0 012-2h10a2 2 0 012 2v3M5 14v3a2 2 0 002 2h10a2 2 0 002-2v-3" />
                </svg>
              )}

              {p.id === "EP" && (
                <svg
                  width="48"
                  height="48"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.5"
                >
                  <polygon points="12,2 22,20 2,20" />
                </svg>
              )}
            </div>

            <h2 style={{ color: p.color }}>{p.label}</h2>

            <h3>{p.name}</h3>

            <p>{p.desc}</p>

            <button
              type="button"
              disabled={!p.available}
              onClick={(e) => {
                e.stopPropagation();
                handleSelection(p);
              }}
            >
              Select {p.label}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ParadigmSelection;
