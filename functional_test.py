from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
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

        # Farshad immediately notices the page title and header mentioning 'Monologue'
        header_text = self.browser.find_element( By.TAG_NAME, 'h1' ).text
        self.assertIn('Welcome to Monologue!' , self.browser.title)
        self.assertEqual('Monologue!' , header_text)
        
        # he can see a button under the header which reads as "create a post"
        button = self.browser.find_element(By.ID, 'create_post_button')

        self.assertEqual('create a post', button.text.lower())
        button.click()
        time.sleep(1)
        # he sees a form where he can type in a heading and the body of the post
        self.browser.find_element(By.ID, 'post_heading')
        self.browser.find_element(By.ID, 'post_body')

        # after creating the post, he submits it and the site redirects him where he can see his post 
        # satisfied by the result, he closes the browser, excited to see if anyone actually reads him or not 

        self.fail('finish the test')


if __name__ == '__main__':
    unittest.main()

