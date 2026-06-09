import os
from flask import current_app
from werkzeug.utils import secure_filename



carlist = []

def add_car(request):
    brand = request.form["brand"]
    name = request.form["name"]
    year = int(request.form["year"])
    price = int(request.form["price"])
    file = request.files.get("img")

    img_path = save_image(file)

    new_car = {
        "name": name,
        "brand": brand,
        "year": year,
        "price": price,
        "img": img_path
    }

    carlist.append(new_car)

    return {
        "message": f"{name} {brand} added successfully."
    }


def save_image(file):
    upload_folder = current_app.config["UPLOAD_FOLDER"]

    if file and file.filename:
        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        return f"uploads/{filename}"

    return "default.jpg"


def search_cars(query):
    if not query:
        return carlist

    return [
        car for car in carlist
        if query.lower() in car["name"].lower()
    ]
