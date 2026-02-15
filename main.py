from dotenv import load_dotenv
import os
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from routes.car_routes import car_bp

load_dotenv()

def create_app():
    app = Flask(__name__)

    upload_folder = os.getenv("UPLOAD_FOLDER")
    app.config["UPLOAD_FOLDER"] = upload_folder
    app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

    os.makedirs(upload_folder, exist_ok=True)

    # Register blueprint
    app.register_blueprint(car_bp)

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({
            "error": error.name,
            "message": error.description,
            "status_code": error.code
        }), error.code

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
