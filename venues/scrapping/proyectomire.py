import requests
from bs4 import BeautifulSoup
import warnings
from geopy.geocoders import Nominatim
import os
import csv

def get_venue_name(url):
    response = requests.get(url, verify=False) 
    soup = BeautifulSoup(response.content, "html.parser")
    # Venue name
    name = soup.find(id="centroderechadatostitulo1").text
    # Venue data
    text = soup.find(id="centroderechadatosrecinto").text
    roofed = False
    if text.find("cubierto") >= 0: roofed=True

    return name, roofed

def get_capacity(url):
    response = requests.get(url, verify=False) 
    soup = BeautifulSoup(response.content, "html.parser")
    text = soup.find(id="centroderechadatosrecinto").text.lower()
    id_aforo = text.find("aforo")
    if id_aforo == -1: capacity = 0
    else:

        text = text[id_aforo + len("aforo"):]

        capacity = ""
        for caracter in text:
            if caracter.isdigit():
                capacity += caracter
            elif capacity: 
                break
    return capacity

def get_location(url):
    response = requests.get(url, verify=False) 
    soup = BeautifulSoup(response.content, "html.parser")
    text = soup.find(id="centroderechadatosrecinto").text
    id_start = text.find("Dirección del edificio:")
    id_end = text.find("Teléfono:")
    if id_start==-1: lat=0;lon=0;town=None
    else:
        address = text[id_start + len("Dirección del edificio:"):id_end]
        geolocator = Nominatim(user_agent="my_geocoding_app")
        location = geolocator.geocode(address, addressdetails=True)
        if location is None: town=None; lat=None; lon=None
        else:
            lat = location.latitude
            lon = location.longitude
            town = None
            for loc in ["town", "city", "vilalge", "county"]:
                town = location.raw["address"].get(loc)
                if town is not None: break
    return town, address, lat, lon

def scrap_mire(url):

    warnings.filterwarnings("ignore")
    
    # "Recinto"
    suffix = "&d=0"
    name, roofed = get_venue_name(url+suffix)

    # Capacity
    suffix = "&d=2"
    capacity = get_capacity(url+suffix)

    # Location
    suffix = "&d=1"
    town, address, lat, lon = get_location(url+suffix)


    return {
        "name": name,
        "town": town,
        "address": address,
        "capacity": capacity,
        "roofed": roofed,
        "latitude": lat,
        "longitude": lon,
        "url": url}



if __name__ == "__main__":
    filepath = "./venues/data/venue_data_scrap.csv"
    file_exists = os.path.exists(filepath)
    columns = ["name", "town", "address","capacity", "roofed", "latitude", "longitude", "url"]

    with open(filepath, 'a', newline='', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=columns)

        if not file_exists:
            writer.writeheader()

        for id in range(0, 10000):
            try:
                url = f"https://www.proyectomire.org/web/datosrecinto.php?id={str(id)}"
                data = scrap_mire(url)
                writer.writerow(data)  # Escribimos el diccionario data como una fila
                print(f"Fetched id {id}")
            except Exception as e:
                print(f"id {id} not fetched. Reason: {e}")



