from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Hosttest(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'

    def tearDown(self):
        self.driver.quit()

    

    def test_01_login_page(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(2)
        login=driver.find_element(By.CSS_SELECTOR,"a[href='/login']")
        login.click()
        time.sleep(2)
        username=driver.find_element(By.CSS_SELECTOR,"#username")
        username.send_keys('user2')
        time.sleep(2)
        password=driver.find_element(By.CSS_SELECTOR,"#id_password")
        password.send_keys('qweasdzxc@123')
        time.sleep(2)
        logincl=driver.find_element(By.CSS_SELECTOR,"#submit")
        logincl.click()
        time.sleep(2)
        course=driver.find_element(By.CSS_SELECTOR,"a[href='/view_catgories']")
        course.click()
        time.sleep(2)
        category=driver.find_element(By.CSS_SELECTOR,"a[type='button'][href='/courses/PIANO']")
        action = ActionChains(driver)
        action.move_to_element(category).perform()
        time.sleep(2)


