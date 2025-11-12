from database.postgres import database
from models.access import Access
from datetime import datetime, timedelta
from sqlalchemy import and_, func
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class AccessRepository:
    def __init__(self):
        self.session = None

    def _get_session(self):
        if self.session is None:
            self.session = database.get_session()
        return self.session

    def create_checkin(self, employee_id: str) -> Access:
        """Create a new check-in record"""
        try:
            session = self._get_session()
            access = Access(
                employee_id=employee_id,
                access_datetime=datetime.utcnow()
            )
            session.add(access)
            session.commit()
            session.refresh(access)
            logger.info(f"Check-in created for employee: {employee_id}")
            return access
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating check-in: {e}")
            raise

    def create_checkout(self, employee_id: str) -> Optional[Access]:
        """Create checkout (update exit_datetime and calculate duration)"""
        try:
            session = self._get_session()
            
            # Find the most recent access without exit_datetime
            access = session.query(Access).filter(
                and_(
                    Access.employee_id == employee_id,
                    Access.exit_datetime == None
                )
            ).order_by(Access.access_datetime.desc()).first()
            
            if access:
                access.exit_datetime = datetime.utcnow()
                
                # Calculate duration in minutes
                duration = access.exit_datetime - access.access_datetime
                access.duration_minutes = int(duration.total_seconds() / 60)
                
                session.commit()
                session.refresh(access)
                logger.info(f"Check-out created for employee: {employee_id}, duration: {access.duration_minutes} min")
                return access
            
            return None
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating check-out: {e}")
            raise

    def has_active_entry(self, employee_id: str) -> bool:
        """Check if employee has an active entry (no exit)"""
        try:
            session = self._get_session()
            count = session.query(Access).filter(
                and_(
                    Access.employee_id == employee_id,
                    Access.exit_datetime == None
                )
            ).count()
            return count > 0
        except Exception as e:
            logger.error(f"Error checking active entry: {e}")
            return False

    def find_by_date(self, target_date: datetime) -> List[Access]:
        """Find all accesses by date"""
        try:
            session = self._get_session()
            
            # Get start and end of day
            start_date = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
            
            accesses = session.query(Access).filter(
                and_(
                    Access.access_datetime >= start_date,
                    Access.access_datetime < end_date
                )
            ).order_by(Access.access_datetime).all()
            
            logger.info(f"Found {len(accesses)} accesses for date: {target_date.date()}")
            return accesses
        except Exception as e:
            logger.error(f"Error finding accesses by date: {e}")
            return []

    def find_by_employee_and_date_range(self, employee_id: str, start_date: datetime, end_date: datetime) -> List[Access]:
        """Find accesses by employee and date range"""
        try:
            session = self._get_session()
            
            # Adjust end_date to include the entire day
            end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            accesses = session.query(Access).filter(
                and_(
                    Access.employee_id == employee_id,
                    Access.access_datetime >= start_date,
                    Access.access_datetime <= end_date
                )
            ).order_by(Access.access_datetime).all()
            
            logger.info(f"Found {len(accesses)} accesses for employee {employee_id} between {start_date.date()} and {end_date.date()}")
            return accesses
        except Exception as e:
            logger.error(f"Error finding accesses by employee and date range: {e}")
            return []

    def close_session(self):
        """Close the session"""
        if self.session:
            self.session.close()
            self.session = None
