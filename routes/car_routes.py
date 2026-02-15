import os
from flask import Blueprint, render_template, request, jsonify, current_app
from static_data.cars import carlist
from werkzeug.utils import secure_filename

car_bp = Blueprint("car_bp", __name__)

@car_bp.route("/")
def home():
    return render_template("index.html", cars=carlist)


@car_bp.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")

    if not query:
        return jsonify(carlist)

    results = [
        car for car in carlist
        if query.lower() in car["name"].lower()
    ]

    return jsonify(results)


@car_bp.route("/add", methods=["POST"])
def add():
    brand = request.form["brand"]
    name = request.form["name"]
    year = int(request.form["year"])
    price = int(request.form["price"])
    file = request.files.get("img")

    upload_folder = current_app.config["UPLOAD_FOLDER"]

    if file and file.filename:
        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        img_path = f"uploads/{filename}"
    else:
        img_path = "default.jpg"

    new_car = {
        "name": name,
        "brand": brand,
        "year": year,
        "price": price,
        "img": img_path
    }

    carlist.append(new_car)

    return jsonify({
        "message": f"{name} {brand} added successfully."
    })
