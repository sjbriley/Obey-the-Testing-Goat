from selenium import webdriver
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
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main()