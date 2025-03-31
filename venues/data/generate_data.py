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
    # Add time dimension to the data
    print(f"Adding time component to the data...")
    data = unfold_time(data, n_days, **kwargs)
    # Generate fans per town and day
    print(f"Generating fans data...")
    data = generate_fans(data, **kwargs)
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
    today = datetime.now().date()
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
    weekday_factors = [1,2,2,4,9,10,8]
    
    cost = np.zeros(len(data), dtype=float)
    cost = round(\
            data['capacity']    * 50 * np.random.uniform(1-var, 1+var)+\
            data['population'] *  5 * np.random.uniform(1-var, 1+var)+\
            data['roofed'] * 100 * np.random.uniform(1-var, 1+var)+\
            data.apply(lambda row: weekday_factors[row['weekday']], axis=1)\
                 * 100 * np.random.uniform(1-var, 1+var)
            , -1)


    data['cost'] = cost
    return data


def generate_availability(data, var = 0.1):
    weekday_factors = [0.9,0.8,0.8,0.6,0.2,0.1,0.15]
    roofed_factors = [0.55, 0.35]

    max_cost = max(data['cost'])
    max_population = max(data['population'])

    avilability = np.zeros(len(data), dtype=bool)
    avilability = (1\
            *data['cost'].values/max_cost * 1.* np.random.uniform(1-var, 1+var)\
            *1/(data['population'].values/max_population*1)* np.random.uniform(1-var, 1+var)\
            *data.apply(lambda row: roofed_factors[row['roofed']], axis=1)*\
                1 * np.random.uniform(1-var, 1+var)\
            *data.apply(lambda row: weekday_factors[row['weekday']], axis=1)*\
                1 * np.random.uniform(1-var, 1+var)\
            )**(1/4) +.5
    
    data['availability'] = avilability.astype(int).astype(bool)
    return data



if __name__ == '__main__':
    np.random.seed(123)

    data = pd.read_csv('./venues/data/data_fused.csv')

    data = generate_data(data, n_days = 3)
    test = (data['fans'] <= data['population']).all()
    print(test)

    data.to_csv('./venues/data/full_data.csv', index=False)
