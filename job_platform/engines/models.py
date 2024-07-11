#!/usr/bin/python3
"""
Contains the ModelsDocs classes
"""

from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    """ returns user_id """
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)  # 'jobseeker' or 'employer'

    def __repr__(self):
        """ initialises username, email, user_type """
        return f"User('{self.username}', '{self.email}', '{self.user_type}')"

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """ returns job tittle and date posted """
        return f"Job('{self.title}', '{self.date_posted}')"

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_applied = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        """ returns application's, job_id, applicant_id, date_applied """
        return f"Application('{self.job_id}', '{self.applicant_id}', '{self.date_applied}')"

