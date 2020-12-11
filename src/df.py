import pandas as pd
import geopandas


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



def geo_frame(frame):
    return geopandas.GeoDataFrame(
        frame, geometry=geopandas.points_from_xy(frame.longitud, frame.latitud))
