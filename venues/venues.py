# Generate venue data
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(123)

"""
Variables
    Categóricas
- disponible: Indica si el recinto está disponible
- techado: Indica si el recinto está techado

    Nominales
- recintos: Nombre de los recintos disponibles
- localidad: Nombre de las localidades donde están los recintos
- clima: Indica el clima esperado para ese momento y lugar
- calidad

"""


# Escala temporal: Dos meses
# Escala espacial: España

venue_names = ["Rosaleda", "Plaza de Toros", "Bernabeu", "Planta baja", "Tertulia", "Palacio de Congresos", "Lemon Rock"]
venue_loc = ["Málaga", "Granada", "Madrid", "Granada", "Granada", "Granada"]

variables_nom = {
    "recinto": list(set(venue_names)),
    "localidad": list(set(venue_loc)),
    "fecha": 'a',
    "clima": {"despejado", "nublado", "lluvia", "granizo", "tormenta"},
    "calidad": {"muy mala", "mala", "regular", "buena", "muy buena"},
    "accesibilidad": {"dfícil", "moderada", "fácil"},
}

variables_cat = ["disponible", "techado"]
variables_num = ["coste_alquiler", "coste_desplazamiento", "capacidad",]


now = datetime.now()
first_day = now.date() + timedelta(days = 10)

n_days = 60
days = []
for day in range(n_days):
    days.append((first_day + timedelta(day)).strftime("%d-%m-%Y,"))

print(days)



variable_names = []
for variable_type in [variables_nom, variables_cat, variables_num]:
    for item in variable_type:
        variable_names.append(item)






df = pd.DataFrame(columns=variable_names)
print(df)












# Escala 1: Anual
"""
Variable tiempo: Mes
"""


# Espacio: Distintas ubicaciones posibles
# variable: venues
# Tiempo: Distintas fechas posibles
# variable: day

"Generación de datos espaciales"




