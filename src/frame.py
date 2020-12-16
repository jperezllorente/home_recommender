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
    '''
    As the result we get from APIs is a json, and after working with it we get a dict, we have to extract those keys
    that we will need for our project. The getFromDict allows us to identify the key we are interested in and extract
    its value. The places_df() used this previous function to iterates through the dictionary and create a dataframe
    with the data extracted

    It takes as arguments the dictionary and the category we want to give to the elements extracted
    '''


    nombre = ["venue", "name"]
    latitud = ["venue", "location", "lat"]
    longitud = ["venue", "location", "lng"]
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

    '''
    This function is a combination of two functions (extract() form the api.py file, and the places_df() of this file)
    Using the extract() we can make queries to the Foursquare API, and using the places_df() we create a dataframe with
    the data extracted

    It takes as arguments:
        - The radius inside which we want to search in Foursquare
        - The limit of results we want to obtain
        - The location(lat, long) as centre point of the search
        - cat_id is the category id of certain places we are interested in. This can be found in Foursquare website
        (https://developer.foursquare.com/docs/build-with-foursquare/categories/)
        - The category we want to give to the results. This will fill all the cells of the category columns of the dataframe
    '''

    url = f'https://api.foursquare.com/v2/venues/explore?&client_id={client_id}&client_secret={client_secret}&v={version}&limit=200&ll={location}&radius={radius}&limit={limit}&categoryId={cat_id}'
    x = ext(url)

    return places_df(x, category)


def geo_frame(df):
    '''
    This function first uses geopanda to create a type:POINT feature that will be used when makign geo queries.
    Secondly, in order to insert a certain dataframe in a MongoDB collection, as type:POINT is not recognized,
    we have to use shspely to turn it into a feature that can work with Mongo.

    The only argument it takes is the dataframe we want to convert
    '''

    df = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.latitude, df.longitude))
    df['geometry']=df['geometry'].apply(lambda x:shapely.geometry.mapping(x))
    return df