import sqlite3
import json
from datetime import datetime, timezone


DB_NAME = "tasks.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            tool TEXT,
            result TEXT,
            steps TEXT,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def clear_tasks():
    conn = get_connection()

    conn.execute("DELETE FROM tasks")

    conn.commit()
    conn.close()

def save_task(task, tool, result, steps):

    executed_at = datetime.now(timezone.utc).isoformat()

    conn = get_connection()

    cursor = conn.execute(
        """
        INSERT INTO tasks
        (task, tool, result, steps, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            task,
            tool,
            result,
            json.dumps(steps),
            executed_at
        )
    )

    task_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return task_id


def get_tasks():

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM tasks
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    tasks = []

    for row in rows:

        tasks.append({
            "id": row["id"],
            "task": row["task"],
            "tool": row["tool"],
            "result": row["result"],
            "steps": json.loads(row["steps"]),
            "created_at": row["created_at"]
        })

    return tasks