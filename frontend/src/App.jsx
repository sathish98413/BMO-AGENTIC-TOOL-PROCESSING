import { useEffect, useState } from "react";
import "./App.css";


function App() {

  const [task, setTask] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);


  // Load history
  const loadHistory = async () => {

    const response = await fetch(
      "http://localhost:8000/tasks"
    );

    const data = await response.json();

    setHistory(data);
  };


  useEffect(() => {
    loadHistory();
  }, []);


  // Submit task
  const submitTask = async () => {

    if (!task.trim()) {
      return;
    }

    setLoading(true);

    try {

      const response = await fetch(
        "http://localhost:8000/tasks",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            task: task
          })
        }
      );

      const data = await response.json();

      setResult(data);

      setHistory((previous) => [
        data,
        ...previous
      ]);

    } finally {

      setLoading(false);
    }
  };


  const selectHistory = (item) => {

    setTask(item.task);

    setResult(item);
  };

  const clearHistory = async () => {

  if (history.length === 0) {
    return;
  }

  const confirmed = window.confirm(
    "Are you sure you want to clear all task history?"
  );

  if (!confirmed) {
    return;
  }

  try {

    const response = await fetch(
      "http://localhost:8000/tasks",
      {
        method: "DELETE"
      }
    );

    if (!response.ok) {
      throw new Error("Failed to clear history");
    }

    // Clear UI history
    setHistory([]);

    // Clear currently displayed result
    setResult(null);

  } catch (error) {

    console.error(error);

    alert("Failed to clear task history");
  }
};


  return (

    <div className="container">

      <h1>
        Tool Agent
      </h1>


      {/* Task Input */}

      <div className="input-section">

        <input
          type="text"
          value={task}
          onChange={(e) =>
            setTask(e.target.value)
          }
          placeholder="Enter a task..."
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              submitTask();
            }
          }}
        />

        <button
          onClick={submitTask}
          disabled={loading}
        >
          {loading ? "Processing..." : "Submit"}
        </button>

      </div>


      {/* Example Tasks */}

      <div className="examples">

        <button
          onClick={() =>
            setTask(
              "Convert hello world to uppercase"
            )
          }
        >
          Text
        </button>

        <button
          onClick={() =>
            setTask("Calculate 25 + 15")
          }
        >
          Calculator
        </button>

        <button
          onClick={() =>
            setTask(
              "What is the weather in Toronto?"
            )
          }
        >
          Weather
        </button>

      </div>


      <div className="content">


        {/* History */}

<div className="history">

  <div className="history-header">

    <h2>
      Task History
    </h2>

    <button
      className="clear-button"
      onClick={clearHistory}
      disabled={history.length === 0}
    >
      Clear History
    </button>

  </div>


  {history.length === 0 && (
    <p>No tasks yet.</p>
  )}


  {history.map((item, index) => (

  <div
    className="history-item"
    key={item.id || index}
    onClick={() => selectHistory(item)}
  >

    <strong>
      {item.task}
    </strong>

    <small>
      Tool: {item.tool}
    </small>

    <small>
      Executed:{" "}
      {new Date(item.created_at).toLocaleString()}
    </small>

  </div>

  ))}

</div>


        {/* Result */}

        <div className="result">

          <h2>
            Result
          </h2>

          {result ? (

            <>

              <div className="result-box">

                {result.result}

              </div>


              <h2>
                Execution Steps
              </h2>


              <div className="steps">

                {result.steps.map(
                  (step, index) => (

                    <div
                      className="step"
                      key={index}
                    >

                      <div>
                        <strong>
                          Step {index + 1}
                        </strong>
                      </div>

                      <div>
                        Tool:{" "}
                        <strong>
                          {step.step}
                        </strong>
                      </div>

                      <div>
                        Input:{" "}
                        {step.input}
                      </div>

                      <div>
                        Output:{" "}
                        {step.output}
                      </div>

                    </div>

                  )
                )}

              </div>

            </>

          ) : (

            <p>
              Submit a task to see the result.
            </p>

          )}

        </div>

      </div>

    </div>
  );
}


export default App;