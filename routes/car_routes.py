from flask import Blueprint, render_template, request, jsonify
from routes.car_modul import add_car, search_cars, get_all_cars

car_bp = Blueprint("car_bp", __name__)

@car_bp.route("/")
def home():
    cars = get_all_cars()
    return render_template("index.html", cars=cars)


@car_bp.route("/add-car")
def add_car_page():
    return render_template("add_car.html")


@car_bp.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "")
    sort = request.args.get("sort", "")
    results = search_cars(query, sort)
    return jsonify(results)


@car_bp.route("/add", methods=["POST"])
def add():
    return jsonify(add_car(request))
