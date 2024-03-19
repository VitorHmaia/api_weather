# repositories.py

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
			
	# CRUD
def get_by_id(self, id):
        return self.get_collection().find_one({"_id": id})
        
def get_all(self):
        return self.get_collection().find({})
        
def get_by_attribute(self, attribute, value):
        return self.get_collection().find({attribute: value})
        
def insert(self, document) -> None:
        self.get_collection().insert_one(document)
        
def delete(self, id) -> None:
        self.get_collection().delete_one({"_id": id})
        
def delete_all(self) -> None:
        self.get_collection().delete_many({})
