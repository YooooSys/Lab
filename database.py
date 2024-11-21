from pymongo import MongoClient
import certifi

def get_collection(database_name, collection_name):
    connection_string = "mongodb+srv://giahuy11095:123123123@hyper.kxke3.mongodb.net/"
    client = MongoClient(connection_string, tlsCAFile=certifi.where())
    db = client[database_name]  # Truy cập database
    collection = db[collection_name]  # Truy cập collection
    return collection
