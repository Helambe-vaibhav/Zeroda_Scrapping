
import datetime
import requests
import json
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from AllFunctions import *

class scrape_stock_data:

    def __init__(self,end_date,cur_path,timeframe = 3,headless=True):
        # self.start_date = start_date
        self.end_date = end_date
        self.start_date = str(datetime.datetime.strptime(self.end_date, '%Y-%m-%d') - datetime.timedelta(days=85))[0:10]
        self.timeframe = timeframe
        self.cur_path = cur_path
        self.headless = headless

    def check_dir(self):
        check_dir(self.cur_path)

    def get_credentials(self):
        self.username,self.password,self.pin = get_credentials()

    def login(self):
        root_url = 'https://kite.zerodha.com/orders'
        service = webdriver.firefox.service.Service("D:\softwares\software ssetup\geckodriver.exe")
        service.start()
        options = Options()
        options.headless = self.headless
        self.driver = webdriver.Remote(service.service_url, options=options)
        self.driver.get(root_url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "userid")))
        self.driver.find_element('id', 'userid').send_keys(self.username)
        self.driver.find_element('id', 'password').send_keys(self.password)
        self.driver.find_element('class name', 'actions').click()
        time.sleep(15)
        print("Login successful")
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, "//a[@class='orders-nav-item router-link-exact-active router-link-active']")))
        self.cookies = self.driver.get_cookies()
        print("Cookies extracted")

    def get_auth_token(self):
        self.auth_token = get_auth_token(self.cookies)


    def get_stock_metadata(self):
        with open('stock_metadata.txt', 'r') as f:
            stock_metadata = json.load(f)
        metadata_df = pd.DataFrame(stock_metadata['items'])
        metadata_df = metadata_df[['tradingsymbol','instrument_token']]
        self.metadata = metadata_df.set_index('tradingsymbol').to_dict()['instrument_token']
        print("Stock metadata loaded")

    def get_request_url(self,stock):
        self.request_url = f"https://kite.zerodha.com/oms/instruments/historical/{stock}/{self.timeframe}minute?user_id=PH2878&oi=1&from={self.start_date}&to={self.end_date}"
        # print("Request url generated")
        # print(self.request_url)

    def get_json_response(self):
        json_response = requests.get(self.request_url,headers={'Authorization':self.auth_token})
        if json_response.status_code != 200:
            print(json_response.status_code,json_response.reason)
            print("Error in getting response")
        self.data_dict = json.loads(json_response.text)
        # print("Response received")

    def data_to_df(self):
        data_df = pd.DataFrame(self.data_dict['data']['candles'])

        print(data_df)
        # renaming dataframe column headers
        data_df.rename(columns = {0:'Datetime',1:'Open',2:'High',3:'Low',4:'Close',5:'Volume',6:'OI'},inplace=True)
        data_df['Date'] = pd.to_datetime(data_df['Datetime']).dt.date
        data_df['Time'] = pd.to_datetime(data_df['Datetime']).dt.time

        data_df.drop('Datetime',axis=1,inplace=True)
        self.data_df = data_df[['Date','Time','Open','High','Low','Close','Volume','OI']]
        # self.data_df.set_index('Date',inplace=True)
        print(self.data_df.head())

    def save_data(self,stock):
        current_parent_path = os.path.dirname(os.path.realpath(__file__))
        saving_path = os.path.join(current_parent_path,r'{cur_path}\{stock}.csv'.format(cur_path=self.cur_path,stock=stock))
        self.data_df.to_csv(saving_path,index=False)
        print(saving_path)
        print(self.data_df)
        print(f"Data for {stock} saved")

    def scraping(self):
        self.check_dir()
        self.get_stock_metadata()
        self.get_credentials()
        self.login()
        self.get_auth_token()
        for i in self.metadata:
            stock = self.metadata[i]
            self.get_request_url(stock)
            self.get_json_response()
            self.data_to_df()
            self.save_data(i)
        print('Done')

import  time
s = time.time()
print(s)
obj= scrape_stock_data('2023-01-25','25 Jan 2023',headless= False)
obj.scraping()
print(time.time()-s)
