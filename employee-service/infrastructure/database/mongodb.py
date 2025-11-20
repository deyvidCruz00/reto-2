"""
MongoDB connection manager - Infrastructure Layer
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import Config
import logging

logger = logging.getLogger(__name__)


class MongoDB:
    """MongoDB singleton connection manager"""
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
        return cls._instance

    def connect(self):
        """Connect to MongoDB"""
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
            logger.error(f"Error creating indexes: {e}")

    def get_collection(self, collection_name: str):
        """Get a collection from the database"""
        if self._db is None:
            raise Exception("Database not connected. Call connect() first")
        return self._db[collection_name]

    def close(self):
        """Close MongoDB connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            logger.info("MongoDB connection closed")

    def ping(self):
        """Ping MongoDB to check connection"""
        if self._client:
            self._client.admin.command('ping')
            return True
        return False


# Singleton instance
mongodb = MongoDB()
