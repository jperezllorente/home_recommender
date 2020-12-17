import pandas as pd
import numpy as np
import requests
from pymongo import MongoClient, GEOSPHERE
from configuration.config import homes, places
from src.frame import geo_frame

x = pd.DataFrame(homes.find({}, {"_id": 0, "geometry": 0, "province": 0, "municipality": 0, "showAddress": 0}))
x = geo_frame(x)
test = x.sample(n=1500)
coordinates = [list(i["coordinates"]) for i in test.geometry]


def lugar(coords, categ, radio):
    '''
    With this function we make queries to the "places" collection of our DataBase. This is te first step towards creating
    the final function that will give us the results we want.

    It take as arguments the coordinates (in this case we will use the coordiantes of the homes found in our collection)
    from which we want to make the search, the category (as we want to look for different object with each query) and
    the search radio
    '''

    return list(places.find(
        {"category": categ, "geometry": {"$near": {
            "$geometry": {"type": "Point",
                          "coordinates": coords
                          }, "$maxDistance": radio}}}, {"name": 1, "longitude": 1, "latitude": 1, "category": 1}
    ))


def sum_gym(coords):
    '''
    This is the funciton that will return all the objects that have the gym category. Inside the function we use the
    previous one, "lugar", and we use the results obtained to get the homes using a query from that will get the
    obejcts from the home collection.

    It takes as arguments the coordinates from the houses inside the home collection

    This function is the same for all specific places, but changing the category we want to look for.
    '''

    result = coords, len(lugar(coords, "gym", 700))
    if result[1] > 3:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]}, {"_id": 0, "province": 0,
                                                                                   "municipality": 0, "geometry": 0})

        return r
    else:
        pass


def sum_rest(coords):
    result = coords, len(lugar(coords, "restaurant_nightlife", 1000))
    if result[1] > 7:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]}, {"_id": 0, "province": 0,
                                                                                   "municipality": 0, "geometry": 0})
        return r
    else:
        pass


def sum_superm(coords):
    result = coords, len(lugar(coords, "supermarket", 700))
    if 1 <= result[1] > 3:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]}, {"_id": 0, "province": 0,
                                                                                   "municipality": 0, "geometry": 0})
        return r
    else:
        pass


def sum_medical(coords):
    result = coords, len(lugar(coords, "medical_centre", 3000))
    if result[1] > 1:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]}, {"_id": 0, "province": 0,
                                                                                   "municipality": 0, "geometry": 0})
        return r
    else:
        pass


def sum_transport(coords):
    result = coords, len(lugar(coords, "transport", 500))
    if 1 <= result[1] > 1:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]}, {"_id": 0, "province": 0,
                                                                                   "municipality": 0, "geometry": 0})
        return r
    else:
        pass


def sum_ent(coords):
    result = coords, len(lugar(coords, "general_entertainment", 1500))
    if result[1] > 7:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]}, {"_id": 0, "province": 0,
                                                                                   "municipality": 0, "geometry": 0})
        return r
    else:
        pass


def sum_pharmacy(coords):
    result = coords, len(lugar(coords, "pharmacy", 500))
    if result[1] > 1:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]}, {"_id": 0, "province": 0,
                                                                                   "municipality": 0, "geometry": 0})
        return r
    else:
        pass


def sum_parks(coords):
    result = coords, len(lugar(coords, "park", 1000))
    if 1 <= result[1] > 2:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]}, {"_id": 0, "province": 0,
                                                                                   "municipality": 0, "geometry": 0})
        return r
    else:
        pass


def sum_school(coords):
    result = coords, len(lugar(coords, "school", 3000))
    if 1 <= result[1] > 2:
        r = homes.find_one({"latitude": result[0][0], "longitude": result[0][1]}, {"_id": 0, "province": 0,
                                                                                   "municipality": 0, "geometry": 0})
        return r
    else:
        pass


def category(choice):
    '''
    This function executes the proper function depending on what we want to look for.

    We need to use map() as we want t apply the function to eah of the coordinates, filter because we want to delete
    none values, and list to obtain a proper result we can work with later

    It takes as argument a string that represents what establishments we want to have near the homes we want
    '''

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


def final(district, cat_1, cat_2, cat_3, proptype, price):
    '''
    This is the function that will return the homes based on the set criteria.

    Insie a list we will append the results from the category() function. The result will be a list with three lists of
    dictionaries, so we have to turn each of those elements into  a dataframe in order to concatenate them later.

    Once concatenated, we search by the district and property type we are interested in, and also by the range of
    price. All this argument, including cat_1, cat_2 and cat_3 will be inerted though an endpoint that can be found in
    the main.py file.

    One the dataframe is created, we look only for those elements that appear more than twice, as we want the results to
    fulfill all three categories, and then we delete duplicates.
    '''

    lista = [category(cat_1), category(cat_2), category(cat_3)]

    result = pd.concat([pd.DataFrame(lista[0]), pd.DataFrame(lista[1]), pd.DataFrame(lista[2])])

    result = result[(result["district"] == district) & (result["propertyType"] == proptype)]

    # In the section below I have set the conditions for home selection based on price range

    if price == "Lower than 1K":
        result = result[result["price"] <= 1000]

    elif price == "Between 1K and 2K":
        result = result[(result.price > 1000) & (result.price <= 2000)]

    elif price == "Between 2K and 3K":
        result = result[(result.price > 2000) & (result.price <= 3000)]

    elif price == "Between 3K and 4K":
        result = result[(result.price > 3000) & (result.price <= 4000)]

    elif price == "Between 4K and 5K":
        result = result[(result.price > 4000) & (result.price <= 5000)]

    elif price == "Greater than 5K":
        result = result = result[(result.price > 5000)]

    # This line of code selects only those rows that appear two or more times and deletes the duplicates to keep only
    # one instance of each element
    return result[result.groupby('latitude').latitude.transform('count') > 1].drop_duplicates(subset="latitude",
                                                                                              keep='first')
