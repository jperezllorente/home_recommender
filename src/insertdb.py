from pymongo import MongoClient

def insert_object(df, collection):
    '''
    This function inserts all the information from the dataframe we created with the previous function as a Mongodb object.
    This object will have two field: title (name of the film or show) and reviews (array with all the reviews users have made)
    '''

    collection.insert_many(df.to_dict('records'))

    return "Data succesfully added"