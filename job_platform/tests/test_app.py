#!/usr/bin/python3
"""
Contains the TestAppDocs classes
"""

import unittest
from app import app

class TestAppSetup(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Job Platform', response.data)

if __name__ == '__main__':
    unittest.main()
