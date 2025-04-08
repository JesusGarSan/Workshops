import pandas as pd
from unidecode import unidecode

def normalize_town(town_name):
    if isinstance(town_name, str): # Verify that the element is a string.
        town_name = town_name.lower()
        town_name = unidecode(town_name)
        # town_name = town_name.replace("/"," ")
        town_name = town_name.replace("-"," ")
        town_name = town_name.replace("  "," ")
        town_name = town_name.replace("   "," ")
        return town_name
    else: return ""


venues = pd.read_csv("./venues/data/venue_data_scrap.csv")
venues.dropna(inplace=True)
venues["capacity"] = venues["capacity"].astype(int)

towns = pd.read_csv("./venues/data/town_data_scrap.csv")
towns.dropna(inplace=True)

venues['town_unidecode'] = venues['town'].apply(normalize_town)
towns['town_unidecode'] = towns['town'].apply(normalize_town)

cols = venues.columns.to_list()
cols.remove("url")
cols.insert(3,'population')
cols[1], cols[2] = cols[2], cols[1]
data = pd.DataFrame([], columns=cols)

for row in venues.iloc():

    town = row['town_unidecode']
    population = towns[towns['town_unidecode'] == town]['population'].to_list()
    if len(population) == 1:
        new_row = row.to_dict()
        new_row['population']=population[0]
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
    else: 
        pass
        # print(f'Unable to fuse "{town}"')


data.drop('town_unidecode', axis=1, inplace=True)
data.drop('url', axis=1, inplace=True)
data.dropna(inplace=True)

data.to_csv("./venues/data/data_fused.csv", index=False)
