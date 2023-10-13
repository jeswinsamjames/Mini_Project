from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime

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
        time.sleep(1)
        login=driver.find_element(By.CSS_SELECTOR,"a[href='/login']")
        login.click()
        time.sleep(1)
        username=driver.find_element(By.CSS_SELECTOR,"#username")
        username.send_keys('user2')
        time.sleep(1)
        password=driver.find_element(By.CSS_SELECTOR,"#id_password")
        password.send_keys('qweasdzxc@123')
        time.sleep(1)
        logincl=driver.find_element(By.CSS_SELECTOR,"#submit")
        logincl.click()
        time.sleep(1)
        course=driver.find_element(By.CSS_SELECTOR,"a[href='/view_catgories']")
        course.click()
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 1200)")
        time.sleep(1)
        category=driver.find_element(By.CSS_SELECTOR,"a[type='button'][href='/courses/VIOLIN']")
        action = ActionChains(driver)
        action.move_to_element(category).perform()
        action.click()
        category.click()
        time.sleep(1)
        course=driver.find_element(By.CSS_SELECTOR,"a[href='/logout']")
        course.click()
        time.sleep(1)

    def test_02_login_page(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)
        login=driver.find_element(By.CSS_SELECTOR,"a[href='/login']")
        login.click()
        time.sleep(1)
        username=driver.find_element(By.CSS_SELECTOR,"#username")
        username.send_keys('midhun')
        time.sleep(1)
        password=driver.find_element(By.CSS_SELECTOR,"#id_password")
        password.send_keys('qweasdzxc@123')
        time.sleep(2)
        logincl=driver.find_element(By.CSS_SELECTOR,"#submit")
        logincl.click()
        time.sleep(2)
        createcourse=driver.find_element(By.CSS_SELECTOR,"a[href='/enrolled-courses/']")
        createcourse.click()
        time.sleep(2)
        viewl=driver.find_element(By.CSS_SELECTOR,"a[href='/add_module_and_lesson_material/3/']")
        viewl.click()
        time.sleep(2)
        module=driver.find_element(By.CSS_SELECTOR,"#module-tab")
        module.click()
        time.sleep(2)
        title=driver.find_element(By.CSS_SELECTOR,"input[type='text'][name='title']")
        title.send_keys('module 4')
        time.sleep(2)
        titlen=driver.find_element(By.CSS_SELECTOR,"input[type='number'][name='module_number']")
        titlen.send_keys('4')
        time.sleep(2)
        module=driver.find_element(By.CSS_SELECTOR,"button[type='submit']")
        module.click()
        time.sleep(2)
        macourse=driver.find_element(By.CSS_SELECTOR,"a[href='/manage-courses/']")
        macourse.click()
        time.sleep(2)
        editcourse=driver.find_element(By.CSS_SELECTOR,"a[href='/edit-course/3/']")
        editcourse.click()
        time.sleep(2)
        editcoursen=driver.find_element(By.CSS_SELECTOR,"#id_name")
        editcoursen.send_keys('sdfsd')
        time.sleep(2)
        save=driver.find_element(By.CSS_SELECTOR,"button[type='submit']")
        save.click()
        time.sleep(2)
        mnmo=driver.find_element(By.CSS_SELECTOR,"a[href='/list_modules/']")
        mnmo.click()
        time.sleep(2)
        mnmovi=driver.find_element(By.CSS_SELECTOR,"a[href='/module_list_view/3/']")
        mnmovi.click()
        time.sleep(2)
        mnmovidl=driver.find_element(By.CSS_SELECTOR,"a[href='/delete_module/20/']")
        mnmovidl.click()
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(2)
        dlt=driver.find_element(By.CSS_SELECTOR,"a[href='/logout']")
        dlt.click()
        time.sleep(2)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(2)

    def test_03_login_page(self):
            driver = self.driver
            driver.get(self.live_server_url)
            driver.maximize_window()
            time.sleep(1)
            login=driver.find_element(By.CSS_SELECTOR,"a[href='/login']")
            login.click()
            time.sleep(1)
            username=driver.find_element(By.CSS_SELECTOR,"#username")
            username.send_keys('jeswins2024')
            time.sleep(1)
            password=driver.find_element(By.CSS_SELECTOR,"#id_password")
            password.send_keys('jeswinsam123')
            time.sleep(2)
            logincl=driver.find_element(By.CSS_SELECTOR,"#submit")
            logincl.click()
            time.sleep(2)
            viewp=driver.find_element(By.CSS_SELECTOR,"a[href='/admin_view_profile']")
            viewp.click()
            time.sleep(2)
            edib=driver.find_element(By.CSS_SELECTOR,"#edit-button")
            edib.click()
            time.sleep(2) 
            first=driver.find_element(By.CSS_SELECTOR,"#id_first_name")
            first.send_keys('mm')
            time.sleep(2)
            first=driver.find_element(By.CSS_SELECTOR,"#save-button")
            first.click()
            time.sleep(2)    
            dlt=driver.find_element(By.CSS_SELECTOR,"a[href='/logout']")
            dlt.click()
            time.sleep(2)
            alert = driver.switch_to.alert
            alert.accept()
            time.sleep(2)



        # input_date = "12-10-2023T14:21"
        # wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
        # start_datetime_input = wait.until(
        #     EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='datetime-local'][name='start_datetime'][id='id_start_datetime'][required]"))
        # )

        # # Input the date and time in the desired format into the input field
        # start_datetime_input.send_keys(input_date)
        # time.sleep(2)
        # link=driver.find_element(By.CSS_SELECTOR,"input[type='text'][name='meeting_link']")
        # link.send_keys('https://meet.google.com/ihz-qjwn-jmy')
        # time.sleep(2)
        # duration=driver.find_element(By.CSS_SELECTOR,"input[type='number'][name='duration']")
        # duration.send_keys('5')
        # time.sleep(2)
        # desc=driver.find_element(By.CSS_SELECTOR,"textarea[name='description']")
        # desc.send_keys('adsfadfa')
        # time.sleep(2)
        # desc=driver.find_element(By.CSS_SELECTOR,"button[type='submit']")
        # desc.click()
        # time.sleep(10)

       


