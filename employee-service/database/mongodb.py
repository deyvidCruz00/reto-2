from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import Config
import logging

logger = logging.getLogger(__name__)

class MongoDB:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
        return cls._instance

    def connect(self):
        try:
            if self._client is None:
                logger.info(f"Connecting to MongoDB: {Config.MONGO_URI}")
                self._client = MongoClient(Config.MONGO_URI)
                self._db = self._client[Config.MONGO_DB]
                
                # Test connection
                self._client.admin.command('ping')
                logger.info("Successfully connected to MongoDB")
                
                # Create indexes
                self._create_indexes()
                
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def _create_indexes(self):
        """Create indexes for employee collection"""
        try:
            employees = self._db.employee
            
            # Unique index on document
            employees.create_index("document", unique=True)
            
            # Index on email for fast lookup
            employees.create_index("email")
            
            # Index on status
            employees.create_index("status")
            
            logger.info("MongoDB indexes created successfully")
        except Exception as e:
            logger.warning(f"Error creating indexes: {e}")

    def get_database(self):
        if self._db is None:
            self.connect()
        return self._db

    def get_collection(self, collection_name):
        return self.get_database()[collection_name]

    def close(self):
        if self._client:
            self._client.close()
            logger.info("MongoDB connection closed")

# Singleton instance
mongodb = MongoDB()
