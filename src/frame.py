import geopandas
import pandas as pd
import shapely
from functools import reduce
import operator
from src.api import extract as ext

client_id = "KP3LZWOOOVPRQ3SW3RGNNW3OTBF42DQSNG2TTI3AZBVKBYN4"
client_secret = "TOLDQWSBZHJAWHTT51INCWB3TQG4MTKOKQQBT1HXVVDADR35"

def getFromDict(diccionario, mapa):
    return reduce(operator.getitem, mapa, diccionario)


def places_df(frame, category):
    nombre = ["venue", "name"]
    latitud = ["venue", "location", "lat"]
    longitud = ["venue", "location", "lng"]
    barrio = ["venue", "location", "neighborhood"]
    tipo = ["venue", "categories", "pluralName"]
    x = []

    for diccionario in frame:
        lista = {}
        lista["name"] = getFromDict(diccionario, nombre)
        lista["latitud"] = getFromDict(diccionario, longitud), getFromDict(diccionario, latitud)

        x.append(lista)

        df = pd.DataFrame(x)

    c = [category for _ in range(len(frame))]

    df["category"] = c

    return df



def locations(radius, limit,location, cat_id, category ):

    url = f'https://api.foursquare.com/v2/venues/explore?&client_id={client_id}&client_secret={client_secret}&v={version}&limit=200&ll={location}&radius={radius}&limit={limit}&categoryId={cat_id}'
    x = ext(url)

    return places_df(x, category)