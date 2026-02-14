from dotenv import load_dotenv
from fileinput import filename
import os
from flask import Flask,render_template, request, redirect, url_for
app = Flask(__name__)

load_dotenv()

upload_folder = os.getenv("UPLOAD_FOLDER")
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  
os.makedirs(upload_folder, exist_ok=True)

@app.errorhandler(413)
def file_too_large(error):
    return "file is too large (maxximum 1MB)", 413

carlist = [
   {"name": "Viper", "brand": "Dodge", "year": 2020, "price": 80000 , "img": "viper.png"},
   {"name": "Mustang", "brand": "Ford", "year": 2019, "price": 25000 , "img": "mustang.jpeg"},
   {"name": "Camaro", "brand": "Chevrolet", "year": 2021, "price": 30000 , "img": "camaro.jpg"},
   {"name": "A200", "brand": "Mercedes-Benz", "year": 2021, "price": 35000 , "img": "a200.jpg"},
   ]

def get_template():
    return render_template("index.html", cars=carlist)

@app.route("/")
def home():
    return get_template()

@app.route("/cars", methods=["GET"])
def cars():
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
    return get_template()

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host="0.0.0.0", port=8000, debug=True)

