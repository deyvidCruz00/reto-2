from domain.ports.access_ports import AccessRepositoryPort
from domain.entities.access import Access
from infrastructure.database.postgres import database
from datetime import datetime, timedelta
from sqlalchemy import and_
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class PostgresAccessRepository(AccessRepositoryPort):
    """PostgreSQL adapter for access data persistence"""
    
    def __init__(self):
        self.session = None

    def _get_session(self):
        """Get or create database session"""
        if self.session is None:
            self.session = database.get_session()
        return self.session

    def create_checkin(self, employee_id: str) -> Access:
        """
        Create a new check-in record
        
        Args:
            employee_id: Employee document ID
            
        Returns:
            Access: Created access record
            
        Raises:
            Exception: If database operation fails
        """
        try:
            session = self._get_session()
            
            # Import SQLAlchemy model here to avoid circular dependency
            from models.access import Access as AccessModel
            
            access_model = AccessModel(
                employee_id=employee_id,
                access_datetime=datetime.utcnow()
            )
            session.add(access_model)
            session.commit()
            session.refresh(access_model)
            
            logger.info(f"Check-in created for employee: {employee_id}")
            
            # Convert SQLAlchemy model to domain entity
            return self._to_domain_entity(access_model)
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating check-in: {e}")
            raise

    def create_checkout(self, employee_id: str) -> Optional[Access]:
        """
        Register check-out for the most recent active entry
        
        Args:
            employee_id: Employee document ID
            
        Returns:
            Optional[Access]: Updated access record or None if no active entry
            
        Raises:
            Exception: If database operation fails
        """
        try:
            session = self._get_session()
            
            # Import SQLAlchemy model here to avoid circular dependency
            from models.access import Access as AccessModel
            
            # Find the most recent access without exit_datetime
            access_model = session.query(AccessModel).filter(
                and_(
                    AccessModel.employee_id == employee_id,
                    AccessModel.exit_datetime == None
                )
            ).order_by(AccessModel.access_datetime.desc()).first()
            
            if access_model:
                access_model.exit_datetime = datetime.utcnow()
                
                # Calculate duration in minutes
                duration = access_model.exit_datetime - access_model.access_datetime
                access_model.duration_minutes = int(duration.total_seconds() / 60)
                
                session.commit()
                session.refresh(access_model)
                
                logger.info(f"Check-out created for employee: {employee_id}, duration: {access_model.duration_minutes} min")
                
                # Convert SQLAlchemy model to domain entity
                return self._to_domain_entity(access_model)
            
            return None
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating check-out: {e}")
            raise

    def has_active_entry(self, employee_id: str) -> bool:
        """
        Check if employee has an active entry (no exit_datetime)
        
        Args:
            employee_id: Employee document ID
            
        Returns:
            bool: True if employee has active entry, False otherwise
        """
        try:
            session = self._get_session()
            
            # Import SQLAlchemy model here to avoid circular dependency
            from models.access import Access as AccessModel
            
            count = session.query(AccessModel).filter(
                and_(
                    AccessModel.employee_id == employee_id,
                    AccessModel.exit_datetime == None
                )
            ).count()
            
            return count > 0
            
        except Exception as e:
            logger.error(f"Error checking active entry: {e}")
            return False

    def find_by_date(self, target_date: datetime) -> List[Access]:
        """
        Find all access records for a specific date
        
        Args:
            target_date: Date to search for
            
        Returns:
            List[Access]: List of access records for the date
        """
        try:
            session = self._get_session()
            
            # Import SQLAlchemy model here to avoid circular dependency
            from models.access import Access as AccessModel
            
            # Get start and end of day
            start_date = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
            
            access_models = session.query(AccessModel).filter(
                and_(
                    AccessModel.access_datetime >= start_date,
                    AccessModel.access_datetime < end_date
                )
            ).order_by(AccessModel.access_datetime).all()
            
            logger.info(f"Found {len(access_models)} accesses for date: {target_date.date()}")
            
            # Convert SQLAlchemy models to domain entities
            return [self._to_domain_entity(model) for model in access_models]
            
        except Exception as e:
            logger.error(f"Error finding accesses by date: {e}")
            return []

    def find_by_employee_and_date_range(
        self,
        employee_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Access]:
        """
        Find access records for an employee within a date range
        
        Args:
            employee_id: Employee document ID
            start_date: Start date of range
            end_date: End date of range
            
        Returns:
            List[Access]: List of access records in the date range
        """
        try:
            session = self._get_session()
            
            # Import SQLAlchemy model here to avoid circular dependency
            from models.access import Access as AccessModel
            
            # Adjust end_date to include the entire day
            end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            access_models = session.query(AccessModel).filter(
                and_(
                    AccessModel.employee_id == employee_id,
                    AccessModel.access_datetime >= start_date,
                    AccessModel.access_datetime <= end_date
                )
            ).order_by(AccessModel.access_datetime).all()
            
            logger.info(f"Found {len(access_models)} accesses for employee {employee_id} between {start_date.date()} and {end_date.date()}")
            
            # Convert SQLAlchemy models to domain entities
            return [self._to_domain_entity(model) for model in access_models]
            
        except Exception as e:
            logger.error(f"Error finding accesses by employee and date range: {e}")
            return []

    def _to_domain_entity(self, model) -> Access:
        """
        Convert SQLAlchemy model to domain entity
        
        Args:
            model: SQLAlchemy Access model
            
        Returns:
            Access: Domain entity
        """
        return Access(
            id=model.id,
            employee_id=model.employee_id,
            access_datetime=model.access_datetime,
            exit_datetime=model.exit_datetime,
            duration_minutes=model.duration_minutes
        )

    def close_session(self):
        """Close the database session"""
        if self.session:
            self.session.close()
            self.session = None
