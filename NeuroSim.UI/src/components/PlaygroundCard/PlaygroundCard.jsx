import "./PlaygroundCard.css";

function PlaygroundCard({ title, description }) {
  return (
    <div className="playground-card">
      <h2>{title}</h2>

      <p>{description}</p>

      <button>Open</button>
    </div>
  );
}

export default PlaygroundCard;