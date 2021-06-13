from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from django.template.loader import render_to_string

from lists.views import home_page

from lists.models import Item, List

# Run with 'python manage.py test lists'

class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):

        #HttpRequest is what django sees when browser asks for page
        #request = HttpRequest()

        #pass to home_page view and receive response in form of HttpResponse object
        #response = home_page(request)

        """
        We should never test constants, which is why we don't return
        Httprequests in views.py, instead use a function to get templates
        where home.html is and return html from there.
        This is refractoring code, where we only change format and not actual function
        This test below tests if views.home_page actually returns the template
        """
        # Manually creating a request:
        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))
        
        # test method Django's TestCase provides that checks what template used to render a response
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

class ListViewTest(TestCase):
    
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        #instead of "assertIn" with "response.content.decode", assertContains
        #knows how to deal with responses and bytes of their content
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        #response.context is the context we pass into the render function
        self.assertEqual(response.context['list'], correct_list)

