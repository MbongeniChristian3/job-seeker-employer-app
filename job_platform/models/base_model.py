#!/usr/bin/env python 3
"""
Base model class of models module
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy import chemy, Column, Integer, String, Float, DateTime
from uuid import uuid4, UUID


Base = declarative_base()

class BaseModel(Base):
    """
    The base model for our database module
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def save(self, session):
        """ it saves instance """
        session.add(self)
        session.commit()

    def delete(self, session):
        """
        Deletes instance from storage
        """
        session.delete(self)
        session.commit()

