#!/usr/bin/python3
"""
Contains the TestModelsDocs classes
"""

import unittest
from app import db
from models import User, Job, Application

class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_model(self):
        user = User(username='testuser', email='test@example.com', password='password', user_type='jobseeker')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(user.username, 'testuser')

    def test_job_model(self):
        job = Job(title='Test Job', description='Job Description', employer_id=1)
        db.session.add(job)
        db.session.commit()
        self.assertEqual(Job.query.count(), 1)
        self.assertEqual(job.title, 'Test Job')

    def test_application_model(self):
        application = Application(job_id=1, applicant_id=1)
        db.session.add(application)
        db.session.commit()
        self.assertEqual(Application.query.count(), 1)
        self.assertEqual(application.job_id, 1)

if __name__ == '__main__':
    unittest.main()
