from bs4 import BeautifulSoup as bs
from selenium import webdriver
import sqlite3
import time
from tabulate import tabulate
import webbrowser

def scrap(URL):
    driver = webdriver.Chrome()
    driver.get(URL)
    r = driver.page_source
    driver.quit()

    base = {}
    price, name, end, link = [],[],[],[]

    soup = bs(r, 'lxml')

    for i in soup.find_all('a', class_=['_w7z6o']):
        name.append(i.text)
        link.append(i.get('href'))
    for i in soup.find_all('span'):
        if i.get('tabindex') == '0' and i.get('aria-label') is not None:
            price.append(i.get('aria-label'))
    for name, price, link in zip(name, price, link):
        base[name] = price,link

    base_sorted = sorted(base.items(), key=lambda x:x[1])
    base = dict(base_sorted)

    for i, (name, data) in enumerate(base.items(), start=1):
        price, link = data
        price = str(price)
        end.append([i, name, price[:-17]])
    headers = ['ID', 'Nazwa', 'Cena']
    print(tabulate(end, headers, tablefmt='grid', numalign="center", stralign="center"))
    print()
    while True:
        choose = int(input('Wybierz ID (0 wychodzisz): '))
        if choose == 0:
            break 
        webbrowser.open(list(base.items())[choose-1][1][1], new=0)
        

if __name__ == '__main__':
    while True:
        print('''Witaj
1. Pelet (15KG)
2. Pelet (Wszystko najtańsze)
3. Benitowy (10-15KG)
    
0. Wyjdź''')
        choose = input('Wybierz żwirek: ')
        match choose:
            case '1':
                scrap('https://allegro.pl/kategoria/ogrzewanie-opal-253377?string=pelet%2015kg&allegro-smart-standard=1&offerTypeBuyNow=1&stan=nowe&rodzaj-opalu=pelet&order=p')
                continue
            case '2':
                scrap('https://allegro.pl/kategoria/ogrzewanie-opal-253377?string=pelet&allegro-smart-standard=1&order=p')
            case '3':
                scrap('https://allegro.pl/kategoria/dla-kotow-zwirki-90051?string=%C5%BCwirek%20bentonitowy&offerTypeBuyNow=1&allegro-smart-standard=1&rodzaj=bentonitowy&waga-od=10&waga-do=15&order=p')
                continue    
            case '0':
                break        
            case _:
                print('Wybierz odpowiednio')
                time.sleep(1)
                continue