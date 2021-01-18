from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from django.template.loader import render_to_string

from lists.views import home_page

from lists.models import Item

# Create your tests here.

# Run with 'python manage.py tests'

class HomePageTest(TestCase):

    #This checks if resolve when called with '/' 
    #finds a function called 'home_page' 
    #home_page is the view function that we wrote AFTER trying the test
    #so initially it fails, then eventually after code will pass
    #We can delete this test because in the next funciton Django implicitly checks for it
    '''
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
    '''

    def test_home_page_returns_correct_html(self):

        #HttpRequest is what django sees when browser asks for page
        #request = HttpRequest()

        #pass to home_page view and receive response in form of HttpResponse object
        #response = home_page(request)

        #converts bits (0's, 1's) into HTML string
        #html = response.content.decode('utf8')
        
        #self.assertTrue(html.startswith('<html>'))
        #self.assertIn('<title>To-Do lists</title>', html)
        #self.assertTrue(html.endswith('</html>'))

        #We should never test constants, which is why we don't return
        #Httprequests in views.py, instead use a function to get templates
        #where home.html is and return html from there.
        #This is refractoring code, where we only change format and not actual function
        #This test below tests if views.home_page actually returns the template
        """
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        expected_html = render_to_string('home.html')
        self.assertEqual(html, expected_html)
        """
        # But here is an easier way to do all of the above it besides manually creating request:
        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))
        
        #test method Django's TestCase provides that checks what
        #template used to render a response
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={
            'item_text': 'A new list item'
        })
        self.assertIn('A new list item', response.content.decode())
        #at first, we return HttpResponse so this will fail, but we change it to return home.html
        self.assertTemplateUsed(response, 'home.html')

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second = Item()
        second.text = 'Item the second'
        second.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')