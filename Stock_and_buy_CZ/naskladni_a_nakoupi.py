from settings import * #není v rámci dobrých mravů
from collections import Counter
import webbrowser  
from selenium import webdriver  
from webdriver_manager.firefox import GeckoDriverManager  
from selenium.webdriver.firefox.webdriver import FirefoxProfile 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 

#TODO rozdělit na část získání dat a nákupúu do 2 .py souborů

"""____________________________________[ DATA K OBJEDNAVCE ]____________________________________"""
def objednavka_data():
    """ZÍSKÁ DATA K OBEJDNÁVCE - z google sheets skladu přes API -"""
    sheet1 = client.open('sklad_gc_dynamic').get_worksheet(3) #otevře list kde jsou data
    #definuji dva listy - kody a pocty - krátím o prvních 10 a druhý list převádím na int
    kody, pocty = sheet1.col_values(1)[10:], list(map(int,sheet1.col_values(2)[10:]))
    #funkce list-map-int pro převod na int
    #list(map(int(sheet1.col_values(2)[10:])))
    objednavka = dict(zip(kody,pocty)) #vytvořím si objednávkový dictionary - kody a pocty
    return objednavka

"""____________________________________[ SEZNAM FAKTUR ]____________________________________"""

def faktury_data():
    """User input pro seznam faktur - většinou pouze 1 ale občas i více"""
    faktury = []
    print("_Nakupovač.v2.0\n")
    print("Instrukce: Vaše faktury musí být ve stejné složce jako tento program.")
    print("Doporučuji přejmenovat faktury na snadné jméno.\n") #neřeším str zadání netřeba
    opakuj = True
    while opakuj:
        try: #zjistíme počet faktur
            pocet_faktur = int(input("Zadejte prosím počet faktur: ")) 
            opakuj = False
        except:
            print("Zadej číslo")
            opakuj = True
    while pocet_faktur != 0: #zjištuji názvy - dokud nezadají správné
        faktura = "./"+ input("Zadejte prosím název faktury, bez koncovky: ") +".pdf"
        if os.path.isfile(faktura): #kontroluji umístění
            faktury.append(faktura)
            pocet_faktur -=1 #snižuji počet faktur dokud nedocílím 0
        else: #pokud zadají špatné musí znovu
            print("Zadali jste špatné jméno faktury, prosím znovu")
    return faktury

"""____________________________________[ DATA Z FAKTURY]"___________________________"""

#TÉŽ PRO NASKLADNOVAČE
#LZE POTÉ PŘEDĚLAT NA FUNKCI CO ŘEŠÍ DOLOVÁNÍ FAKTURY - ABY SE VŠE ZJEDNODUŠILO 
def doluj_data_z_faktury():
    """ZÍSKÁ DATA Z FAKTUR - kody a počty - PRO PRŮNIK S OBJEDNÁVKOU"""
    faktury = faktury_data()
    suma_faktur = []
    for faktura in faktury: #proiteruji moje faktury a zavedu je do dt
        i = 1
        tabula.convert_into(faktura, (f"./{faktura}_naskladneni.csv"), output_format="csv", pages='all')
        with open(f"{faktura}_naskladneni.csv", 'r') as file: #otvírám csv a projedu řádky
            reader = csv.reader(file)
            dt_sklady_nazvy = {} #musím nulovat dictionary zde
            for row in reader:
                try:#podmínka je pcs nebo szt - lze změnit za jiné
                    if "szt" in row[5] or "pcs" in row[5]:
                        #pokud máme řádek s kusy - dolujeme kod a počet
                        if row[1] != "EU01":
                            dt_sklady_nazvy[row[1]] = int(row[4])
                            dt_sklady_nazvy[row[1]]
                    elif "szt" in row[4] or "pcs" in row[4]:
                        #pokud máme řádek s kusy - dolujeme kod a počet
                        if row[1] != "EU01":
                            dt_sklady_nazvy[row[1]] = int(row[3])
                except: #pokud podmínka není - neřešíme
                    pass
            print(f"Celkový počet položek ve fakuře-{i}: {len(dt_sklady_nazvy)}")
            i +=1
        if len(faktury) > 1: #operace pouze pro 2 a více faktur
            suma_faktur.append(dict(dt_sklady_nazvy)) #sbírám dt - může být více f
    if len(faktury) > 1: #operace pouze pro dvě a více faktur
        dt_sklady_nazvy = Counter(suma_faktur[0]) + Counter(suma_faktur[1])
    return dt_sklady_nazvy
  
"""____________________________________[ FINÁLNÍ DATA]"___________________________"""

