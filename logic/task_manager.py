import sqlite3
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

class TaskManager:
    """
    Aufgabenverwaltung für To-Do-App.
    Speichert Aufgaben ausschließlich in SQLite mit erweiterten Feldern.
    """

    def __init__(self, path="data/tasks.db"):
        self.path = Path(path)
        self.path.parent.mkdir(exist_ok=True)
        try:
            self.conn = sqlite3.connect(self.path)
            self.conn.row_factory = sqlite3.Row
            self._ensure_table()
            logging.info(f"Connected to SQLite DB at {self.path}")
        except Exception as e:
            logging.error(f"Error connecting to SQLite DB at {self.path}: {e}")

        self.tasks = self._load_sqlite()

    def _ensure_table(self):
        try:
            cur = self.conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    done INTEGER NOT NULL CHECK(done IN (0,1)),
                    tag TEXT,
                    due_date TEXT,
                    priority TEXT,
                    created_at TEXT
                )
            """)
            self.conn.commit()
            logging.info("Ensured tasks table exists in SQLite.")
        except Exception as e:
            logging.error(f"Error creating tasks table in SQLite: {e}")

    def _load_sqlite(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM tasks ORDER BY id")
            rows = cur.fetchall()
            tasks = [
                {
                    "id": r["id"],
                    "title": r["title"],
                    "done": bool(r["done"]),
                    "tag": r["tag"],
                    "due_date": r["due_date"],
                    "priority": r["priority"],
                    "created_at": r["created_at"]
                }
                for r in rows
            ]
            logging.info(f"Loaded {len(tasks)} tasks from SQLite.")
            return tasks
        except Exception as e:
            logging.error(f"Error loading tasks from SQLite: {e}")
            return []

    def _insert_sqlite(self, title, tag, due_date, priority):
        try:
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO tasks (title, done, tag, due_date, priority, created_at) VALUES (?, 0, ?, ?, ?, ?)",
                (title, tag, due_date, priority, created_at)
            )
            self.conn.commit()
            logging.info(f"Inserted task '{title}' into SQLite.")
        except Exception as e:
            logging.error(f"Error inserting task into SQLite: {e}")

    def _update_sqlite(self, task_id, title, tag, due_date, priority):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "UPDATE tasks SET title=?, tag=?, due_date=?, priority=? WHERE id=?",
                (title, tag, due_date, priority, task_id)
            )
            self.conn.commit()
            logging.info(f"Updated task id {task_id} in SQLite.")
        except Exception as e:
            logging.error(f"Error updating task in SQLite: {e}")

    def _delete_sqlite(self, task_id):
        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
            self.conn.commit()
            logging.info(f"Deleted task id {task_id} from SQLite.")
        except Exception as e:
            logging.error(f"Error deleting task from SQLite: {e}")

    def _toggle_sqlite(self, task_id, new_done):
        try:
            cur = self.conn.cursor()
            cur.execute("UPDATE tasks SET done=? WHERE id=?", (int(new_done), task_id))
            self.conn.commit()
            logging.info(f"Toggled done={new_done} for task id {task_id} in SQLite.")
        except Exception as e:
            logging.error(f"Error toggling task in SQLite: {e}")

    def add(self, title, tag, due_date, priority):
        self._insert_sqlite(title, tag, due_date, priority)
        self.tasks = self._load_sqlite()

    def edit(self, task_id, title, tag, due_date, priority):
        self._update_sqlite(task_id, title, tag, due_date, priority)
        self.tasks = self._load_sqlite()

    def delete(self, task_id):
        self._delete_sqlite(task_id)
        self.tasks = self._load_sqlite()

    def toggle_done(self, task_id):
        for t in self.tasks:
            if t.get("id") == task_id:
                new_done = not t["done"]
                self._toggle_sqlite(task_id, new_done)
                break
        self.tasks = self._load_sqlite()
