from pymongo import MongoClient

def insert_object(review, title, genres, collection):
    '''
    This function inserts all the information from the dataframe we created with the previous function as a Mongodb object.
    This object will have two field: title (name of the film or show) and reviews (array with all the reviews users have made)
    '''

    test = [i for i in review]

    genres = [i for i in genres[0]]

    final = [i for i in genres]

    datos = {'title': title,
             'reviews': test,
             'genres': final}

    collection.insert_one(datos)

    return "Film reviews succesfully added"