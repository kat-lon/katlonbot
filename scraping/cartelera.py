import requests
from bs4 import BeautifulSoup

def scrapping_periodico():
    url = 'https://www.cristalcines.com'
    paxina = requests.get(url)
    soup = BeautifulSoup(paxina.content, 'html.parser')

    cartelera = soup.find("div", class_="hoyslider")
    peliculas = cartelera.find_all("a")
    return [{"titulo": pelicula.find("h3").contents[0], 
             "enlace": url + pelicula.get("href"),
             "imagen": pelicula.find("img").get("src")}
            for pelicula in peliculas]