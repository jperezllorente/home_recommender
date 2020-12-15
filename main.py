import pandas as pd
from src.frame import geo_frame
from flask import Flask, request, render_template, jsonify
import markdown.extensions.fenced_code
import json
import src.home as hm
import src.maps as mp
import folium
from folium import Choropleth, Circle, Marker, Icon, Map


app = Flask(__name__)


@app.route("/form")
def form():
    cat_list = ["Transport", "Restaurants and Nightlife", "Gyms", "Hospital", "Entertainment", "Supermarkets",
                "Parks", "Pharmacy", "School"]
    dist_list = ['Moncloa','Centro','Tetuán','Chamartín','Salamanca','Retiro','San Blas',
                 'Hortaleza','Chamberí','Fuencarral','Ciudad Lineal','Carabanchel','Arganzuela','Latina']
    type_list = ["flat", "penthouse", "duplex"]

    return render_template('test.html', cat_list=cat_list, dist_list=dist_list, type_list=type_list)


@app.route("/input", methods=["GET"])
def options():
    dist = request.args.get("district")
    cat_1 = request.args.get("category_1")
    cat_2 = request.args.get("category_2")
    cat_3 = request.args.get("category_3")
    proptype = request.args.get("type")

    result = hm.final(dist, cat_1, cat_2, cat_3, proptype)

    start_coords = (40.437863, -3.690433)
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

    return final_map._repr_html_()




@app.route("/prueba", methods=["GET"])
def prueba():
    tabla = pd.DataFrame(list(filter(None, map(hm.sum_gym, coordinates))))
    return tabla.to_html()


app.run(debug=True)
