import os
from flask import Blueprint, render_template, request, jsonify, current_app
from static_data.cars import carlist
from routes.car_modul import add_car, search_cars

car_bp = Blueprint("car_bp", __name__)

@car_bp.route("/")
def home():
    return render_template("index.html", cars=carlist)


@car_bp.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "")
    results = search_cars(query)
    return jsonify(results)


@car_bp.route("/add", methods=["POST"])
def add():
    return jsonify(add_car(request))
