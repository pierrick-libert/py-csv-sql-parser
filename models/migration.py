'''Migration Model'''
import datetime

from sqlalchemy import Column, func
from sqlalchemy.types import String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base


class Migration(declarative_base()):
    '''Migration table'''
    __tablename__ = 'ch_admin_migrations'
    id = Column(Integer, primary_key=True)
    filename = Column(String(150))
    migrated_at = Column(DateTime(timezone=datetime.datetime.utcnow), default=func.now())
