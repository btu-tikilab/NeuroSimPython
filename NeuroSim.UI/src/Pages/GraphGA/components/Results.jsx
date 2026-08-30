import { useEffect, useState } from "react";
import CytoscapeComponent from "react-cytoscapejs";
import { FaArrowLeft, FaNetworkWired, FaChartLine, FaCheckCircle, FaHashtag } from "react-icons/fa";
import "./Results.css";

export default function Results({ runResult, bestGenome, history, back, config }) {
  const [cyElements, setCyElements] = useState([]);

  useEffect(() => {
    if (bestGenome && bestGenome.nodes) {
      const nodes = bestGenome.nodes.map((n) => ({
        data: {
          id: n.id,
          label: `${n.id.toUpperCase()} (${n.value === 1 ? "Active" : "Off"})`,
          type: n.type,
          value: n.value,
        },
      }));

      const edges = bestGenome.edges.map((e, idx) => ({
        data: {
          id: `edge-${idx}`,
          source: e.source,
          target: e.target,
          weight: e.weight,
        },
      }));

      setCyElements([...nodes, ...edges]);
    }
  }, [bestGenome]);

  // Calculate SVG dimensions for the history chart
  const padding = 40;
  const width = 500;
  const height = 220;

  let pointsStr = "";
  let avgPointsStr = "";
  if (history && history.length > 0) {
    const maxGen = history.length - 1;
    const maxFit = Math.max(...history.map((h) => h.bestFitness), 1.0);
    const minFit = Math.min(...history.map((h) => h.worstFitness), 0.0);
    const fitRange = maxFit - minFit || 1.0;

    pointsStr = history
      .map((h, i) => {
        const x = padding + (i / maxGen) * (width - 2 * padding);
        const y = height - padding - ((h.bestFitness - minFit) / fitRange) * (height - 2 * padding);
        return `${x},${y}`;
      })
      .join(" ");

    avgPointsStr = history
      .map((h, i) => {
        const x = padding + (i / maxGen) * (width - 2 * padding);
        const y = height - padding - ((h.avgFitness - minFit) / fitRange) * (height - 2 * padding);
        return `${x},${y}`;
      })
      .join(" ");
  }

  // Calculate stats
  const activeNodesCount = bestGenome?.nodes?.filter((n) => n.value === 1).length || 0;
  const totalNodesCount = bestGenome?.nodes?.length || 0;
  const edgesCount = bestGenome?.edges?.length || 0;
  const density = totalNodesCount > 1 
    ? (edgesCount / (config.graphMode === "Directed" ? (totalNodesCount * (totalNodesCount - 1)) : (totalNodesCount * (totalNodesCount - 1) / 2))).toFixed(3)
    : "0.000";

  return (
    <div className="results-page">
      <div className="breadcrumb">Home &gt; GraphGA &gt; Results</div>

      <div className="results-header-section">
        <div>
          <h1 className="page-title">Run Results</h1>
          <p className="page-description">Analysis and visualization of the optimized Graph GA run.</p>
        </div>
        <button className="back-to-config-btn" onClick={back}>
          <FaArrowLeft /> Edit Configuration
        </button>
      </div>

      <div className="section-divider"></div>

      {/* Overview Cards */}
      <div className="metrics-grid">
        <div className="metric-card premium-card">
          <div className="metric-icon-wrapper fitness-bg">
            <FaCheckCircle className="metric-icon" />
          </div>
          <div className="metric-info">
            <h4>Best Fitness</h4>
            <p className="metric-value">{runResult.bestFitness?.toFixed(2)}</p>
          </div>
        </div>

        <div className="metric-card premium-card">
          <div className="metric-icon-wrapper avg-bg">
            <FaChartLine className="metric-icon" />
          </div>
          <div className="metric-info">
            <h4>Avg Fitness</h4>
            <p className="metric-value">{runResult.avgFitness?.toFixed(2)}</p>
          </div>
        </div>

        <div className="metric-card premium-card">
          <div className="metric-icon-wrapper gen-bg">
            <FaHashtag className="metric-icon" />
          </div>
          <div className="metric-info">
            <h4>Generations</h4>
            <p className="metric-value">{runResult.generation}</p>
          </div>
        </div>
      </div>

      {/* Main content split */}
      <div className="results-layout">
        {/* Left column: Visualizer */}
        <div className="left-column">
          <div className="visualizer-card">
            <div className="card-title">
              <FaNetworkWired />
              <h2>Best Genome Visualization</h2>
            </div>
            <div className="cytoscape-container">
              {cyElements.length > 0 && (
                <CytoscapeComponent
                  elements={cyElements}
                  style={{ width: "100%", height: "350px" }}
                  layout={{
                    name: "cose",
                    fit: true,
                    animate: true,
                    padding: 20,
                  }}
                  zoom={1}
                  minZoom={0.5}
                  maxZoom={2.0}
                  stylesheet={[
                    {
                      selector: "node",
                      style: {
                        label: "data(label)",
                        backgroundColor: (ele) => (ele.data("value") === 1 ? "#10B981" : "#EF4444"),
                        color: "#FFFFFF",
                        "text-valign": "bottom",
                        "text-margin-y": 6,
                        width: 25,
                        height: 25,
                        "font-size": 10,
                        "text-background-opacity": 0.7,
                        "text-background-color": "#1E293B",
                        "text-background-padding": "3px",
                        "text-background-shape": "roundrectangle",
                      },
                    },
                    {
                      selector: "edge",
                      style: {
                        width: 2,
                        "line-color": "#6366F1",
                        "target-arrow-color": "#6366F1",
                        "curve-style": "bezier",
                        "target-arrow-shape": config.graphMode === "Directed" ? "triangle" : "none",
                      },
                    },
                  ]}
                />
              )}
            </div>
          </div>

          <div className="stats-card">
            <div className="card-title">
              <h2>Graph Properties</h2>
            </div>
            <div className="stats-list">
              <div className="stat-row">
                <span>Total Nodes:</span>
                <strong>{totalNodesCount}</strong>
              </div>
              <div className="stat-row">
                <span>Active Nodes (On):</span>
                <strong className="text-green">{activeNodesCount}</strong>
              </div>
              <div className="stat-row">
                <span>Inactive Nodes (Off):</span>
                <strong className="text-red">{totalNodesCount - activeNodesCount}</strong>
              </div>
              <div className="stat-row">
                <span>Total Edges:</span>
                <strong>{edgesCount}</strong>
              </div>
              <div className="stat-row">
                <span>Adjacency Density:</span>
                <strong>{density}</strong>
              </div>
            </div>
          </div>
        </div>

        {/* Right column: Charts */}
        <div className="right-column">
          <div className="chart-card">
            <div className="card-title">
              <FaChartLine />
              <h2>Fitness History Trace</h2>
            </div>
            <div className="svg-chart-container">
              {history && history.length > 0 ? (
                <svg width="100%" height={height} viewBox={`0 0 ${width} ${height}`}>
                  {/* Grid Lines */}
                  <line x1={padding} y1={padding} x2={width - padding} y2={padding} stroke="#334155" strokeDasharray="3,3" />
                  <line x1={padding} y1={height / 2} x2={width - padding} y2={height / 2} stroke="#334155" strokeDasharray="3,3" />
                  <line x1={padding} y1={height - padding} x2={width - padding} y2={height - padding} stroke="#475569" strokeWidth="2" />
                  <line x1={padding} y1={padding} x2={padding} y2={height - padding} stroke="#475569" strokeWidth="2" />

                  {/* Lines */}
                  {avgPointsStr && (
                    <polyline fill="none" stroke="#3B82F6" strokeWidth="2" strokeDasharray="4,2" points={avgPointsStr} />
                  )}
                  {pointsStr && (
                    <polyline fill="none" stroke="#10B981" strokeWidth="3" points={pointsStr} />
                  )}

                  {/* Graph Labels */}
                  <text x={padding - 10} y={padding + 5} fill="#94A3B8" fontSize="10" textAnchor="end">
                    {Math.max(...history.map((h) => h.bestFitness), 1.0).toFixed(0)}
                  </text>
                  <text x={padding - 10} y={height - padding + 5} fill="#94A3B8" fontSize="10" textAnchor="end">
                    {Math.min(...history.map((h) => h.worstFitness), 0.0).toFixed(0)}
                  </text>
                  <text x={padding} y={height - padding + 20} fill="#94A3B8" fontSize="10" textAnchor="middle">
                    Gen 0
                  </text>
                  <text x={width - padding} y={height - padding + 20} fill="#94A3B8" fontSize="10" textAnchor="middle">
                    Gen {history.length - 1}
                  </text>
                </svg>
              ) : (
                <p>No history data available.</p>
              )}
              <div className="chart-legend">
                <span className="legend-item"><span className="legend-dot green"></span> Best Fitness</span>
                <span className="legend-item"><span className="legend-dot blue dashed"></span> Average Fitness</span>
              </div>
            </div>
          </div>

          <div className="config-summary-card">
            <div className="card-title">
              <h2>Experiment Parameters</h2>
            </div>
            <div className="summary-grid">
              <div>
                <span>Mode</span>
                <p>{config.graphMode}</p>
              </div>
              <div>
                <span>Self Loops</span>
                <p>{config.allowSelfLoop ? "Enabled" : "Disabled"}</p>
              </div>
              <div>
                <span>Parent Selection</span>
                <p>{config.parentSelection}</p>
              </div>
              <div>
                <span>Crossover</span>
                <p>{config.crossoverType} ({config.crossoverRate * 100}%)</p>
              </div>
              <div>
                <span>Mutation</span>
                <p>{config.mutationType} ({config.mutationRate * 100}%)</p>
              </div>
              <div>
                <span>Elite Count</span>
                <p>{config.eliteCount}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
