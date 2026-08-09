# Tool Agent

A simple tool-based agent built with **LangGraph, FastAPI, React, and SQLite**.

The application accepts a user task, routes it to the appropriate tool using conditional routing, executes the tool, stores the result, and displays the result, task history, and execution steps.

## Project Structure

```text
tool-agent/
├── backend/
│   ├── main.py
│   ├── graph.py
│   ├── tools.py
│   ├── database.py
│   ├── requirements.txt
│   └── tasks.db
│
├── frontend/
│   ├── package.json
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       └── main.jsx
│
└── README.md
```

## Dependencies

### Backend

* Python 3.10+
* FastAPI
* Uvicorn
* LangGraph
* LangChain Core
* SQLite

SQLite is included with Python, so no separate database installation is required.

### Frontend

* Node.js 18+
* React
* Vite



Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Backend

Navigate to the backend:

```bash
cd backend/src
```

Start the API:

```bash
uvicorn main:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

The SQLite database is created automatically when the application starts.

## Run the Frontend

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## Available Tools

### TextProcessorTool

Supports:

* Uppercase
* Lowercase
* Word count
* Character count
* Reverse

Example:

```text
Convert hello world to uppercase
```

### CalculatorTool

Supports basic arithmetic:

```text
Calculate 25 + 15
```

Result:

```text
40
```

### WeatherMockTool

Returns predefined mock weather without calling an external API.

Example:

```text
What is the weather in Toronto?
```

## Assumptions and Tradeoffs

* **Conditional routing instead of an LLM:** The application uses deterministic keyword-based routing because there are only three predefined tools. This avoids external LLM dependencies and API costs.
* **Mock weather:** Weather data is intentionally static because the requirement specifies that no external weather API is needed.
* **SQLite:** SQLite was selected for simple persistent storage without requiring a separate database server.
* **Keyword extraction:** Task parsing is intentionally simple and supports the expected task patterns rather than arbitrary natural-language instructions.
* **Single-process application:** The current implementation is intended for a local/demo assignment rather than a production multi-user deployment.

## Time Spent

Approximately **4–5 hours**, including:

* Tool implementation
* LangGraph workflow and conditional routing
* FastAPI backend
* React UI
* SQLite persistence
* Execution-step tracking
* Testing and documentation

## What I Would Improve With More Time

1. Replace keyword-based routing with a structured intent/router model for more flexible natural-language tasks.
2. Add comprehensive unit and integration tests.
3. Improve error handling and validation on both frontend and backend.
4. Add pagination and filtering to task history.
5. Add timestamps and execution duration for each graph step.
6. Add Docker support for easier setup and deployment.
7. Add authentication if the application were exposed to multiple users.
8. Add production-grade database handling and migrations.
9. Add LangSmith tracing for more detailed agent observability.
10. Improve the UI with better loading, error, and execution-state indicators.
