import os
import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

    # Farshad has recently heard about a cool website where he can write a blog post and share it with others

class FunctionalTest(StaticLiveServerTestCase):

    MAX_WAIT= 5

    @classmethod
    def setUpClass(cls):
        # Start Django live server first
        super().setUpClass()
        cls.browser = webdriver.Firefox()
        if test_server := os.environ.get("TEST_SERVER"):   
            cls.live_server_url = "http://" + test_server

    @classmethod
    def tearDownClass(cls):
        try:
            cls.browser.quit()
        finally:
            super().tearDownClass()

    def tearDown(self):
        try:
            self.browser.delete_all_cookies()
        except Exception:
            pass
    
    def wait_for(self, fn):
        start_time= time.time()
        while True:
            try:
                return fn()
            
            except (AssertionError, WebDriverException):
                if (time.time() - start_time) > self.MAX_WAIT:
                    raise
                time.sleep(0.5)

    def login(self,email= 'test@gmail.com', password='test1234'):
        
        self.browser.get(self.live_server_url + reverse('login'))

        email_input= self.browser.find_element(By.ID, "email_input")
        password_input= self.browser.find_element(By.ID, "password_input")
                
        email_input.send_keys(email)
        password_input.send_keys(password)
        self.browser.find_element(By.ID, "submit").click()

    def sign_up(self,email= 'test@gmail.com',username= 'test',password='test1234'):

        self.browser.get(f"{self.live_server_url}{reverse('sign_up')}")
        email_input= self.browser.find_element(By.ID, "email_input")
        username_input= self.browser.find_element(By.ID, "username_input")
        password_input= self.browser.find_element(By.ID, "password_input")
        
        self.browser.find_element(By.NAME, "captcha_1").send_keys("passed")

        email_input.send_keys(email)
        username_input.send_keys(username)
        password_input.send_keys(password)
        self.browser.find_element(By.ID, "submit_button").click()

    def create_post(self, header='header test', body= 'body test'):

        self.browser.get(f"{self.live_server_url}{reverse('posts:create_post')}")
        self.browser.find_element(By.ID, 'post_form')
        header_input = self.browser.find_element(By.NAME, 'header_input')
        body_input = self.browser.find_element(By.NAME, 'body_input')

        header_input.send_keys(header)
        body_input.send_keys(body)
        self.browser.find_element(By.ID, 'submit').click()