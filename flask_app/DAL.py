import sqlite3
import os
from typing import List, Dict, Optional


DB_FILENAME = 'projects.db'


def get_db_path() -> str:
    """Return the absolute path to the database file next to this module."""
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, DB_FILENAME)


def init_db() -> None:
    """Create the projects database and table if they don't already exist."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT NOT NULL,
                Description TEXT,
                ImageFileName TEXT,
                CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        conn.commit()
    finally:
        conn.close()


def save_project(title: str, description: str, image_filename: Optional[str] = None) -> int:
    """Insert a project into the database and return the new row id."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO projects (Title, Description, ImageFileName) VALUES (?,?,?)",
            (title, description, image_filename or ""),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def get_all_projects() -> List[Dict]:
    """Return a list of projects as dictionaries."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, Title, Description, ImageFileName, CreatedAt FROM projects ORDER BY id DESC;")
        rows = cur.fetchall()
        projects = []
        for r in rows:
            projects.append(
                {
                    "id": r["id"],
                    "Title": r["Title"],
                    "Description": r["Description"],
                    "ImageFileName": r["ImageFileName"],
                    "CreatedAt": r["CreatedAt"],
                }
            )
        return projects
    finally:
        conn.close()


def get_project_by_id(project_id: int) -> Optional[Dict]:
    """Return a single project dict by id, or None if not found."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, Title, Description, ImageFileName, CreatedAt FROM projects WHERE id=?;", (project_id,))
        row = cur.fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "Title": row["Title"],
            "Description": row["Description"],
            "ImageFileName": row["ImageFileName"],
            "CreatedAt": row["CreatedAt"],
        }
    finally:
        conn.close()


def delete_project(project_id: int) -> None:
    """Delete a project by id."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM projects WHERE id=?;", (project_id,))
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    # Quick CLI helper used for manual testing
    init_db()
    print(f"Initialized DB at: {get_db_path()}")
    print("Existing projects:")
    for p in get_all_projects():
        print(p)
