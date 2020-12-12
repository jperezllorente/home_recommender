import geopandas
import pandas as pd
import shapely

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


def locations(radius, limit, cat_id, category ):
    url = f'https://api.foursquare.com/v2/venues/explore?&client_id={client_id}&client_secret={client_secret}&v={version}&ll=40.446067,-3.691247&radius={radius}&limit={limit}&categoryId={cat_id}'
    x = extract(url)
    return places_df(x, category)


def geo_frame(df):

    df = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.latitude, df.longitude))
    df['geometry']=df['geometry'].apply(lambda x:shapely.geometry.mapping(x))

    return df