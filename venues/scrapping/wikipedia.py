import requests
from bs4 import BeautifulSoup
import warnings
from geopy.geocoders import Nominatim
import os
import csv


def scrap_locations(url = "https://es.wikipedia.org/wiki/Anexo:Municipios_de_Espa%C3%B1a_por_poblaci%C3%B3n"):

    response = requests.get(url) 
    soup = BeautifulSoup(response.content, "html.parser")

    tables = soup.find_all('table')

    data = {"town":[], "population":[]}

    for table in tables:
        rows = table.find_all('tr')
        for row in rows[1:]:
            town = (row.text).split("\n")[3]
            population = int((row.text).split("\n")[5].replace(" ", ""))

            data["town"].append(town)
            data["population"].append(population)

            
    return data

# wikitable sortable jquery-tablesorter

if __name__ == "__main__":


    data = scrap_locations()

    import pandas as pd
    df = pd.DataFrame(data)
    df.to_csv("./venues/data/town_data_scrap.csv", index=False)