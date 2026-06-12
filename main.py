from dotenv import load_dotenv
import os
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from routes.car_routes import car_bp
import sqlite3
from flask import g

load_dotenv()

DATABASE_PATH = os.getenv("DATABASE_PATH")

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def ensure_db_schema():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS tbl_cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brandName TEXT,
            model TEXT,
            productionYear INTEGER,
            price INTEGER NOT NULL,
            img TEXT
        )
    """)
    existing_columns = [row[1] for row in db.execute("PRAGMA table_info(tbl_cars)").fetchall()]
    if "img" not in existing_columns:
        db.execute("ALTER TABLE tbl_cars ADD COLUMN img TEXT")
    db.commit()

def create_app():
    app = Flask(__name__)
    app.get_db = get_db

    upload_folder = os.getenv("UPLOAD_FOLDER")
    app.config["UPLOAD_FOLDER"] = upload_folder
    app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

    os.makedirs(upload_folder, exist_ok=True)

    app.config["DATABASE_PATH"] = os.getenv("DATABASE_PATH")

    app.register_blueprint(car_bp)

    app.teardown_appcontext(close_db)

    with app.app_context():
        ensure_db_schema()

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({
            "error": error.name,
            "message": error.description,
            "status_code": error.code
        }), error.code

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)