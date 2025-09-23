import React, { useState } from "react";

const API_BASE = process.env.REACT_APP_API_BASE_URL;

export default function App() {
  const [mode, setMode] = useState("shorten"); // "shorten" or "analytics"
  const [longUrl, setLongUrl] = useState("");
  const [shortCode, setShortCode] = useState("");
  const [secretKey, setSecretKey] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const toggleMode = () => {
    setMode(mode === "shorten" ? "analytics" : "shorten");
    setResult(null);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      if (mode === "shorten") {
        const res = await fetch(`${API_BASE}/shorten`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ long_url: longUrl }),
        });
        if (!res.ok) throw new Error(`Error ${res.status}`);
        const data = await res.json();
        setResult(data);
      } else {
        const res = await fetch(
          `${API_BASE}/analytics/${shortCode}?analytics_secret=${secretKey}`
        );
        if (!res.ok) throw new Error(`Error ${res.status}`);
        const data = await res.json();
        setResult(data);
      }
    } catch (err) {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        fontFamily: "sans-serif",
        padding: "2rem",
        maxWidth: "600px",
        margin: "auto",
      }}
    >
      <h1 style={{ textAlign: "center" }}>🔗 LinkTrail</h1>
      <button
        onClick={toggleMode}
        style={{
          background: "#2563eb",
          color: "white",
          border: "none",
          padding: "0.5rem 1rem",
          borderRadius: "5px",
          cursor: "pointer",
          marginBottom: "1.5rem",
          display: "block",
          marginLeft: "auto",
          marginRight: "auto",
        }}
      >
        Switch to {mode === "shorten" ? "Analytics" : "Shorten"} Mode
      </button>

      <form onSubmit={handleSubmit}>
        {mode === "shorten" ? (
          <div>
            <label>Enter long URL:</label>
            <input
              type="url"
              required
              value={longUrl}
              onChange={(e) => setLongUrl(e.target.value)}
              placeholder="https://example.com"
              style={{
                width: "100%",
                padding: "0.5rem",
                marginTop: "0.5rem",
                marginBottom: "1rem",
              }}
            />
          </div>
        ) : (
          <>
            <div>
              <label>Shortcode:</label>
              <input
                type="text"
                required
                value={shortCode}
                onChange={(e) => setShortCode(e.target.value)}
                placeholder="abc123"
                style={{
                  width: "100%",
                  padding: "0.5rem",
                  marginTop: "0.5rem",
                  marginBottom: "1rem",
                }}
              />
            </div>
            <div>
              <label>Analytics Secret:</label>
              <input
                type="text"
                required
                value={secretKey}
                onChange={(e) => setSecretKey(e.target.value)}
                placeholder="your-secret"
                style={{
                  width: "100%",
                  padding: "0.5rem",
                  marginTop: "0.5rem",
                  marginBottom: "1rem",
                }}
              />
            </div>
          </>
        )}

        <button
          type="submit"
          disabled={loading}
          style={{
            background: "#10b981",
            color: "white",
            border: "none",
            padding: "0.5rem 1.5rem",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          {loading ? "Loading..." : "Submit"}
        </button>
      </form>

      {error && <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>}

      {result && (
        <div
          style={{
            marginTop: "1.5rem",
            padding: "1rem",
            border: "1px solid #ddd",
            borderRadius: "5px",
            background: "#f9fafb",
          }}
        >
          {mode === "shorten" ? (
            <>
              <p>
                <strong>Short URL:</strong> {API_BASE + "/l/" + result.short_code}
              </p>  
              <p>
                <strong>Shortcode:</strong> {result.short_code}
              </p>
              <p>
                <strong>Secret Key:</strong> {result.analytics_secret}
              </p>
            </>
          ) : (
            <>
              <p>
                <strong>Total Clicks:</strong> {result.total_clicks}
              </p>
              <p>
                <strong>Raw Data:</strong> <pre>{JSON.stringify(result, null, 2)}</pre>
              </p>
            </>
          )}
        </div>
      )}
    </div>
  );
}