def finalni_data():
    """TVORBA FINÁLNÍ MNOŽINY - CO OBJEDNAT, DATA Z OBJEDNÁVKY - DATA Z FAKTUR NA CESTĚ"""
    produkty_r, pocty_r = [], []
    objednavka = objednavka_data() #data z excelu pro objednavku
    dt_sklady_nazvy = doluj_data_z_faktury() #data z faktur
    for produkt, pocet in dt_sklady_nazvy.items(): #vydoluji rozdíly
        if produkt in objednavka:
            print(f"Objednávka snížena o {produkt} X {pocet}")
            produkty_r.append(produkt) #produkt z faktury
            pocty_r.append(pocet) #počet z faktury
    for i in range(len(produkty_r)):
        objednavka[produkty_r[i]] = objednavka[produkty_r[i]] - pocty_r[i]
        #objednavka[jeho_klic_o_i] = objednavka[jeho_hodnota_o_i] - hodnota_fa_o_i
        #TEHLE ZÁPIS nesnáším :/ - ale dejme tomu
    final_order = objednavka.copy() #vytvářím kopii dt pro iteraci    
    for produkt, pocet in objednavka.items(): #odmažu páry s počtem 0 a méně
        if pocet <=0:
            del final_order[produkt]
    print(f"\nFinální objednávka, která přejde k objednání: {final_order}")
    print("\nProbíhá zpracování feedu a poté objednání produktů, prosím vyčkejte.\n")
    return final_order #navracím již výsledek k prodeji

"""________________________________[NAKOUPENÍ]________________________________________"""

def nakup():
    """FINÁLNÍ NÁKUP - až bude čas provést restrukturalizaci - nečitelné"""
    zadej_produkty = finalni_data() #použije všecny fnce předtím pro získání dat
    response = requests.get(
    "https://b2b.greencell.global/modules/xmlgenerator/get.php?secure_key=66b3b98f99bface19e3f03d002f8e78a")
    feed = BeautifulSoup(response.text, "html.parser") #parsuje feed
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install()) 
    #načítá gecko pro selenium

    #Autologin do administrace - vhodné pro samostatnou fci
    driver.get("https://b2b.greencell.global/en/") 
    username = driver.find_element_by_id("email")
    password = driver.find_element_by_id("passwd")
    username.send_keys("xxxxxxxxxxxxxx")
    password.send_keys("xxxxxxxxxxxxxx")
    driver.find_element_by_name("SubmitLogin").click()

    # Definujeme si set pro evidenci úspěšných nákupů - bude odečet z dictionary
    unikatni_produkty = set()
    xpath_buy = "//*[@id='add_to_cart']/button" #xpth pro buy tlačítko
    # DOLUJEME data a nakupujeme
    for produkt in feed.find_all("o"):  # hledáme vše a přidělíme název
        nazev_produktu = produkt.find("a", {"name": "Kod_producenta"}).get_text()
        #Dolujeme kody z feedu - a budeme je porovnovávat s listem našeho nákupního seznamu
        #Jakmiel najde shodu - tzn..propojí produkt co chceme koupit s feedem - načte jeho
        #url a vloží požadované množství do košíku
        for nazev, pocet in zadej_produkty.items():
            if nazev == nazev_produktu:  # při shodě nakupujeme
                unikatni_produkty.add(nazev)  # evidence nákupů - pro odečtení z DT
                while pocet > 0:  # odečet pro správné množství nákupu
                    url = produkt["url"]  # definujeme url produktu  
                    try:
                        driver.get(url)
                        element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xpath_buy)))
                        element.click() #musí být wait obaleno .click prohlížeš jinak chybuje
                        element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xpath_buy)))
                    except:  # nákup selže ale adresa a kod správná - latency nebo skladovost
                        print(f"{nazev_produktu} se nepodařilo přidat")
                    pocet -= 1  # korekce množství z dicitonary

    # odečteme z dicitonary úspěšně nakoupené produkty - zbytek nenalezené
    for produkt in unikatni_produkty:
        del zadej_produkty[produkt]

    print(f"Produkty nenalezeny ve feedu:\n{zadej_produkty}")  # tisk nenalezených
    input("Po odkliknutí objednávky zmáčkněte Enter - uzavře se mozila i program")
    driver.close()


def main(): 
    """SPÍŠE jen kdyby bylo třeba něco doladit - nakup() už je main"""
    nakup() #pracuje s finalnimi daty - který si vše převezme od předešlých funkcí
    #pracuje s daty objednavky - a s daty faktur
    #volá si data z funkcí - objednavka data, doluj_data_z_faktury(faktury_data)

if __name__ == "__main__":
    main()
