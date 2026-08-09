from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from graph.graph import agent
from database.database import init_db, save_task, get_tasks, clear_tasks


app = FastAPI(
    title="Tool Agent API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize SQLite database
init_db()


@app.get("/")
def root():

    return {
        "message": "Tool Agent API is running"
    }


@app.post("/tasks")
def process_task(payload: dict):

    task = payload.get("task")

    if not task:

        return {
            "error": "Task is required"
        }

    try:

        # Run LangGraph
        result = agent.invoke({
            "task": task,
            "tool": "",
            "result": "",
            "steps": []
        })

        # Save to SQLite
        task_id = save_task(
            task=task,
            tool=result["tool"],
            result=result["result"],
            steps=result["steps"]
        )

        return {
            "id": task_id,
            "task": task,
            "tool": result["tool"],
            "result": result["result"],
            "steps": result["steps"]
        }

    except Exception as e:

        return {
            "task": task,
            "error": str(e),
            "steps": []
        }


@app.get("/tasks")
def get_history():

    return get_tasks()


@app.delete("/tasks")
def delete_task_history():

    clear_tasks()

    return {
        "message": "Task history cleared successfully"
    }