import requests
from bs4 import BeautifulSoup
import warnings
from geopy.geocoders import Nominatim
import os
import csv


def scrap_locations(url = "https://es.wikipedia.org/wiki/Anexo:Municipios_de_Espa%C3%B1a_por_poblaci%C3%B3n"):

    return

# wikitable sortable jquery-tablesorter

if __name__ == "__main__":

    url = "https://es.wikipedia.org/wiki/Anexo:Municipios_de_Espa%C3%B1a_por_poblaci%C3%B3n"
    response = requests.get(url) 
    soup = BeautifulSoup(response.content, "html.parser")
    # Encuentra la tabla que contiene los datos

    filas = soup.find_all('tr', lambda tag: tag.find('td', text=re.compile(r'\d+')))

    print(filas)