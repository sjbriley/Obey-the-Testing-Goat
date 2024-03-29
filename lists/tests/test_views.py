from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from django.template.loader import render_to_string

from lists.views import home_page

from lists.models import Item, List
from django.utils.html import escape
from lists.forms import ItemForm, EMPTY_ITEM_ERROR


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
        
    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

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

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/',
            data = {'text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data = {'text': 'A new item for an existing list'}
        )
        
        self.assertRedirects(response, f'/lists/{correct_list.id}/')
    """
    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.id}/',data={'text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
    """  
    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')        
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')
        
    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(f'/lists/{list_.id}/', data={'text':''})

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)
    
    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
    
    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)
    
    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))
        
    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(
            f'/lists/{list1.id}/',
            data={'text':'textey'}
        )
        
        expected_error = escape("You've already got this in your list")
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.asssertEqual(Item.objects.all().count(), 1)
        
class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        # we leave off trailing slash after /new because /new is action URL which modify database
        self.client.post('/lists/new', data={
            'text': 'A new list item'
        })

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        new_list = List.objects.first()

        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        # escape is used because django would prior change apostrophe to something else by HTML-escape
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text':''})
        self.assertEqual(List.objects.count(),0)
        self.assertEqual(Item.objects.count(),0)

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertIsInstance(response.context['form'], ItemForm)
