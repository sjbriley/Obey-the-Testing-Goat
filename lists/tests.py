from django.test import TestCase
from django.urls import resolve
from lists.views import home_page

# Create your tests here.

#Run with 'python manage.py tests'

class HomePageTest(TestCase):

    #This checks if resolve when called with '/' 
    #finds a function called 'home_page' 
    #home_page is the view function that we wrote AFTER trying the test
    #so initially it fails, then eventually after code will pass
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)