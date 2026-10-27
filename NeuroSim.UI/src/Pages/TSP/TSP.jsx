import { FaRoute, FaArrowLeft, FaTools } from "react-icons/fa";

export default function TSP({ onNavigate }) {
  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      height: "100%",
      padding: "40px",
      textAlign: "center",
      background: "#13111f",
      color: "#ffffff"
    }}>
      <div style={{
        background: "rgba(59, 130, 246, 0.1)",
        color: "#3b82f6",
        borderRadius: "50%",
        width: "80px",
        height: "80px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        marginBottom: "24px",
        fontSize: "36px"
      }}>
        <FaRoute />
      </div>
      <h1 style={{ fontSize: "28px", fontWeight: "600", marginBottom: "16px" }}>
        Traveling Salesman Problem (TSP)
      </h1>
      <div style={{
        display: "flex",
        alignItems: "center",
        gap: "8px",
        background: "rgba(245, 158, 11, 0.1)",
        color: "#f59e0b",
        padding: "8px 16px",
        borderRadius: "20px",
        fontSize: "14px",
        fontWeight: "500",
        marginBottom: "24px"
      }}>
        <FaTools />
        <span>Module in Development (Phase 2)</span>
      </div>
      <p style={{
        maxWidth: "500px",
        lineHeight: "1.6",
        color: "#9998a9",
        marginBottom: "32px",
        fontSize: "16px"
      }}>
        The TSP playground is designed to visualize evolutionary route optimizations, showing how crossover and mutation strategies solve NP-hard routing tasks. This module is under active construction.
      </p>
      <button 
        onClick={() => onNavigate("Home")}
        style={{
          background: "#3b82f6",
          color: "white",
          border: "none",
          padding: "12px 24px",
          borderRadius: "8px",
          cursor: "pointer",
          fontSize: "15px",
          fontWeight: "500",
          display: "flex",
          alignItems: "center",
          gap: "8px",
          transition: "background 0.2s"
        }}
        onMouseOver={(e) => e.target.style.background = "#2563eb"}
        onMouseOut={(e) => e.target.style.background = "#3b82f6"}
      >
        <FaArrowLeft />
        Back to Home
      </button>
    </div>
  );
}