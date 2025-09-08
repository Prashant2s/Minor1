import { useState } from "react";
import api from "../api/axios.js";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const form = new FormData();
      form.append("file", file);
      const res = await api.post("/summarize", form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data);
    } catch (err) {
      setError(err?.response?.data?.error || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 16 }}>
      <h2>Document Summarizer</h2>
      <p>
        Upload a document (PDF, JPG, PNG, TIFF) to get an AI-generated summary
      </p>
      <form onSubmit={onSubmit}>
        <input
          type="file"
          accept=".pdf,.jpg,.jpeg,.png,.tiff,.tif"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
        <button
          type="submit"
          disabled={!file || loading}
          style={{ marginLeft: 8 }}
        >
          {loading ? "Processing..." : "Summarize Document"}
        </button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {result && (
        <div
          style={{
            marginTop: 20,
            padding: 16,
            border: "1px solid #ccc",
            borderRadius: 8,
          }}
        >
          <h3>Summary:</h3>
          <p style={{ fontSize: "16px", lineHeight: "1.5" }}>
            {result.summary}
          </p>
          <hr style={{ margin: "16px 0" }} />
          <p>
            <strong>File Type:</strong> {result.file_type}
          </p>
          <p>
            <strong>Text Length:</strong> {result.extracted_text_length}{" "}
            characters
          </p>
          <p>
            <strong>Processed At:</strong>{" "}
            {new Date(result.processed_at).toLocaleString()}
          </p>
        </div>
      )}
    </div>
  );
}
