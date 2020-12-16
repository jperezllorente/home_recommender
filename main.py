import pandas as pd
from src.frame import geo_frame
from flask import Flask, request, render_template, jsonify
import markdown.extensions.fenced_code
import json
import src.home as hm
import folium
from folium import Choropleth, Circle, Marker, Icon, Map


app = Flask(__name__)


@app.route("/")
def form():
    cat_list = ["Transport", "Restaurants and Nightlife", "Gyms", "Hospital", "Entertainment", "Supermarkets",
                "Parks", "Pharmacy", "School"]

    dist_list = ['Moncloa','Centro','Tetuán','Chamartín','Salamanca','Retiro','San Blas',
                 'Hortaleza','Chamberí','Fuencarral','Ciudad Lineal','Carabanchel','Arganzuela','Latina']

    type_list = ["flat", "penthouse", "duplex"]

    price_list = ["Lower than 1K", "Between 2K and 3K", "Between 3K and 4K", "Between 4K and 5K", "Greater than 5K"]

    return render_template('form.html', cat_list=cat_list, dist_list=dist_list, type_list=type_list, price_list=price_list)


@app.route("/input", methods=["GET"])
def options():
    dist = request.args.get("district")
    cat_1 = request.args.get("category_1")
    cat_2 = request.args.get("category_2")
    cat_3 = request.args.get("category_3")
    proptype = request.args.get("type")
    price = request.args.get("price")

    result = hm.final(dist, cat_1, cat_2, cat_3, proptype, price)
    loc = (result.iloc[0]["latitude"], result.iloc[0]["longitude"])


    start_coords = loc
    final_map = folium.Map(location=start_coords, zoom_start=14)

    for i, row in result.iterrows():
        home = {
            "location": [row["latitude"], row["longitude"]],
            "tooltip": [row["price"], row["propertyType"], row["size"]]
        }
        icon = Icon(color="blue",
                    prefix="fa",
                    icon="home",
                    icon_color="white")

        Marker(**home, icon=icon).add_to(final_map)

    final_map.save("templates/map.html")
    return render_template("index.html")


@app.route("/table", methods=["GET"])
def info():
    dist = request.args.get("district")
    cat_1 = request.args.get("category_1")
    cat_2 = request.args.get("category_2")
    cat_3 = request.args.get("category_3")
    proptype = request.args.get("type")
    price = request.args.get("price")

    result = hm.final(dist, cat_1, cat_2, cat_3, proptype, price).reset_index(drop=True)

    result_html = result.to_html()

    return render_template("table.html", tables=[result_html])




app.run(debug=True)
