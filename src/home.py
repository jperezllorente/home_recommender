import pandas as pd
import numpy as np
import requests
from pymongo import MongoClient, GEOSPHERE
from configuration.config import homes, places
from src.frame import geo_frame

data = pd.read_csv("C:\\Users\\juanp\\Ironhack\\proyectos\\final-project\\data\\vivienda.csv")
data = geo_frame(data)
test = data.sample(n=700)
coordinates = [list(i["coordinates"]) for i in test.geometry]
coord_prueba = coordinates[0]


def lugar(coords, categ, radio):
    return list(places.find(
        {"category": categ, "geometry": {"$near": {
            "$geometry": {"type": "Point",
                          "coordinates": coords
                          }, "$maxDistance": radio}}}, {"name": 1, "longitude": 1, "latitude": 1, "category": 1}
    ))


def sum_gym(coords):
    result = coords, len(lugar(coords, "gym", 500))
    if result[1] < 10:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]}, {"_id": 0, "province": 0, "municipality": 0, "geometry": 0})

        return r
    else:
        pass


def sum_rest(coords):
    result = coords, len(lugar(coords, "restaurant_nightlife", 500))
    if result[1] > 7:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]}, {"_id": 0, "province": 0, "municipality": 0, "geometry": 0})
        return r
    else:
        pass


def sum_superm(coords):
    result = coords, len(lugar(coords, "supermarket", 500))
    if 1 <= result[1] <= 10:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]}, {"_id": 0, "province": 0, "municipality": 0, "geometry": 0})
        return r
    else:
        pass


def sum_medical(coords):
    result = coords, len(lugar(coords, "medical_centre", 5000))
    if result[1] == 1:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]}, {"_id": 0, "province": 0, "municipality": 0, "geometry": 0})
        return r
    else:
        pass


def sum_transport(coords):
    result = coords, len(lugar(coords, "transport", 500))
    if 1 <= result[1] <= 10:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]}, {"_id": 0, "province": 0, "municipality": 0, "geometry": 0})
        return r
    else:
        pass


def sum_ent(coords):
    result = coords, len(lugar(coords, "general_entertainment", 1000))
    if result[1] > 5:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]}, {"_id": 0, "province": 0, "municipality": 0, "geometry": 0})
        return r
    else:
        pass


def sum_pharmacy(coords):
    result = coords, len(lugar(coords, "pharmacy", 500))
    if result[1] == 1:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]}, {"_id": 0, "province": 0, "municipality": 0, "geometry": 0})
        return r
    else:
        pass


def sum_parks(coords):
    result = coords, len(lugar(coords, "park", 1000))
    if 1 <= result[1] <= 5:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]}, {"_id": 0, "province": 0, "municipality": 0, "geometry": 0})
        return r
    else:
        pass


def sum_school(coords):
    result = coords, len(lugar(coords, "school", 500))
    if 1 <= result[1] <= 5:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]}, {"_id": 0, "province": 0, "municipality": 0, "geometry": 0})
        return r
    else:
        pass


def category(choice):
    if choice == "Supermarkets":
        return list(filter(None, map(sum_superm, coordinates)))

    elif choice == "Gyms":
        return list(filter(None, map(sum_gym, coordinates)))

    elif choice == "Transport":
        return list(filter(None, map(sum_transport, coordinates)))

    elif choice == "Entertainment":
        return list(filter(None, map(sum_ent, coordinates)))

    elif choice == "Parks":
        return list(filter(None, map(sum_parks, coordinates)))

    elif choice == "Restaurants nd Nightlife":
        return list(filter(None, map(sum_rest, coordinates)))

    elif choice == "Pharmacy":
        return list(filter(None, map(sum_pharmacy, coordinates)))

    elif choice == "Hospital":
        return list(filter(None, map(sum_medical, coordinates)))

    elif choice == "School":
        return list(filter(None, map(sum_school, coordinates)))


def final(district, cat_1, cat_2, cat_3, proptype):
    lista = []

    lista.append(category(cat_1))
    lista.append(category(cat_2))
    lista.append(category(cat_3))

    x = pd.DataFrame(lista[0])
    y = pd.DataFrame(lista[1])
    z = pd.DataFrame(lista[2])

    result = pd.concat([x, y, z])

    result = result[(result["district"] == district) & (result["propertyType"]==proptype)]

    return result[result.groupby('latitude').latitude.transform('count') > 1].drop_duplicates(subset="latitude",keep='first')
