import time
from datetime import date, timedelta
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import re

class Data_miner:
    """recieved a data from Upgates - eshop administration - turnovers"""
    profile = FirefoxProfile(
        "C:\\Users\\rober\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\a36p2r7u.default-release")
    #possible use autologin
    driver = webdriver.Firefox(profile, executable_path=GeckoDriverManager().install())
    #possible load gecko directly
    x = date.today() - timedelta(days=1) #miner is getting yesterday data
    day_month = (x.strftime("%d"))+"."+(x.strftime("%m"))+"." #format in online administration

    def __init__(self):
        self.list_name = [] #orders + turnover

    def load_page(self, adress):
        self.driver.get(adress)  # loading a page
        time.sleep(2)  #eliminate bad loading time..:/
        self.html_parse = self.driver.page_source
        self.html_source = BeautifulSoup(
            self.html_parse, "html.parser") #parsing html
        #mining turnover and number of order
        for tag in self.html_source.find_all("td", text=re.compile(self.day_month)):
            #looking for all tag which have "td" tag equal to day month
            self.record = tag.find_next('td').get_text() #getting turnover 
            self.list_name.append(self.record) #append values to final list
        # tags contains useless values - getting rid of them
        self.list_name = [gap.replace('\xa0', '')
                            for gap in self.list_name]
        #finally change values to an integers ones
        self.list_name = [int(i) for i in self.list_name]
        return self.list_name
