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

        self.browser.find_element(By.ID, 'post_form')
        header = self.browser.find_element(By.NAME, 'header_input')
        body = self.browser.find_element(By.NAME, 'body_input')

        self.assertEqual(header.get_attribute('placeholder'), 'Enter the heading')
        self.assertEqual(body.get_attribute('placeholder'), 'Enter the body')

        # Farshad wants to write a post about extreme climate and its effects on puppies 
        header.send_keys('extreme climate and its effects on puppies')

        body.send_keys('Extreme climate, whether scorching heat or freezing cold, can severely affect puppies.' \
        'High temperatures can cause dehydration and heatstroke, while extreme cold can lead to hypothermia'
        ' and frostbite. Puppies are especially vulnerable because their bodies cannot regulate temperature' \
        ' well. Proper shelter, hydration, and care are essential to keep them safe in harsh weather.')

        # after creating the post, he clicks the submit button and it redirects him where he can see his post 
        self.browser.find_element(By.TAG_NAME, 'button').click()
        posted_header= self.browser.find_element(By.ID, 'posted_header').text
        posted_body = self.browser.find_element(By.ID, 'posted_body').text

        self.assertEqual(posted_header, "extreme climate and its effects on puppies")
        self.assertIn("Puppies are especially vulnerable because their bodies cannot regulate temperature", posted_body)


        # satisfied by the result, he closes the browser, excited to see if anyone actually reads him or not 

        self.fail('finish the test')


if __name__ == '__main__':
    unittest.main()

