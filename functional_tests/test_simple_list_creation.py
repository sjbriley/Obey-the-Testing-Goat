#from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
# from django.test import LiveServerTestCase
#from django.contrib.staticfiles.testing import StaticLiveServerTestCase # we need STATIC to be able to handle our static files (css and bootsrap)
#from unittest import skip
#import time
#import unittest
#import os
from .base import FunctionalTest

class NewVisitorTest(FunctionalTest):
    # unittest automatically runs any function that starts with 'test'
    # also always runs setUp first, then finishes with tearDown no matter what
    def test_can_start_a_list_for_one_user(self):
        
        # Edith heads to the homepage of a to-do page
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do immediately
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        
        # she types 'Buy peacock feathers' into the text box
        inputbox.send_keys('Buy peacock feathers')

        # she hits enter and the page updates listing
        # '1: Buy peacock feathers' as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        # give page a second to load before we make new assertions
        # called an 'explicit wait'
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # There is another page inviting her to make a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        # she types a new to-do item in:
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates and now shows her items on her list
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # she notices her list has a unique URL
        edith_list_url = self.browser.current_url
        # assertRegex is from unittest that checks if string matches regular expression
        self.assertRegex(edith_list_url, '/lists/.+')

        # a new user, francis, comes
        # We use new browser session to reset Ediths cookies
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # francis visits homepage, no sign of edith
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # francis starts a new list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # again, there is no trace of ediths list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

#Now that we use LiveServerTestCase and created a new folder with init file, we don't need this
'''
if __name__ == '__main__':
    unittest.main()
'''