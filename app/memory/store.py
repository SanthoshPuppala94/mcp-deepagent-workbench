import json
import sqlite3
from pathlib import Path
from typing import Any

from app.config import DB_PATH


class MemoryStore:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def initialize(self) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS user_memory (
                    user_id TEXT PRIMARY KEY,
                    profile_json TEXT NOT NULL DEFAULT '{}'
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS task_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    task TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def get_user_memory(self, user_id: str) -> dict[str, Any]:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT profile_json FROM user_memory WHERE user_id = ?",
                (user_id,),
            ).fetchone()
        return json.loads(row["profile_json"]) if row else {}

    def save_user_memory(self, user_id: str, profile: dict[str, Any]) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO user_memory (user_id, profile_json)
                VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET profile_json = excluded.profile_json
                """,
                (user_id, json.dumps(profile, sort_keys=True)),
            )

    def save_task_result(self, user_id: str, task: str, answer: str) -> None:
        with self.connect() as conn:
            conn.execute(
                "INSERT INTO task_memory (user_id, task, answer) VALUES (?, ?, ?)",
                (user_id, task, answer),
            )

