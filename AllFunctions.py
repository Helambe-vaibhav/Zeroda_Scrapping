import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
from math import exp
from ta.utils import IndicatorMixin

def get_credentials():
    # Read credentials from file
    with open('credential.txt', 'r') as f:
        username = f.readline().strip()
        password = f.readline().strip()
        pin = f.readline().strip()
    print("Credentials loaded")
    return username, password, pin

def check_dir(cur_path):
    # Check if directory exists, if not create it
    if not os.path.exists(cur_path):
        os.makedirs(cur_path)
    else:
        print("Directory already exists")
        pass
    return cur_path

def login(username,password,pin,headless = False):
    # Create a new instance of the Firefox driver and login
    root_url = 'https://kite.zerodha.com/orders'
    service = webdriver.firefox.service.Service("geckodriver.exe")
    service.start()
    options = Options()
    options.headless = headless
    driver = webdriver.Remote(service.service_url, options=options)
    driver.get(root_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "userid")))
    driver.find_element('id' ,'userid').send_keys(username)
    driver.find_element('id' ,'password').send_keys(password)
    driver.find_element('class name','actions').click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".su-input-group > input:nth-child(2)")))
    driver.find_element('css selector', '.su-input-group > input:nth-child(2)').send_keys(pin)
    driver.find_element('class name','actions').click()
    print("Login successful")
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, "//a[@class='orders-nav-item router-link-exact-active router-link-active']")))
    cookies = driver.get_cookies()
    print("Cookies extracted")
    return driver,cookies

def get_auth_token(cookies):
    # Extract auth token from cookies
    print(cookies)
    for i in range(len(cookies)):
        if 'enctoken' in cookies[i].values():
            auth_token = cookies[i]['name'] + ' ' + cookies[i]['value']
    print("Auth token extracted")
    return auth_token
