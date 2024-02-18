import requests
from bs4 import BeautifulSoup

def scrapping_periodico():
    url = 'https://www.elprogreso.es'
    paxina = requests.get(url)
    soup = BeautifulSoup(paxina.content, 'html.parser')

    portada = soup.find("div", class_="wrapper-tree-columns first-wrapper aperture-wrapper")
    articulos_portada = portada.find_all("h2", class_="title")
    return [{"titular":articulo.find("a").contents[0], 
             "enlace":url + articulo.find("a").get("href")}
             for articulo in articulos_portada]
