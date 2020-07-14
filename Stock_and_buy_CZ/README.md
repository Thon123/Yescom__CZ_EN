# Stock_and_Buy_info

## Základní info
<p>Provede kompletní objednávku od dodavatele dle potřeby skladu. V následujícícm postupu:</br>
1 - uživatel zadá počet a jména faktur zboží, která jsou na cestě<br>
2 - skript již dále propočítá data pro objednávku ze skladu x fatkury a objedná zboží<br>
3 - finální dokončení objednávky je již na uživateli<br></p>

## Skript je převeden na .exe pomocí pyinstalleru
<p>Je třeba dát pozor, že skript používá tabulu pro získávání dat z .pdf a tabula sama o sobě<br>
vyžaduje JAVU, tzn. v pyinstalleru je nutné dodat cestu na dependencies.jar viz. ukázka:<br>
pyinstaller --onefile --add-binary "C:\Users\thon\AppData\Local\Temp\_MEI46602\<br>
tabula\tabula-1.0.3-jar-with-dependencies.jar;./tabula/" naskladni_fakturu.py</p>

## Obsahuje tři soubory
A) credentials - slouží pro connection s Google Sheets pro získání dat </br>
B) settings - obsahuje základní údaje </br>
C) naskladni_a_nakoupi.py - skript řešící veškerý proces </br>

## Naskladni_a_nakoupi.py
<p>Celý proces je poměrně jednoduchý, operuje s dvojími daty a to:<br>
 A) Data ze skladu - funkce [DATA K OBJEDNÁVCE] - napojí se a získá CO JE TŘEBA OBJEDNAT</br>
 B) Data z faktur - neboli zboží na cestě - přečte si faktury a získá znich data</br></p>
<p>Výsledná objednávka je získaná ze vztahu DATA K OBJEDNÁVCE - ZBOŽÍ NA CESTĚ postup je tedy:</br>
- fce data k objednávce => získá data z gsheets</br>
- fce seznam faktur => získá od uživatele faktury, disponující zbožím na cestě</br>
- fce data z faktury => vydoluje seznam produktů z faktur</br>
- fce finální data => provede průnik dat a získá tak finální objednávku</br>
- fce nakoupení => nakoupí pomocí selenia (b2b dod. má pouze online stránky)</br>
<strong>Uživatel již finálně pouze ukončí objednávku, po kontrole zda je vše Ok.</br>

