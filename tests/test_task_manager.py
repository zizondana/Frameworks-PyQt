import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import sqlite3
import pytest
from logic.task_manager import TaskManager

@pytest.fixture
def tmp_sqlite(tmp_path):
    """Erstellt eine temporäre SQLite-Datei für Tests."""
    db_path = tmp_path / "test_tasks.db"
    return str(db_path)

def test_load_empty_db(tmp_sqlite):
    mgr = TaskManager(path=tmp_sqlite)
    assert mgr.tasks == []

def test_add_and_load_sqlite(tmp_sqlite):
    mgr = TaskManager(path=tmp_sqlite)
    mgr.add("Test Task", "Arbeit", "2024-12-31", "Hoch")
    assert len(mgr.tasks) == 1
    task = mgr.tasks[0]
    assert task["title"] == "Test Task"
    assert task["done"] is False
    assert task["tag"] == "Arbeit"
    assert task["due_date"] == "2024-12-31"
    assert task["priority"] == "Hoch"

def test_edit_task_sqlite(tmp_sqlite):
    mgr = TaskManager(path=tmp_sqlite)
    mgr.add("Original Task", "Privat", "2024-01-01", "Niedrig")
    task_id = mgr.tasks[0]["id"]
    mgr.edit(task_id, "Updated Task", "Studium", "2024-06-01", "Mittel")
    task = mgr.tasks[0]
    assert task["title"] == "Updated Task"
    assert task["tag"] == "Studium"
    assert task["due_date"] == "2024-06-01"
    assert task["priority"] == "Mittel"

def test_delete_task_sqlite(tmp_sqlite):
    mgr = TaskManager(path=tmp_sqlite)
    mgr.add("To Be Deleted", "Privat", "2024-05-01", "Mittel")
    task_id = mgr.tasks[0]["id"]
    mgr.delete(task_id)
    assert mgr.tasks == []

def test_toggle_done_sqlite(tmp_sqlite):
    mgr = TaskManager(path=tmp_sqlite)
    mgr.add("Toggle Task", "Arbeit", "2024-07-15", "Niedrig")
    task_id = mgr.tasks[0]["id"]
    mgr.toggle_done(task_id)
    assert mgr.tasks[0]["done"] is True
