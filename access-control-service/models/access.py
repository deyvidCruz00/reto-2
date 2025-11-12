from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Access(Base):
    __tablename__ = 'access'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(String(50), nullable=False, index=True)
    access_datetime = Column(DateTime, nullable=False, default=datetime.utcnow)
    exit_datetime = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    
    def __repr__(self):
        return f"<Access(id={self.id}, employee_id={self.employee_id}, access={self.access_datetime})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'access_datetime': self.access_datetime.isoformat() if self.access_datetime else None,
            'exit_datetime': self.exit_datetime.isoformat() if self.exit_datetime else None,
            'duration_minutes': self.duration_minutes
        }

class Alert(Base):
    __tablename__ = 'alert'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    description = Column(String(500), nullable=False)
    code = Column(String(100), nullable=False, index=True)
    severity = Column(String(20), nullable=False, default='INFO')
    employee_id = Column(String(50), nullable=True)
    
    def __repr__(self):
        return f"<Alert(id={self.id}, code={self.code}, severity={self.severity})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'description': self.description,
            'code': self.code,
            'severity': self.severity,
            'employee_id': self.employee_id
        }
