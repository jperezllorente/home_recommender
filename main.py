import pandas as pd
from src.frame import geo_frame
from flask import Flask, request, render_template, jsonify
import markdown.extensions.fenced_code
import json
import src.home as hm
from wtforms import Form, FloatField, validators

app = Flask(__name__)


@app.route("/form")
def form():
    cat_list = ["Transport", "Nightlife", "Gyms", "Hospital", "Entertainment", "Supermarkets", "Restaurants",
                "Parks", "Pharmacy", "School", "Clothing store", ""]
    return render_template('test.html', cat_list=cat_list)


@app.route("/input", methods=["GET"])
def options():
    cat_1 = request.args.get("category_1")
    cat_2 = request.args.get("category_2")
    cat_3 = request.args.get("category_3")
    result = hm.final(cat_1, cat_2, cat_3)
    result.to_csv("data\\end_1.csv")
    return result.to_html()


@app.route("/prueba", methods=["GET"])
def prueba():
    tabla = pd.DataFrame(list(filter(None, map(hm.sum_gym, coordinates))))
    return tabla.to_html()


app.run(debug=True)
