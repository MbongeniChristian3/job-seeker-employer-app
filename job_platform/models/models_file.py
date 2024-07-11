#!/usr/bin/python3
"""
job application from Models module
"""

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from base_model import BaseModel  
from sqlalchemy.ext.declarative import declarative_base

class User(BaseModel, model):
    """
    creates a users table to fulfill the following attributes 
    * name
    * email
    * jobs
    """
    __tablename__ = 'users'

    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    jobs = relationship('JobApplication', back_populates='user')

class JobApplication(BaseModel, model):
     """
    The JobsApplied table has a many to one relationship with User Table.

    Mandatory Fields that the user must submit include:
        * Company
        * Job_Title

    The following attributes have special characteristics that must
    be followed:

    status -> Values must be one of the following:
    ['Applied', 'Interviewing', 'Offer Stage', 'Archived']

    interview_progress -> Values must be one of the following:
    ['Recruiter Call', 'Onsite', 'Tech Screen', 'Awaiting Decision', 'Phone Interview']
    """
    __tablename__ = 'job_applications'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    company = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    status = Column(String, nullable=False)
    user = relationship('User', back_populates='jobs')

