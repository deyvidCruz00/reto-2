from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
from models.access import Base
from config import Config
import logging

logger = logging.getLogger(__name__)


class Database:
    """PostgreSQL database connection manager (Singleton)"""
    
    _instance = None
    _engine = None
    _session_factory = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def connect(self):
        """
        Initialize database connection and create tables
        
        Creates the SQLAlchemy engine, session factory, and ensures
        all tables are created based on the models.
        """
        try:
            if self._engine is None:
                logger.info(f"Connecting to PostgreSQL: {Config.DATABASE_URL}")
                
                self._engine = create_engine(
                    Config.DATABASE_URL,
                    poolclass=QueuePool,
                    pool_size=10,
                    max_overflow=20,
                    pool_pre_ping=True,
                    echo=Config.DEBUG
                )
                
                # Create tables
                Base.metadata.create_all(self._engine)
                
                # Create session factory
                self._session_factory = sessionmaker(bind=self._engine)
                self.Session = scoped_session(self._session_factory)
                
                logger.info("Successfully connected to PostgreSQL")
                
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            raise

    def get_session(self):
        """
        Get database session
        
        Returns:
            Session: SQLAlchemy session for database operations
        """
        if self._session_factory is None:
            self.connect()
        return self.Session()

    def ping(self):
        """
        Test database connection
        
        Returns:
            bool: True if connection is alive, False otherwise
        """
        try:
            if self._engine:
                with self._engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                return True
            return False
        except Exception as e:
            logger.error(f"Database ping failed: {e}")
            return False

    def close(self):
        """Close database connection and dispose of the engine"""
        if self._engine:
            self._engine.dispose()
            self._engine = None
            self._session_factory = None
            logger.info("PostgreSQL connection closed")


# Singleton instance
database = Database()
