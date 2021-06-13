#from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from selenium.common.exceptions import WebDriverException
# from django.test import LiveServerTestCase
#from django.contrib.staticfiles.testing import StaticLiveServerTestCase # we need STATIC to be able to handle our static files (css and bootsrap)
#from unittest import skip
#import time
#import unittest
#import os
from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):
    
    def test_layout_and_styling(self):
        """
        usually we do not test static things such as layout/css
        however, it can be good to do a very basic test to make sure things are in order
        """
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # she notices the input box is nicely centered
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta = 10
        )

        # she starts a new list and sees input is also nicely centered
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta = 10
        )

#Now that we use LiveServerTestCase and created a new folder with init file, we don't need this
'''
if __name__ == '__main__':
    unittest.main()
'''