"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
"""
from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase): # def setUp(self): #
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self): #
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000/earthquakes')
        self.assertIn('Foundation 5.5.0', self.browser.title)
        self.fail('Finish the test!')

if __name__ == '__main__': #
    unittest.main()
    """

class SmokeTest(TestCase):
    def test_bad_maths(self): self.assertEqual(1 + 1, 3)
