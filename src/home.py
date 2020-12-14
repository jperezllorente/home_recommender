import pandas as pd
import numpy as np
import requests
from pymongo import MongoClient, GEOSPHERE
from configuration.config import homes, places
from src.frame import geo_frame


data = pd.read_csv("C:\\Users\\juanp\\Ironhack\\proyectos\\final-project\\data\\test.csv")
data = geo_frame(data)
test = data.head(100)
coordinates = [list(i["coordinates"]) for i in test.geometry]
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
    if result[1] > 2:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]})
        return r
    else:
        pass


def sum_rest(coords):
    result = coords, len(lugar(coords, "restaurant"))
    if result[1] > 15:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]})
        return r
    else:
        pass


def sum_night(coords):
    result = coords, len(lugar(coords, "nightlife"))
    if result[1] > 15:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]})
        return r
    else:
        pass


def sum_superm(coords):
    result = coords, len(lugar(coords, "supermarket"))
    if result[1] > 2:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]})
        return r
    else:
        pass


def sum_store(coords):
    result = coords, len(lugar(coords, "clothing_store"))
    if result[1] > 10:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]})
        return r
    else:
        pass


def sum_medical(coords):
    result = coords, len(lugar(coords, "medical_centre"))
    if result[1] > 2:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]})
        return r
    else:
        pass


def sum_transport(coords):
    result = coords, len(lugar(coords, "transport"))
    if result[1] > 2:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]})
        return r
    else:
        pass


def sum_ent(coords):
    result = coords, len(lugar(coords, "general_entertainment"))
    if result[1] > 15:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]})
        return r
    else:
        pass


def sum_pharmacy(coords):
    result = coords, len(lugar(coords, "pharmacy"))
    if result[1] > 2:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]})
        return r
    else:
        pass


def sum_parks(coords):
    result = coords, len(lugar(coords, "park"))
    if result[1] > 2:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]})
        return r
    else:
        pass

def sum_school(coords):
    result = coords, len(lugar(coords, "school"))
    if result[1] > 5:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]})
        return r
    else:
        pass


def category(choice):

    if choice == "Supermarkets":
        return list(filter(None, map(sum_superm, coordinates)))

    elif choice == "Gyms":
        return list(filter(None, map(sum_gym, coordinates)))

    elif choice == "Clothing store":
        return list(filter(None, map(sum_store, coordinates)))

    elif choice == "Nightlife":
        return list(filter(None, map(sum_night, coordinates)))

    elif choice == "Transport":
        return list(filter(None, map(sum_transport, coordinates)))

    elif choice == "Entertainment":
        return list(filter(None, map(sum_ent, coordinates)))

    elif choice == "Parks":
        return list(filter(None, map(sum_parks, coordinates)))

    elif choice == "Restaurants":
        return list(filter(None, map(sum_rest, coordinates)))

    elif choice == "Pharmacy":
        return list(filter(None, map(sum_pharmacy, coordinates)))

    elif choice == "Hospital":
        return list(filter(None, map(sum_medical, coordinates)))

    elif choice == "School":
        return list(filter(None, map(sum_school, coordinates)))


def final(cat_1, cat_2, cat_3) -> object:
    lista = []

    lista.append(category(cat_1))
    lista.append(category(cat_2))
    lista.append(category(cat_3))

    x = pd.DataFrame(lista[0])
    y = pd.DataFrame(lista[1])
    z = pd.DataFrame(lista[2])

    result = pd.concat([x, y, z])

    return result[result.groupby('latitude').latitude.transform('count') > 1]
