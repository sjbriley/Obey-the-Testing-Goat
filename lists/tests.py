from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

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

    def test_home_page_returns_correct_html(self):

        #HttpRequest is what django sees when browser asks for page
        request = HttpRequest()

        #pass to home_page view and receive response in form of HttpResponse object
        response = home_page(request)

        #converts bits (0's, 1's) into HTML string
        html = response.content.decode('utf8')
        
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))