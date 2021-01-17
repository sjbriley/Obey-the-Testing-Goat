from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

#Functional tests test the application from the outside
#Unit tests test from a developers POV

#Make sure 'TestCase' is capitized
class NewVisitorTest(unittest.TestCase):

    #Make sure the 'Up' and the 'Down' are capitlized
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
    
    #unittest automatically runs any function that starts with 'test'
    #also always runs setUp first, then finishes with tearDown no matter what
    def test_Start(self):
        
        #Edith heads to the homepage of a to-do page
        self.browser.get('http://localhost:8000')

        #She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #She is invited to enter a to-do immediately
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        
        #she types 'Buy peacock feathers' into the text box
        inputbox.send_keys('Buy peacock feathers')

        #she hits enter and the page updates listing
        #'1: Buy peacock feathers' as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        #give page a second to load before we make new assertions
        #called an 'explicit wait'
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_element_by_tag_name('tr')
        self.assertTrue(any(row.text == '1: Buy peacock feathers' for row in rows), "New to-do item did not appear in table")

        #there is still a text box inviting her to add another item
        #she enters 'Use peacock feathers to make a fly"
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main()