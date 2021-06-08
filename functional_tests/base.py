from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase # we need STATIC to be able to handle our static files (css and bootsrap)
#from unittest import skip
import time
#import unittest
import os

MAX_WAIT = 10

#Functional tests test the application from the outside
#Unit tests test from a developers POV

#Make sure 'TestCase' is capitized
class FunctionalTest(StaticLiveServerTestCase):

    #Make sure the 'Up' and the 'Down' are capitlized
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            pass
            #self.live_server_url = 'http://' + staging_server # live_server_url is StaticLiveServerTestCase default own test server, so we change to real server
        self.live_server_url = 'http://mydjangoproject.xyz'
        self.live_server_url = 'http://127.0.0.1:8000/'

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


#Now that we use LiveServerTestCase and created a new folder with init file, we don't need this
'''
if __name__ == '__main__':
    unittest.main()
'''