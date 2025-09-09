from selenium import webdriver
import unittest

        # Farshad has recently heard about a cool website where he can write a blog post and share it with others
        # he opens his browser and checks the homepage 

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_see_the_homepage(self):
        self.browser.get('http://localhost:8000/')
        self.assertIn('Welcome to Monologue!' , self.browser.title)

        self.fail('finish the test')
        # Farshad is immediately welcomed by a button at the top of the site which invites him to create a post 
        # he sees a form where he can type in a heading and the body of the post
        # after creating the post, he submits it and the site redirects him where he can see his post 
        # satisfied by the result, he closes the browser, excited to see if anyone actually reads him or not 
    
if __name__ == '__main__':
    unittest.main()

