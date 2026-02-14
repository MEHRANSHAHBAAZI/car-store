from dotenv import load_dotenv
from fileinput import filename
import os
from flask import Flask,render_template, request, redirect, url_for, jsonify
from werkzeug.exceptions import HTTPException
from static_data.cars import carlist

app = Flask(__name__)

load_dotenv()

upload_folder = os.getenv("UPLOAD_FOLDER")
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  
os.makedirs(upload_folder, exist_ok=True)

@app.errorhandler(HTTPException)
def handle_http_exception(error):
    return jsonify({
        "error": error.name,
        "message": error.description,
        "status_code": error.code
    }), error.code

@app.route("/")
def home():
    return render_template("index.html", cars=carlist)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    if query is None:
        return []
    
    results = [car for car in carlist if query.lower() in car["name"].lower()]
    return results

@app.route("/add", methods=["POST"])
def add():
    brand = request.form["brand"]
    name = request.form["name"]
    year = int(request.form["year"])
    price = int(request.form["price"])
    file = request.files["img"]

    if file:
        filepath = os.path.join(upload_folder, file.filename)
        file.save(filepath)
        img_path = f"uploads/{file.filename}"
    else:
        img_path = "default.jpg"

    new_car = {"name": name, "brand": brand, "year": year, "price": price, "img": img_path}

    carlist.append(new_car)

    return jsonify({
        "message": f"{name} {brand} added successfully."
    })

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host="0.0.0.0", port=8000, debug=True)

