import requests
import webbrowser
from bs4 import BeautifulSoup

url_feed = "b2b-adress.html" #not a real adress, hidden

def product_code_input():
    """mass input using ctrl+c/ctrl+v"""
    print("Insert the product codes and hit Enter: ")
    enter_products = []
    task = True
    while task:
        kod = input().upper() #codes are always upper
        if kod: #loop for mass input ability
            enter_products.append(kod)
        else:
            task = False
    return enter_products #input result
    
def feed_check(enter_products, feed):
    """accepting list of product codes and compare codes with feed"""
    names_gc = []
    for produkt in feed.find_all("o"):#path to product code "o" -> "a"
        #feed product info example <a name="Kod_producenta">HP01</a> 
        nazev_produktu = produkt.find("a", {"name": "Kod_producenta"}).get_text()
        names_gc.append(nazev_produktu) #creating a list with names from feed
        #TODO: SHOUDL BE SOLVED with generator faster and better solution!
    for produkt_dif in enter_products:
        if produkt_dif in names_gc:
            pass #if input equal with feed 
        else: #looking only for differences
            print(produkt_dif) 

def main(adresa_feedu):
    print("Parsing the feed, please wait :)...")
    response = requests.get(url_feed) #get an adress
    #parsing - using BeatifulSoup 
    feed = BeautifulSoup(response.text, "html.parser")
    enter_products = product_code_input() #accepting an input
    feed_check(enter_products, feed) #comparing the differences

if __name__ == "__main__":
    main(url_feed)
