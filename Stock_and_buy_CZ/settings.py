#!/usr/bin/python3

"""________________________________[ MODULY PRO CELEK ]"________________________________"""
import gspread #ok
from oauth2client.service_account import ServiceAccountCredentials 
import requests  # pip3 install requests
from bs4 import BeautifulSoup # pip3 install beautifulsoup4
from boltons.setutils import IndexedSet #pip3 install boltons
import tabula #tabula netřeba na server
from tabula import read_pdf #též netřeba na ubuntu
import csv #též netřeba na ubuntu
import os #též netřeba
from lxml import etree #sudo apt-get install python3-lxml
from lxml.builder import E #není instalačka
from timeit import default_timer as timer #netřeba už je
from retrying import retry #pip3 install retry
from datetime import datetime #pip3 install Datetime
from apscheduler.schedulers.blocking import BlockingScheduler #pip3 install APScheduler
import time
import json
from requests.auth import HTTPBasicAuth
import pprint
import sys

#adresa = ".\credentials.json"
#adresa = "C:\\Users\\thon\\OneDrive\\Plocha\\Upgrade\\Python\\Django\\Django SKLAD\\SKLAD_CELEK\\credentials.json"
"""________________________________[ PROPOJENÍ GOOGLE SHEETS ]"________________________________"""
#Základní propojení Google Sheets
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(credentials) #používá json soubor pro autorizaci

#URLČKA PRO FEEDY - daily upload vždy v 4:00
nabitabaterka_url = "nabitabaterka.xml"
yescom_url = "yescom.xmll"
ep_url = "ep.xml"

"""___________________________________[ PROPOJENÍ S API ]"____________________________________"""

url_nb = "https://nabitabaterka.admin.s10.upgates.com/api/v2/products"
heslo_nb ="xxxxxxxxxxxxxxxxxxx" 
jmeno_nb ="nabitabaterka"

url_yescom = "https://yescom.admin.s5.upgates.com/api/v2/products"
heslo_yescom = "xxxxxxxxxxxxxxxxxxx"
jmeno_yescom = "yescom"

url_ep = "https://easy-print.admin.s5.upgates.com/api/v2/products"
heslo_ep = "xxxxxxxxxxxxxxxxxxx"
jmeno_ep = "easy-print"




