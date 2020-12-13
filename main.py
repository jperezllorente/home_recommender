import pandas as pd
from src.frame import geo_frame
from flask import Flask, request, render_template
import markdown.extensions.fenced_code
import json
import src.home as hm
from wtforms import Form, FloatField, validators


app = Flask(__name__)


@app.route("/form")
def form():
    cat_list = ["Transport", "Nightlife", "Gyms", "Medical centre", "Entertainment"]
    return render_template('test.html', cat_list=cat_list)


@app.route("/input", methods=["GET"])
def options():

    if request.method == ['GET','POST']:
        cat_1 = request.form["category_1"]
        cat_2 = request.form["category_2"]
        cat_3 = request.form["category_3"]

        return json.dumps((hm.final(cat_1, cat_2, cat_3)))

    else:
        cat_1 = request.args.get("category_1")
        cat_2 = request.args.get("category_2")
        cat_3 = request.args.get("category_3")

        return json.dumps((hm.final(cat_1, cat_2, cat_3)))


@app.route("/prueba", methods=["GET"])
def prueba():
    tabla = pd.DataFrame(list(filter(None, map(hm.sum_gym, coordinates))))
    return tabla.to_html()





app.run(debug=True)
