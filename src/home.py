import pandas as pd
import numpy as np
import requests
from pymongo import MongoClient, GEOSPHERE
from configuration.config import homes, places
from src.frame import geo_frame


data = pd.read_csv("C:\\Users\\juanp\\Ironhack\\proyectos\\final-project\\data\\test.csv")
data = geo_frame(data)
test = data.head(50)
coordinates = [list(i["coordinates"]) for i in data.geometry]
coord_prueba = coordinates[0]




def lugar(coords, categ):
    return list(places.find(
        {"category": categ, "geometry": {"$near": {
            "$geometry": {"type": "Point",
                          "coordinates": coords
                          }, "$maxDistance": 500}}}, {"name": 1, "longitude": 1, "latitude": 1, "category": 1}
    ))


def sum_gym(coords):
    result = coords, len(lugar(coords, "gym"))
    if result[1] > 7:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]})
        return r
    else:
        pass


def sum_superm(coords):
    result = coords, len(lugar(coords, "supermarket"))
    if result[1] > 5:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]})
        return r
    else:
        pass


def sum_store(coords):
    result = coords, len(lugar(coords, "clothing_stores"))
    if result[1] > 5:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]})
        return r
    else:
        pass


def sum_medical(coords):
    result = coords, len(lugar(coords, "medical_centre"))
    if result[1] > 5:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]},
                           {"_id": 0, "province": 0, "municipality": 0, "showAdress": 0, "geometry": 0})
        return r
    else:
        pass


def sum_nightlife(coords):
    result = coords, len(lugar(coords, "nightlife"))
    if result[1] > 5:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]},
                           {"_id": 0, "province": 0, "municipality": 0, "showAdress": 0, "geometry": 0})
        return r
    else:
        pass


def sum_transport(coords):
    result = coords, len(lugar(coords, "transport"))
    if result[1] > 5:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]},
                           {"_id": 0, "province": 0, "municipality": 0, "showAdress": 0, "geometry": 0})
        return r
    else:
        pass


def sum_ent(coords):
    result = coords, len(lugar(coords, "general_entertainment"))
    if result[1] > 5:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]},
                           {"_id": 0, "province": 0, "municipality": 0, "showAdress": 0, "geometry": 0})
        return r
    else:
        pass


def sum_store(coords):
    result = coords, len(lugar(coords, "clothing_stores"))
    if result[1] > 5:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]},
                           {"_id": 0, "province": 0, "municipality": 0, "showAdress": 0, "geometry": 0})
        return r
    else:
        pass


def category(choice):

    if choice == "Supermarkets":
        return str(list(filter(None, map(sum_gym, coordinates))))

    elif choice == "Gyms":
        return str(list(filter(None, map(sum_superm, coordinates))))

    elif choice == "Clothing store":
        return str(list(filter(None, map(sum_store, coordinates))))

    elif choice == "Nightlife":
        return str(list(filter(None, map(sum_nightlife, coordinates))))

    elif choice == "Transport":
        return str(list(filter(None, map(sum_transport, coordinates))))

    elif choice == "Entertainment":
        return str(list(filter(None, map(sum_ent, coordinates))))

    elif choice == "Medical centre":
        return str(list(filter(None, map(sum_medical, coordinates))))


def final(cat_1, cat_2, cat_3):

    lista = [category(cat_1), category(cat_2), category(cat_3)]


    return lista
