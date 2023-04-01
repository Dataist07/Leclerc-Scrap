import pickle
import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

if __name__ == '__main__':
    options = Options()
    options.add_experimental_option('detach', True)

    path ="C:\Program Files (x86)\chromedriver.exe"
    driver = uc.Chrome() 

    driver.get("https://fd11-courses.leclercdrive.fr/magasin-018201-montauban---sapiac.aspx")
    driver.maximize_window()
    time.sleep(20)

    cookies = driver.get_cookies()
    pickle.dump(cookies, open("cookies.pkl", "wb"))

    time.sleep(10)




