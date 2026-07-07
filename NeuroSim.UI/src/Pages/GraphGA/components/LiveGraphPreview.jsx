import CytoscapeComponent from "react-cytoscapejs";
import { generateRandomGraph } from "../utils/graphGenerator";

const LiveGraphPreview = ({
  nodeCount,
  graphMode,
  allowSelfLoop,
  graphVersion,
}) => {

  // Generate graph using shared utility
  const { elements } = generateRandomGraph(
    nodeCount,
    allowSelfLoop
  );

  return (
    <CytoscapeComponent
      key={graphVersion}
      elements={elements}
      style={{
        width: "100%",
        height: "320px",
      }}
      layout={{
        name: "cose",
        fit: true,
        animate: true,
        padding: 30,
      }}
      zoom={1}
      minZoom={0.5}
      maxZoom={2}
      stylesheet={[
        {
          selector: "node",
          style: {
            label: "data(label)",
            backgroundColor: "#7C3AED",
            color: "#ffffff",
            "text-valign": "center",
            "text-halign": "center",
            width: 35,
            height: 35,
            "font-size": 12,
          },
        },
        {
          selector: "edge",
          style: {
            width: 2,
            "line-color": "#94A3B8",
            "target-arrow-color": "#94A3B8",
            "curve-style": "bezier",
            "target-arrow-shape":
              graphMode === "Directed"
                ? "triangle"
                : "none",
          },
        },
      ]}
    />
  );
};

export default LiveGraphPreview;