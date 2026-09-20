import React, { useState, useEffect } from "react";
import "./Wiki.css";

import {
  WIKI_SECTIONS,
  PARADIGM_CARDS,
  HOW_IT_WORKS,
  KEY_CONCEPTS,
  OPERATORS,
  PLAYGROUND_GUIDES
} from "./wikiMock";

export default function Wiki({ onNavigate, initialSection = "overview" }) {
  const [activeSection, setActiveSection] = useState(initialSection);
  const [expandedConcept, setExpandedConcept] = useState(null);

  useEffect(() => {
    setActiveSection(initialSection);
  }, [initialSection]);

  return (
    <main className="wiki">

      {/* Left Sidebar */}

      <aside className="wiki__sidebar">

        <div className="wiki__sidebar-header">
          <h2>Wiki</h2>

          <p>
            Learn evolutionary computation and
            NeuroSim concepts.
          </p>
        </div>

        <div className="wiki__menu">

          {WIKI_SECTIONS.map((section) => (

            <button
              key={section.id}
              className={`wiki__menu-item ${
                activeSection === section.id
                  ? "wiki__menu-item--active"
                  : ""
              }`}
              onClick={() =>
                setActiveSection(section.id)
              }
            >
              <span>{section.label}</span>

              {section.hasArrow && (
                <span className="wiki__arrow">
                  ›
                </span>
              )}

            </button>

          ))}

        </div>

      </aside>

      {/* Main Content */}

      <section className="wiki__content">
                {activeSection === "overview" && (
          <>

            {/* ==========================
                HERO
            ========================== */}

            <section className="wiki__hero">

              <span className="wiki__badge">
                NeuroSim Documentation
              </span>

              <h1 className="wiki__hero-title">
                Evolutionary Computation Wiki
              </h1>

              <p className="wiki__hero-description">

                Welcome to the official NeuroSim Wiki.

                Learn the theory behind Evolutionary
                Computation, understand optimization
                algorithms, and explore interactive
                playgrounds designed for students,
                researchers and developers.

              </p>

            </section>

            {/* ==========================
                OVERVIEW
            ========================== */}

            <section className="wiki__section">

              <h2 className="wiki__heading">
                What is Evolutionary Computation?
              </h2>

              <p className="wiki__text">

                Evolutionary Computation is a family of
                optimization algorithms inspired by
                biological evolution.

                Instead of finding a solution directly,
                these algorithms improve a population of
                candidate solutions generation by
                generation.

              </p>

              <p className="wiki__text">

                NeuroSim provides an interactive platform
                to visualize every stage of evolution,
                including initialization, fitness
                evaluation, selection, crossover,
                mutation, replacement and convergence.

              </p>

        </section>
                    {/* ==========================
                EVOLUTIONARY PARADIGMS
            ========================== */}

            <section className="wiki__section">

              <div className="wiki__section-header">

                <h2 className="wiki__heading">
                  Evolutionary Paradigms
                </h2>

                <p className="wiki__subheading">
                  Learn about the four major paradigms
                  supported by NeuroSim.
                </p>

              </div>

              <div className="wiki__cards">

                {PARADIGM_CARDS.map((card) => (

                  <div
                    key={card.id}
                    className="wiki__card"
                    style={{
                      borderTop: `4px solid ${card.color}`,
                    }}
                  >

                    <div className="wiki__card-header">

                      <div
                        className="wiki__card-icon"
                        style={{
                          background: card.colorDim,
                          color: card.color,
                        }}
                      >
                        {card.icon}
                      </div>

                      <div>

                        <h3
                          className="wiki__card-title"
                          style={{ color: card.color }}
                        >
                          {card.title}
                        </h3>

                      </div>

                    </div>

                    <p className="wiki__card-description">
                      {card.desc}
                    </p>

                    <button
                      className="wiki__card-link"
                      style={{ color: card.color }}
                      onClick={() => setActiveSection(card.id)}
                    >
                      {card.linkLabel}
                    </button>

                  </div>

                ))}

              </div>

            </section>
                        {/* ==========================
                HOW EVOLUTION WORKS
            ========================== */}

            <section className="wiki__section">

              <div className="wiki__section-header">

                <h2 className="wiki__heading">
                  How Evolution Works
                </h2>

                <p className="wiki__subheading">
                  Every evolutionary algorithm follows
                  a similar optimization cycle.
                </p>

              </div>

              <div className="wiki__flow">

                {HOW_IT_WORKS.map((step, index) => (

                  <React.Fragment key={step.label}>

                    <div className="wiki__flow-card">

                      <div className="wiki__flow-number">
                        {index + 1}
                      </div>

                      <h4 className="wiki__flow-title">
                        {step.label}
                      </h4>

                      <p className="wiki__flow-sub">
                        {step.sub}
                      </p>

                    </div>

                    {index !== HOW_IT_WORKS.length - 1 && (
                      <div className="wiki__flow-arrow">
                        →
                      </div>
                    )}

                  </React.Fragment>

                ))}

              </div>

            </section>
            {/* ==========================
                KEY CONCEPTS
            ========================== */}

            <section className="wiki__section">

              <div className="wiki__section-header">

                <h2 className="wiki__heading">
                  Key Concepts
                </h2>

                <p className="wiki__subheading">
                  Important concepts used in
                  Evolutionary Computation.
                </p>

              </div>

              <div className="wiki__concept-grid">

                {KEY_CONCEPTS.map((concept) => (

                  <div
                    key={concept.term}
                    className="wiki__concept-card"
                    onClick={() => {
                      setExpandedConcept(concept);
                      setActiveSection("concept_detail");
                    }}
                    style={{ cursor: "pointer" }}
                  >

                    <h3 className="wiki__concept-title" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                      {concept.term}
                      <span style={{ fontSize: "0.8em", color: "#6b7280" }}>▶</span>
                    </h3>

                    <p className="wiki__concept-description">
                      {concept.def}
                    </p>

                  </div>

                ))}

              </div>

            </section>

          </>
        )}

        {/* ==========================
            GENETIC ALGORITHMS
        ========================== */}

        {activeSection === "ga" && (

  <section className="wiki__section">

    <button
      className="wiki__back-btn"
      onClick={() => setActiveSection("overview")}
    >
      ← Back to Overview
    </button>

    <h1 className="wiki__heading">
      Genetic Algorithms (GA)
    </h1>

    <p className="wiki__text">
      Genetic Algorithms are inspired by natural selection.
      A population of candidate solutions evolves through
      selection, crossover and mutation until an optimal
      solution is found.
    </p>

    <div style={{ margin: "2rem 0", textAlign: "center", background: "#f9fafb", padding: "1.5rem", borderRadius: "12px", border: "1px solid #e5e7eb" }}>
      <img src="/ga_flowchart.jpg" alt="Genetic Algorithm Flowchart" style={{ maxWidth: "100%", maxHeight: "500px", borderRadius: "8px", objectFit: "contain" }} />
    </div>

    <div className="wiki__detail-table">

      <div className="wiki__detail-row">
        <strong>Representation</strong>
        <span>Binary strings, vectors, graphs</span>
      </div>

      <div className="wiki__detail-row">
        <strong>Selection</strong>
        <span>Tournament, Roulette Wheel, Rank</span>
      </div>

      <div className="wiki__detail-row">
        <strong>Crossover</strong>
        <span>Single Point, Two Point, Uniform</span>
      </div>

      <div className="wiki__detail-row">
        <strong>Mutation</strong>
        <span>Bit Flip, Edge Flip, Node Mutation</span>
      </div>

      <div className="wiki__detail-row">
        <strong>Applications</strong>
        <span>
          Optimization, Scheduling,
          Feature Selection,
          Graph Problems,
          Neural Networks
        </span>
      </div>

    </div>

    <button
      className="wiki__open-btn"
      onClick={() => onNavigate("BitGA")}
    >
      Open BitGA Playground →
    </button>

  </section>

)}

                {/* ==========================
            GENETIC PROGRAMMING
        ========================== */}

        {activeSection === "gp" && (

          <section className="wiki__section">

            <button
              className="wiki__back-btn"
              onClick={() => setActiveSection("overview")}
            >
              ← Back to Overview
            </button>

            <h1 className="wiki__heading">
              Genetic Programming (GP)
            </h1>

            <p className="wiki__text">

              Genetic Programming extends Genetic
              Algorithms by evolving executable
              programs instead of fixed chromosomes.

              Candidate solutions are represented as
              tree structures where internal nodes
              are functions and leaf nodes are
              terminals.

            </p>

            <div className="wiki__detail-table">

              <div className="wiki__detail-row">
                <strong>Representation</strong>
                <span>Expression Trees</span>
              </div>

              <div className="wiki__detail-row">
                <strong>Population</strong>
                <span>Programs / Trees</span>
              </div>

              <div className="wiki__detail-row">
                <strong>Crossover</strong>
                <span>Sub-tree Exchange</span>
              </div>

              <div className="wiki__detail-row">
                <strong>Mutation</strong>
                <span>Node & Sub-tree Mutation</span>
              </div>

              <div className="wiki__detail-row">
                <strong>Applications</strong>
                <span>
                  Symbolic Regression,
                  Automatic Programming,
                  Control Systems,
                  Image Processing,
                  Machine Learning
                </span>
              </div>

            </div>

            <button
              className="wiki__open-btn"
              onClick={() => onNavigate("GP")}
            >
              Explore GP →
            </button>

          </section>

        )}
                {/* ==========================
            EVOLUTION STRATEGIES
        ========================== */}

        {activeSection === "es" && (

          <section className="wiki__section">

            <button
              className="wiki__back-btn"
              onClick={() => setActiveSection("overview")}
            >
              ← Back to Overview
            </button>

            <h1 className="wiki__heading">
              Evolution Strategies (ES)
            </h1>

            <p className="wiki__text">

              Evolution Strategies (ES) are optimization
              algorithms designed for continuous-valued
              problems. Unlike traditional Genetic
              Algorithms, ES relies heavily on mutation
              and self-adaptation of strategy parameters
              to improve solutions over generations.

            </p>

            <div className="wiki__detail-table">

              <div className="wiki__detail-row">
                <strong>Representation</strong>
                <span>Real-valued vectors</span>
              </div>

              <div className="wiki__detail-row">
                <strong>Main Operator</strong>
                <span>Gaussian Mutation</span>
              </div>

              <div className="wiki__detail-row">
                <strong>Selection</strong>
                <span>(μ + λ) and (μ, λ)</span>
              </div>

              <div className="wiki__detail-row">
                <strong>Strength</strong>
                <span>
                  Excellent for continuous optimization
                  and parameter tuning.
                </span>
              </div>

              <div className="wiki__detail-row">
                <strong>Applications</strong>
                <span>
                  Robotics,
                  Engineering Design,
                  Hyperparameter Optimization,
                  Reinforcement Learning
                </span>
              </div>

            </div>

            <button
              className="wiki__open-btn"
              onClick={() => onNavigate("ES")}
            >
              Explore ES →
            </button>

          </section>

        )}
                {/* ==========================
            EVOLUTIONARY PROGRAMMING
        ========================== */}

        {activeSection === "ep" && (

          <section className="wiki__section">

            <button
              className="wiki__back-btn"
              onClick={() => setActiveSection("overview")}
            >
              ← Back to Overview
            </button>

            <h1 className="wiki__heading">
              Evolutionary Programming (EP)
            </h1>

            <p className="wiki__text">

              Evolutionary Programming (EP) is an
              evolutionary optimization technique that
              focuses primarily on mutation rather than
              crossover. Originally developed to evolve
              intelligent behavior, EP is particularly
              useful for optimization and adaptive
              decision-making problems.

            </p>

            <div className="wiki__detail-table">

              <div className="wiki__detail-row">
                <strong>Representation</strong>
                <span>Finite State Machines / Real-valued Solutions</span>
              </div>

              <div className="wiki__detail-row">
                <strong>Main Operator</strong>
                <span>Mutation</span>
              </div>

              <div className="wiki__detail-row">
                <strong>Crossover</strong>
                <span>Not typically used</span>
              </div>

              <div className="wiki__detail-row">
                <strong>Selection</strong>
                <span>Stochastic Tournament Selection</span>
              </div>

              <div className="wiki__detail-row">
                <strong>Applications</strong>
                <span>
                  Artificial Intelligence,
                  Pattern Recognition,
                  Control Systems,
                  Scheduling,
                  Optimization
                </span>
              </div>

            </div>

            <button
              className="wiki__open-btn"
              onClick={() => onNavigate("EP")}
            >
              Explore EP →
            </button>

          </section>

        )}
        {activeSection === "concepts" && (

  <section className="wiki__section">

    <button
      className="wiki__back-btn"
      onClick={() => setActiveSection("overview")}
    >
      ← Back to Overview
    </button>

    <h1 className="wiki__heading">
      Key Concepts
    </h1>

    <div className="wiki__concept-grid">

      {KEY_CONCEPTS.map((concept) => (

        <div
          key={concept.term}
          className="wiki__concept-card"
          onClick={() => {
            setExpandedConcept(concept);
            setActiveSection("concept_detail");
          }}
          style={{ cursor: "pointer" }}
        >
          <h3 className="wiki__concept-title" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            {concept.term}
            <span style={{ fontSize: "0.8em", color: "#6b7280" }}>▶</span>
          </h3>

          <p className="wiki__concept-description">
            {concept.def}
          </p>
        </div>

      ))}

    </div>

  </section>

)}
{activeSection === "operators" && (

  <section className="wiki__section">

    <button
      className="wiki__back-btn"
      onClick={() => setActiveSection("overview")}
    >
      ← Back to Overview
    </button>

    <h1 className="wiki__heading">
      Operators
    </h1>

    <div className="wiki__detail-table">

      {OPERATORS.map((op) => (

        <div
          key={op.name}
          className="wiki__detail-row"
        >

          <div className="wiki__operator-left">

            <div className="wiki__operator-name">
              {op.name}
            </div>

            <span
              className={`wiki__operator-badge wiki__badge-${op.type.toLowerCase()}`}
            >
              {op.type}
            </span>

          </div>

          <div className="wiki__operator-description">
            <p style={{ marginBottom: "12px", color: "#374151" }}>{op.desc}</p>
            {op.example && (
              <p style={{ fontSize: "0.95em", color: "#1e3a8a", backgroundColor: "#eff6ff", padding: "10px", borderRadius: "6px", borderLeft: "4px solid #3b82f6" }}>
                {op.example}
              </p>
            )}
          </div>

        </div>

      ))}

    </div>

  </section>

)}
{activeSection === "guides" && (

<section className="wiki__section">

  <button
    className="wiki__back-btn"
    onClick={() => setActiveSection("overview")}
  >
    ← Back to Overview
  </button>

  <h1 className="wiki__heading">
    Playground Guides
  </h1>

  <div className="wiki__guides">

    {PLAYGROUND_GUIDES.map((guide) => (

      <div
        key={guide.title}
        className="wiki__guide-card"
      >

        <h2>{guide.title}</h2>

        <ol>
          {guide.steps.map((step, index) => (
            <li key={index}>{step}</li>
          ))}
        </ol>

        <div className="wiki__guide-footer">

          <button
            className="wiki__open-btn"
            onClick={() => onNavigate(guide.title)}
          >
            Open {guide.title}
          </button>

        </div>

      </div>

    ))}

  </div>

</section>

)}


        {/* GP, ES, EP, Operators and Guides will be added here */}

        {/* ==========================
            CONCEPT DETAIL PAGE
        ========================== */}
        {activeSection === "concept_detail" && expandedConcept && (
          <section className="wiki__section">
            <button
              className="wiki__back-btn"
              onClick={() => setActiveSection("concepts")}
            >
              ← Back to Key Concepts
            </button>

            <h1 className="wiki__heading">
              {expandedConcept.term}
            </h1>

            <div className="wiki__concept-detail-content" style={{ marginTop: "2rem" }}>
              <div style={{ marginBottom: "2rem" }}>
                <h2 style={{ fontSize: "1.25rem", color: "#4f46e5", marginBottom: "0.5rem" }}>Definition & Context</h2>
                <p style={{ fontSize: "1.1rem", color: "#374151", lineHeight: "1.6", whiteSpace: "pre-line" }}>{expandedConcept.detailedDef}</p>
              </div>

              {expandedConcept.image && (
                <div style={{ marginBottom: "2rem", padding: "1.5rem", background: "#f9fafb", borderRadius: "12px", textAlign: "center", border: "1px solid #e5e7eb" }}>
                  <img src={expandedConcept.image} alt={expandedConcept.term} style={{ maxWidth: "100%", maxHeight: "300px", borderRadius: "8px", objectFit: "contain" }} />
                </div>
              )}

              {expandedConcept.practicalExample && (
                <div style={{ padding: "1.5rem", background: "#eff6ff", borderRadius: "12px", border: "1px solid #bfdbfe" }}>
                  <h2 style={{ fontSize: "1.25rem", color: "#1d4ed8", marginBottom: "0.75rem" }}>Diagram Explanation & Example</h2>
                  <p style={{ fontSize: "1.05rem", color: "#1e3a8a", lineHeight: "1.6" }}>{expandedConcept.practicalExample}</p>
                </div>
              )}
            </div>
          </section>
        )}

      </section>

    </main>
  );
}