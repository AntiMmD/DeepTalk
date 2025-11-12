from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from .base import FunctionalTest

class StaticFilesSmokeTest(FunctionalTest):
    def setUp(self):
        production_server = os.environ.get("PRODUCTION_SERVER")
        if production_server:
            self.live_server_url = f"http://{production_server}"

    def test_static_files_are_served_correctly(self):
        # Farshid goes to the home page
        self.browser.get(self.live_server_url)
        
        # His browser window is set to a very specific size
        self.browser.set_window_size(1024, 768)
        
        # He notices the create post button is located on the right side of the page
        # (Without CSS, buttons would stack vertically on the left)
        myPostsButton = self.browser.find_element(By.ID, "my_posts")
        self.wait_for(lambda: self.assertGreater(
            myPostsButton.location["x"],
            512,
            "My Posts button should be on right side if CSS loaded"
        ))
        
