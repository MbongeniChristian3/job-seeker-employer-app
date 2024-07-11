#!/usr/bin/python3
"""
Contains the TestFormsDocs classes
"""

import unittest
from forms import RegistrationForm, LoginForm, JobPostForm

class TestForms(unittest.TestCase):
    def test_registration_form(self):
        form = RegistrationForm(username='testuser', email='test@example.com', password='password', confirm_password='password', user_type='jobseeker')
        self.assertTrue(form.validate())

    def test_login_form(self):
        form = LoginForm(email='test@example.com', password='password')
        self.assertTrue(form.validate())

    def test_job_post_form(self):
        form = JobPostForm(title='Test Job', description='Job Description')
        self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()

