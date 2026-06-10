import os
from flask import current_app
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest


def add_car(request):
    brand = request.form.get("brandName")
    name = request.form.get("model")
    year = request.form.get("productionYear")
    price = request.form.get("price")
    file = request.files.get("img")

    if not brand:
        raise BadRequest("brandName is required")
    if not name:
        raise BadRequest("model is required")
    if not year:
        raise BadRequest("productionYear is required")
    if not price:
        raise BadRequest("price is required")

    try:
        year = int(year)
    except ValueError:
        raise BadRequest("productionYear must be a number")

    try:
        price = int(price)
    except ValueError:
        raise BadRequest("price must be a number")

    img_path = save_image(file)
    db = current_app.get_db()
    db.execute(
        "INSERT INTO tbl_cars (brandName, model, productionYear, price, img) VALUES (?, ?, ?, ?, ?)",
        (brand, name, year, price, img_path)
    )
    db.commit()

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

    return "uploads/default.jpg"


def row_to_dict(row):
    return {
        "id": row["id"],
        "model": row["model"],
        "brandName": row["brandName"],
        "productionYear": row["productionYear"],
        "price": row["price"],
        "img": row["img"] if "img" in row.keys() and row["img"] else "uploads/default.jpg"
    }


def get_all_cars():
    db = current_app.get_db()
    rows = db.execute("SELECT * FROM tbl_cars").fetchall()
    return [row_to_dict(row) for row in rows]


def search_cars(query, sort=""):
    db = current_app.get_db()

    order_clause = ""
    if sort == "high_price":
        order_clause = " ORDER BY price DESC"
    elif sort == "low_price":
        order_clause = " ORDER BY price ASC"
    elif sort == "alphabet":
        order_clause = " ORDER BY model COLLATE NOCASE ASC"

    if not query:
        sql = "SELECT * FROM tbl_cars" + order_clause
        rows = db.execute(sql).fetchall()
    else:
        search_value = f"%{query}%"
        sql = "SELECT * FROM tbl_cars WHERE model LIKE ? OR brandName LIKE ?" + order_clause
        rows = db.execute(sql, (search_value, search_value)).fetchall()

    return [row_to_dict(row) for row in rows]
