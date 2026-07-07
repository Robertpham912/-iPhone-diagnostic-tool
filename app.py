# -*- coding: utf-8 -*-
import json
import os
import sqlite3
import time
from flask import Flask, jsonify, request, render_template, g

from rules import PROBLEMS, categories_summary

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "history.db")

app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS diagnostics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts INTEGER NOT NULL,
            category TEXT NOT NULL,
            problem_id TEXT NOT NULL,
            problem_name TEXT NOT NULL,
            diagnosis_title TEXT NOT NULL,
            severity TEXT NOT NULL,
            path_json TEXT NOT NULL,
            user_agent TEXT
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/problems")
def api_problems():
    """Danh sach van de theo tung nhom, kem loai auto-test neu co."""
    return jsonify(categories_summary())


@app.route("/api/tree/<problem_id>")
def api_tree(problem_id):
    """Tra ve toan bo cay cau hoi cho mot problem cu the."""
    problem = PROBLEMS.get(problem_id)
    if not problem:
        return jsonify({"error": "khong tim thay van de nay"}), 404
    return jsonify({
        "id": problem_id,
        "name": problem["name"],
        "category": problem["category"],
        "auto_test": problem["auto_test"],
        "tree": problem["tree"],
    })


@app.route("/api/log", methods=["POST"])
def api_log():
    """Luu lai mot phien chan doan sau khi nguoi dung di het cay cau hoi."""
    data = request.get_json(force=True, silent=True) or {}
    problem_id = data.get("problem_id")
    path = data.get("path", [])
    diagnosis = data.get("diagnosis", {})

    problem = PROBLEMS.get(problem_id)
    if not problem:
        return jsonify({"error": "problem_id khong hop le"}), 400

    db = get_db()
    db.execute(
        """INSERT INTO diagnostics
           (ts, category, problem_id, problem_name, diagnosis_title, severity, path_json, user_agent)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            int(time.time()),
            problem["category"],
            problem_id,
            problem["name"],
            diagnosis.get("title", ""),
            diagnosis.get("severity", ""),
            json.dumps(path, ensure_ascii=False),
            request.headers.get("User-Agent", ""),
        ),
    )
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/history")
def api_history():
    """Lich su cac lan chan doan gan day (moi nhat truoc)."""
    db = get_db()
    rows = db.execute(
        "SELECT ts, problem_name, diagnosis_title, severity FROM diagnostics ORDER BY ts DESC LIMIT 50"
    ).fetchall()
    return jsonify([dict(r) for r in rows])


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5050, debug=True)
