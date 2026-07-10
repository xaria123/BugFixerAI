import { useState } from "react";
import "./App.css";

function App() {
  const [code, setCode] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleDebug() {
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/debug", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          code: code,
          error_message: errorMessage,
        }),
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({
        error: "Could not connect to the backend. Make sure Flask is running.",
      });
    }

    setLoading(false);
  }

  return (
    <div className="app">
      <h1>BugFixerAI</h1>
      <p className="subtitle">
        Paste your Python code and error message to get a simple bug explanation
        and suggested fix.
      </p>

      <div className="input-section">
        <label>Python Code</label>
        <textarea
          value={code}
          onChange={(event) => setCode(event.target.value)}
          placeholder="Paste your Python code here..."
        />

        <label>Error Message</label>
        <textarea
          value={errorMessage}
          onChange={(event) => setErrorMessage(event.target.value)}
          placeholder="Paste your error message here..."
        />

        <button onClick={handleDebug}>
          {loading ? "Debugging..." : "Debug Code"}
        </button>
      </div>

      {result && (
        <div className="result-card">
          {result.error ? (
            <p className="error">{result.error}</p>
          ) : (
            <>
              <h2>Result</h2>

              <h3>Bug Type</h3>
              <p>{result.bug_type}</p>

              <h3>Explanation</h3>
              <p>{result.explanation}</p>

              <h3>Suggested Fix</h3>
              <pre>{result.fixed_code}</pre>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;