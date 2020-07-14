#TODO: 1. pokrýt případnou nedostupnost obrázků
#TODO: 2. předělat na OOP? Proces je 3x stejný ale zase je to krátký kod...

import requests #pro získání url
from bs4 import BeautifulSoup #pro parsování
import wget  # potenciální fičura pro stahování obrázků
from ftplib import FTP #pro napojení na FTP
import os 
import fileinput #pravděpodobně pro import
import csv
import os
import copy
path = os.path.dirname("./")

print("Načítám a parsuji feed...") # ZÁKLADNÍ REQUEST A PARSOVÁNÍ FEEDU

response = requests.get(
    "https://b2b.greencell.global/modules/xmlgenerator/get.php?secure_key=66b3b98f99bface19e3f03d002f8e78a")
feed = BeautifulSoup(response.text, "html.parser")

"""______________________________________[USER INPUT]_____________________________________________"""

def user_input():
  """Funkce pro datový vstup - kody produktů, u kterých chceme získat jpg"""
  print("Vložte seznam produktů, jejichž obrázky chcete stáhnout\nEnter 2x pro spuštění")
  while True:
    kod = input().upper() #pokrytí case sensitive
    if kod: #takto pokryjeme ctr+c a ctrl+v
      seznam_kodu.append(kod)
    else:
      return seznam_kodu

  
"""_____________________________________[IMAGE DOWNLOAD]________________________________________"""

def stahni_obrazky(): #ve feedu jsou na 2x - main a veldejší proto 2x
   """Stáhne obrázky z feedu podle zadaného listu""" 
  for produkt in feed.find_all("o"):
    # naše podmínka => POKUD KOD Z LISTU = KOD FEEDU => STAHUJEME OBRÁZKY
    nazev_produktu = produkt.find("a", {"name": "Kod_producenta"}).get_text()
    if nazev_produktu in seznam_kodu:
        image_url = produkt.find("main")['url'] #hledám obrázky
        nazev_1 = nazev_produktu + "-0.jpg" #základní název
        seznam_nazvu.append(nazev_1) #list pro delete a upload
        nazev_dohromady = nazev_1 #generuji základ pro csv listy
        zbytek_kodu.remove(nazev_produktu) #tvoříme zbytek listu - TO co nemá shodu
        #v podstatě potřebuji sečíst všechny názvy pro produkt do jednoho řetězce
        #nazev_1 = nazev_csv
        uloz_image = wget.download(image_url, nazev_1) #uložení obrázku dle url
        i = 1 #máme main a ostatní proto na 2x-0
        for images in produkt.find_all("i"):
            image_url = images['url']         
            nazev_2 = f"{nazev_produktu}-{i}.jpg" #pro správný název
            nazev_dohromady += ";"+nazev_2 #nestíme do sebe hodnoty obrázků
            seznam_nazvu.append(nazev_2) #list pro delete a upload
            uloz_image = wget.download(image_url, nazev_2) #pro uložení
            i += 1 
        csv_nazvy_list.append(nazev_dohromady) #finální část listu pro daný produkt
         
"""____________________________________[FTP PUSH]_________________________________________________"""

def upload_to_ftp(adresa, jmeno, heslo):
  """Funkce pro připojení na FTP a upload obrázků do složky"""
  ftp = FTP()
  ftp.set_debuglevel(2)
  ftp.connect(adresa, 21) 
  ftp.login(jmeno, heslo) #řádky sloužící k zalogování
  ftp.cwd('/money-import') #určení kam se bude uploadovat
  for obrazek in seznam_nazvu:
    file_muj= open(obrazek, 'rb') #projede všechny obrázky a uploaduje je..
    ftp.storbinary(f'STOR {obrazek}', file_muj)
  file_muj.close()
  ftp.quit() #po uploadu ukončí
    
"""_____________________________________[IMAGE DELETE]_______________________________________________"""
def delete_images():
   """Funkce na odmazání obrázků po uploaudu"""
  for obrazek in seznam_nazvu:
    os.remove(obrazek)
    print(f"Mažu: {obrazek}") #stáhne - uploadne - smaže
"""_____________________________________[CSV CREATE]_______________________________________________"""

def vytvor_csv_import(jazyk, dodatek_kodu=""):
   """#Funkce pro vytvoření CSV k importu"""
    with open(f"{jazyk}-import-obrazku.csv", 'w', newline='') as file:
        writer = csv.writer(file, delimiter = ';') #pro excel lepší středník
        writer.writerow(["[PRODUCT_CODE]", "[IMAGES]", "[LANGUAGE]"]) #header csv
        for i in range(len(seznam_kodu)): #a zde udaje - délka listu = počtu řádků
          #a též logicky i definuje i jejich hodnoty
            writer.writerow([seznam_kodu[i]+dodatek_kodu, csv_nazvy_list[i], jazyk])
            
"""__________________________________[MAIN - BEZ MAINU :)]_________________________________________________"""

#TODO - předělat na main a pokrýt možné výpadky => TRY-EXCEPT-CONTINUE-FINALLY ideálně

seznam_kodu, seznam_nazvu, csv_nazvy_list = [], [], []
user_input()
zbytek_kodu = copy.deepcopy(seznam_kodu)  #tvořími deepcopy pro to co zbude
stahni_obrazky()
try:
  upload_to_ftp("ftp.s5.upgates.com","project_connections_2889","gdpb97rx")
  upload_to_ftp("ftp.s5.upgates.com","project_connections_2891","nacpgm7d")
  upload_to_ftp("ftp.s10.upgates.com","project_connections_3614","oai3xe9t")
  delete_images()
  koncovka_produktu = input("Tvoříme csv - zadej koncovku produktu: ")
  vytvor_csv_import("cz",koncovka_produktu) #druhý volitelný - dodatek k product kodu
  vytvor_csv_import("sk",koncovka_produktu) #druhý volitelný - dodatek k product kodu
except:
  print("Žádné kody ze zadání nejsou ve feedu")
print("Kody nenalezene ve feedu:",zbytek_kodu)
