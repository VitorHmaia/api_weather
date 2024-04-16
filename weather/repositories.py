from django.conf import settings
import pymongo

class WeatherRepository:

    collection = ''

    def __init__(self, collection_name) -> None:
        self.collection = collection_name
        
    def get_connection(self):
        CONNECTION_STRING = getattr(settings, "MONGO_CONNECTION_STRING")
        database = getattr(settings, "MONGO_DATABASE_NAME")
        client = pymongo.MongoClient(CONNECTION_STRING)
        connection = client[database]
        return connection
            
    def get_collection(self):
        connection = self.get_connection()
        collection = connection[self.collection]
        return collection

    def get_by_id(self, id):
        document = self.get_collection().find_one({"id": id})
        return document
        
    def get_all(self):
        document = self.get_collection().find({}).sort("date", -1)
        return document
        
    def get_by_attribute(self, attribute, value):
        return self.get_collection().find({attribute: value})
        
    def insert(self, document):
        data = {
            "id": str(uuid.uuid4()),
            "temperature": document['temperature'],
            "date": document['date'],
            "atmospheric_pressure": document['atmospheric_pressure'],
            "humidity": document['humidity'],
            "city": document['city'],
            "weather": document['weather']
        }
        self.get_collection().insert_one(data)
        
    def delete(self, id) -> None:
        return self.get_collection().delete_one({"_id": id})
        
    def delete_all(self) -> None:
        return self.get_collection().delete_many({})
    
    def update(self, query, data):
        self.get_collection().update_one({"id": query}, {"$set": data})
        
    def delete(self, query):
        self.get_collection().delete_one({"id": query})
        
    def delete_by_id(self, id):
        self.get_collection().delete_one({"id": id})
