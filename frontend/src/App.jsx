import "./App.css";
import Upload from "./pages/Upload.jsx";

function App() {
  return (
    <div>
      <nav
        style={{
          padding: 12,
          borderBottom: "1px solid #eee",
          backgroundColor: "#f5f5f5",
        }}
      >
        <h1 style={{ margin: 0, color: "#333" }}>Document Summarizer</h1>
      </nav>
      <Upload />
    </div>
  );
}

export default App;
