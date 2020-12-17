import pandas as pd
from src.frame import geo_frame
from flask import Flask, request, render_template, jsonify
import markdown.extensions.fenced_code
import json
import src.home as hm
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from pymongo import MongoClient, GEOSPHERE
from configuration.config import homes, places

data = pd.DataFrame(homes.find({},{"_id":0, "geometry":0, "province":0, "municipality":0, "showAddress":0}))
data_df = geo_frame(data)


app = Flask(__name__)


@app.route("/")
def form():
    cat_list = ["Transport", "Restaurants and Nightlife", "Gyms", "Hospital", "Entertainment", "Supermarkets",
                "Parks", "Pharmacy", "School"]

    dist_list = ['Moncloa','Centro','Tetuán','Chamartín','Salamanca','Retiro','San Blas',
                 'Hortaleza','Chamberí','Fuencarral','Ciudad Lineal','Carabanchel','Arganzuela','Latina']

    type_list = ["flat", "penthouse", "duplex"]

    price_list = ["Lower than 1K", "Between 1K and 2K", "Between 2K and 3K", "Between 3K and 4K", "Between 4K and 5K",
                  "Greater than 5K"]

    data_summary = data_df.groupby("district").agg({"price": [max, min, 'mean']})

    return render_template('form.html', cat_list=cat_list, dist_list=dist_list, type_list=type_list,
                           price_list=price_list, tables=[data_summary.to_html()])


@app.route("/input", methods=["GET"])
def options():
    dist = request.args.get("district")
    cat_1 = request.args.get("category_1")
    cat_2 = request.args.get("category_2")
    cat_3 = request.args.get("category_3")
    proptype = request.args.get("type")
    price = request.args.get("price")

    result = hm.final(dist, cat_1, cat_2, cat_3, proptype, price)

    if result.empty:
        return render_template("error.html")

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

    if result.empty == True:
        return render_template("error.html")

    result_html = result.to_html()

    return render_template("table.html", tables=[result_html])




app.run(debug=True)
