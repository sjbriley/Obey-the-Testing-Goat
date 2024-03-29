#from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
# from django.test import LiveServerTestCase
#from django.contrib.staticfiles.testing import StaticLiveServerTestCase # we need STATIC to be able to handle our static files (css and bootsrap)
from unittest import skip
import time
#import unittest
#import os
from .base import FunctionalTest

MAX_WAIT = 10

class ItemValidationTest(FunctionalTest):
    
    def test_cannot_add_empty_list_items(self):
        # Edith accidently submits an empty list item with
        # She receives an error message
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'  
        ))

        
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'  
        ))

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        
        # she decides to submit a second blank item
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))
        
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')
        
    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy Wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy Wellies')

        # edith accidently enters the same item twice
        self.get_item_input_box().send_keys('Buy Wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # she sees an error message
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You've already got this in your list"
        ))
        
    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
        
        

#Now that we use LiveServerTestCase and created a new folder with init file, we don't need this
'''
if __name__ == '__main__':
    unittest.main()
'''