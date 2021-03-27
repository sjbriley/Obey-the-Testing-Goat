from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase # we need STATIC to be able to handle our static files (css and bootsrap)
import time
import unittest
import os

MAX_WAIT = 10

#Functional tests test the application from the outside
#Unit tests test from a developers POV

#Make sure 'TestCase' is capitized
class NewVisitorTest(StaticLiveServerTestCase):

    #Make sure the 'Up' and the 'Down' are capitlized
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server # live_server_url is StaticLiveServerTestCase default own test server, so we change to real server

    def tearDown(self):
        self.browser.quit()
    
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows], f"New to-do item did not appear in table. Contents were: \n{table.text}")
                return
            # This checks for 2 exceptions-webdriverexception if page hasn't loaded
            # and assertionerror is when table is there but hasn't reloaded (missing our row)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

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

    def test_layout_and_styling(self):
        """
        usually we do not test static things such as layout/css
        however, it can be good to do a very basic test to make sure things are in order
        """
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # she notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta = 10
        )

        # she starts a new list and sees input is also nicely centered
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
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