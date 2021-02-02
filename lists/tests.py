from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from django.template.loader import render_to_string

from lists.views import home_page

from lists.models import Item, List

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

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)
"""
    def test_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())
"""

class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        #list_ is used as name to avoid conflict with built in python list
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)

class ListViewTest(TestCase):
    
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        #instead of "assertIn" with "response.content.decode", assertContains
        #knows how to deal with responses and bytes of their content
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        # we leave off trailing slash after /new because /new is action URL which modify database
        response = self.client.post('/lists/new', data={
            'item_text': 'A new list item'
        })

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
    
        '''
        self.assertIn('A new list item', response.content.decode())
        #at first, we return HttpResponse so this will fail, but we change it to return home.html
        self.assertTemplateUsed(response, 'home.html')
        '''

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        
        #assrtRedirects replaces the 2 lines below
        #self.assertEqual(response.status_code, 302)
        #self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')