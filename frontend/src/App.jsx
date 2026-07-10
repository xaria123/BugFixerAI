import { useState } from "react";
import "./App.css";

function App() {
  const [code, setCode] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [historyMessage, setHistoryMessage] = useState("");
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

    async function loadHistory() {
    setHistoryMessage("Loading history...");

    try {
      const response = await fetch("http://127.0.0.1:5000/api/history");
      const data = await response.json();

      setHistory(data.slice(0, 5));
      setHistoryMessage(`Showing latest ${Math.min(data.length, 5)} debug sessions.`);
    } catch (error) {
      setHistory([]);
      setHistoryMessage("Could not load history. Make sure the backend is running.");
    }
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

              <h3>Problem Line</h3>
              <p>{result.line_number ? `Line ${result.line_number}` : "No line number detected"}</p>

              {result.code_analysis && (
                <>
                  <h3>Code Analysis</h3>
                  <p>
                    Valid Python: {result.code_analysis.is_valid_python ? "Yes" : "No"}
                  </p>
                  <p>Function Count: {result.code_analysis.function_count}</p>
                  <p>
                    Detected Functions:{" "}
                    {result.code_analysis.function_names.length > 0
                      ? result.code_analysis.function_names.join(", ")
                      : "None"}
                  </p>
                </>
              )}

              <h3>Explanation</h3>
              <p>{result.explanation}</p>

              <h3>Suggested Fix</h3>
              <pre>{result.fixed_code}</pre>
            </>
          )}
        </div>
      )}

      <div className="history-section">
        <button onClick={loadHistory}>Load History</button>
        {historyMessage && <p className="date">{historyMessage}</p>}

        {history.length > 0 && (
          <div className="history-list">
            <h2>Debugging History</h2>

            {history.map((item) => (
              <div className="history-card" key={item.id}>
                <h3>{item.bug_type}</h3>
                <p className="date">{item.created_at}</p>

                <h4>Original Code</h4>
                <pre>{item.original_code}</pre>

                <h4>Error Message</h4>
                <p>{item.error_message}</p>

                <h4>Suggested Fix</h4>
                <pre>{item.fixed_code}</pre>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;