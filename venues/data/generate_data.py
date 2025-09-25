import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def generate_data(data, **kwargs):

    if "n_days" in kwargs:
        n_days = kwargs['n_days']
        kwargs.pop('n_days')
    if "popularity" in kwargs: popularity = kwargs['popularity']
    # data = remove_empty(data)
    # Remove empty rows
    print(f"Removing rows with empty values...")
    data.dropna(inplace=True)
    print(f"Removing venues with ''0'' capacity...")
    data.dropna(inplace=True)
    data = data.drop(data[data['capacity']==0].index)
    # Generate fans per town and day
    print(f"Generating fans data...")
    data = generate_fans_static(data, popularity=0.01, **kwargs)
    # Add reviews
    print(f"Adding reviews to the venue data...")
    data = generate_reviews(data, **kwargs)

    # Add time dimension to the data
    print(f"Adding time component to the data...")
    data = unfold_time(data, n_days, **kwargs)
    # Generate fans per town and day
    # print(f"Generating fans data...")
    # data = generate_fans(data, popularity=0.01, **kwargs)
    # Generate weather per town and day
    print(f"Generating weather data...")
    data = generate_weather(data, **kwargs)
    # Generate the cost of each venue each day
    print(f"Generating cost data...")
    data = generate_cost(data, **kwargs)
    # Generate the availability of each venue each day
    print(f"Generating availability data...")
    data = generate_availability(data, **kwargs)

    return data

"""
Add the time dimension to the dataset
"""
def unfold_time(data, n_days, day_margin=30):
    today = datetime.now().date() + timedelta(days=30)
    start_day = today + timedelta(days=day_margin)
    weekday = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes","Sábado","Domingo"]
    rows = [] 

    for _, row in data.iterrows(): 
        for day in range(n_days):
            new_row = row.copy() 
            new_row['day'] = day
            new_row['date'] = (start_day + timedelta(days=day))
            new_row['weekday'] = int(new_row['date'].weekday())
            new_row['weekday_name'] = weekday[int(new_row['date'].weekday())]
            rows.append(new_row)

    new_data = pd.DataFrame(rows) 
    return new_data

"""
Generate the number of fans that each town has each day
"""
def generate_fans(data, popularity=0.25, var=0.1):
    """
    Genera el número de fans para cada ciudad y día, asegurando que 
    la población correcta se aplique a cada ciudad.
    """
    days = data['day'].unique()
    towns = data['town'].unique()
    
    population_dict = data[data['day'] == 0].groupby('town')['population'].first().to_dict()
    
    N = len(towns)
    M = len(days)
    
    fans = np.zeros((N, M), dtype=int)
    
    for i, town in enumerate(towns):
        population = population_dict[town]
        fans[i, 0] = np.clip(int(population * popularity * np.random.rand()), 0, population)
    
    for i in range(1, M):
        for j in range(N):
            population = population_dict[towns[j]]
            fans[j, i] = np.clip(int(fans[j, i - 1] * np.random.uniform(1 - var, 1 + var)), 0, population)
    
    fans_dict = {}
    for i, town in enumerate(towns):
        for j, day in enumerate(days):
            fans_dict[(town, day)] = fans[i, j]
    
    data['fans'] = data.apply(lambda row: fans_dict[(row['town'], row['day'])], axis=1)
    
    return data
"""
Generate the number of fans that each town has 
"""
def generate_fans_static(data, popularity=0.25):
    """
    Genera un número estático de fans para cada ciudad,
    basado en su población y una tasa de popularidad.
    """
    towns = data['town'].unique()
    population_dict = data.set_index('town')['population'].to_dict()
    fans_dict = {}

    for town in towns:
        population = population_dict[town]
        # Genera un número de fans basado en la población y popularidad
        if town == "Granada":
            num_fans = np.clip(int(population * popularity * 10 * np.random.rand()), 0, population) # En granada son muy populares
        else:
            num_fans = np.clip(int(population * popularity * np.random.rand()), 0, population)
        fans_dict[town] = num_fans

    # Asigna el mismo número de fans a cada aparición de la ciudad en el DataFrame
    data['fans'] = data['town'].map(fans_dict)

    return data

"""
Generate the weather forecast on each town each day
"""
def generate_weather(data):
    options = ["clear", "cloudy", "light rain", "rain", "heavy rain"]
    options = ["despejado", "nublado", "lluvia suave", "lluvia", "lluvia fuerte"]

    days = data['day'].unique()
    towns = data['town'].unique()

    # First values
    N = len(towns)
    M = len(days)
    weather = np.zeros((N, M), dtype=int)
    weather[:, 0] = np.random.randint(0,len(options)-1, N)
    # Following values
    # Next values
    for i in range(1, M):
        step = np.random.randint(0,3) -1

        weather[:, i] = np.clip((weather[:, i - 1] + step).astype(int),0, len(options)-1)

    # Fill new dataframe
    weather_dict = {}
    for i, town in enumerate(towns):
        for j, day in enumerate(days):
            weather_dict[(town, day)] = options[weather[i, j]]

    data['weather'] = data.apply(lambda row: weather_dict[(row['town'], row['day'])], axis=1)
    return data


def generate_cost(data, var = 0.1):
    weekday_factors = np.array([1,2,2,2.5,3,3.5,3])/1
    
    cost = np.zeros(len(data), dtype=float)
    cost = round(\
            (data['capacity']/ data['capacity'].abs().max()     * 2000 * np.random.uniform(1-var, 1+var)+\
            data['population']/ data['population'].abs().max() *  10000 * np.random.uniform(1-var, 1+var)+\
            data['reviews']/ data['reviews'].abs().max() *  500 * np.random.uniform(1-var, 1+var)+\
            data['roofed'] * 2500 * np.random.uniform(1-var, 1+var))*\
            data.apply(lambda row: weekday_factors[row['weekday']], axis=1)\
                 * 1* np.random.uniform(1-var, 1+var)
            , -1)


    data['cost'] = cost
    return data


def generate_availability(data, var = 0.3):
    weekday_factors = [0.95,0.85,0.8,0.6,0.5,0.45,0.4]
    roofed_factors = [0.55, 0.35]

    max_cost = max(data['cost'])
    max_population = max(data['population'])

    avilability = np.zeros(len(data), dtype=bool)

    avilability = (0\
                    +1-(data['population'].values/max_population)**(1/8) * np.random.uniform(1-var, 1+var)\
                    +data.apply(lambda row: weekday_factors[row['weekday']], axis=1)*.5 * np.random.uniform(1-var, 1+var)\
                    )+.5
    
    data['availability'] = avilability.astype(int).astype(bool)
    return data

def generate_reviews(data, center=3.0, var = 0.55):
    N = len(data)
    reviews = np.random.normal(center, var, N).round(1)
    data["reviews"] = reviews
    return data


if __name__ == '__main__':
    np.random.seed(123)

    data = pd.read_csv('./venues/data/data_fused.csv')

    data = generate_data(data, n_days = 20)
    test = (data['fans'] <= data['population']).all()
    print(test)

    data.to_csv('./venues/data/full_data.csv', index=False)
