import requests
from bs4 import BeautifulSoup
import re

def get_gmaps_score(item, url="https://www.google.com/maps/search/"):

    url = f"{url}{item}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        soup = BeautifulSoup(response.content, "html.parser")
        print(soup)
        score = soup.find("span", class_="cards-rating")
        if score:
            score_text = score.text
            score_num = re.findall(r"\d+\.\d+", score_text)
            if score_num:
                return score_num[0]
        return None  
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

if __name__ == "__main__":
    cadena_busqueda = "Auditori Alfons Vallhonrat(Centre Cultural Caixa de Terrassa) de Tarrasa/Terrassa"
    puntuacion = get_gmaps_score(cadena_busqueda)
    if puntuacion:
        print(f"La puntuación del primer resultado es: {puntuacion}")
    else:
        print("No se encontró la puntuación.")