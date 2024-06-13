import uuid
from django.conf import settings
import pymongo
import logging

# Configure logging
logger = logging.getLogger(__name__)

class MongoDBConnection:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            try:
                CONNECTION_STRING = settings.MONGO_CONNECTION_STRING
                cls._client = pymongo.MongoClient(CONNECTION_STRING)
                logger.info("MongoDB connection established.")
            except pymongo.errors.ConnectionError as e:
                logger.error("Failed to connect to MongoDB", exc_info=True)
                raise Exception("Failed to connect to MongoDB") from e
        return cls._client

class WeatherRepository:

    def __init__(self, collection_name) -> None:
        self.collection_name = collection_name
        self.collection = self.get_collection()

    def get_connection(self):
        client = MongoDBConnection.get_client()
        database = settings.MONGO_DATABASE_NAME
        return client[database]
            
    def get_collection(self):
        connection = self.get_connection()
        return connection[self.collection_name]

    def get_by_id(self, id):
        try:
            document = self.collection.find_one({"id": id})
            return document
        except Exception as e:
            logger.error(f"Error fetching document by id: {id}", exc_info=True)
            raise Exception("Error fetching document by id") from e
        
    def get_all(self):
        try:
            documents = self.collection.find({}).sort("date", -1)
            return list(documents)
        except Exception as e:
            logger.error("Error fetching all documents", exc_info=True)
            raise Exception("Error fetching all documents") from e
        
    def get_by_attribute(self, attribute, value):
        try:
            documents = self.collection.find({attribute: value})
            return list(documents)
        except Exception as e:
            logger.error(f"Error fetching documents by attribute: {attribute} = {value}", exc_info=True)
            raise Exception("Error fetching documents by attribute") from e
        
    def insert(self, document):
        try:
            data = {
                "id": str(uuid.uuid4()),
                "temperature": document['temperature'],
                "date": document['date'],
                "atmospheric_pressure": document['atmospheric_pressure'],
                "humidity": document['humidity'],
                "city": document['city'],
                "weather": document['weather']
            }
            result = self.collection.insert_one(data)
            logger.info(f"Inserted document with id: {data['id']}")
            return result.inserted_id
        except Exception as e:
            logger.error("Error inserting document", exc_info=True)
            raise Exception("Error inserting document") from e
        
    def update(self, id, data):
        try:
            result = self.collection.update_one({"id": id}, {"$set": data})
            if result.matched_count:
                logger.info(f"Updated document with id: {id}")
            else:
                logger.warning(f"No document found with id: {id}")
            return result.matched_count
        except Exception as e:
            logger.error(f"Error updating document with id: {id}", exc_info=True)
            raise Exception("Error updating document") from e
        
    def delete_by_id(self, id):
        try:
            result = self.collection.delete_one({"id": id})
            if result.deleted_count:
                logger.info(f"Deleted document with id: {id}")
            else:
                logger.warning(f"No document found with id: {id}")
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error deleting document with id: {id}", exc_info=True)
            raise Exception("Error deleting document") from e
        
    def delete_all(self):
        try:
            result = self.collection.delete_many({})
            logger.info(f"Deleted {result.deleted_count} documents")
            return result.deleted_count
        except Exception as e:
            logger.error("Error deleting all documents", exc_info=True)
            raise Exception("Error deleting all documents") from e
