import streamlit as st
import pandas as pd
# import folium
import copy
# from streamlit_folium import st_folium
# from maps import *
# from tables import *
from base_app import maps
from base_app.tables import *




st.set_page_config("Talleres | Recintos", layout="wide", page_icon="🎫")

venues = pd.read_csv("venues/data/venue_data_scrap.csv")
venues.columns = ["Nombre recinto", "Localidad", "Aforo", "Techado", "Latitud", "Longitud", "URL"]

localidades = pd.read_csv("venues/data/town_data_scrap.csv")
localidades.columns = ["Localidad", "Población" ]

fused = pd.read_csv("venues/data/data_fused.csv")
full = pd.read_csv("venues/data/full_data.csv")
full_es = copy.copy(full)
full_es.columns = ["Nombre recinto","Aforo", "Localidad", "Población", "Techado", "Latitud", "Longitud","Día", "Fecha", "# Día de la semana","Día de la semana", "Fans", "clima", "Precio", "Disponible"]
# fused.columns = ["Nombre recinto","Aforo", "Localidad", "Población", "Techado", "Latitud", "Longitud"]



tabs = st.tabs(["Datos de recintos", "Datos localidades", "Datos completos", "Mapa"])
with tabs[0]:
    columns = column_selector(venues)
    show_table(venues, columns)

with tabs[1]:
    columns = column_selector(localidades)
    show_table(localidades, columns)

with tabs[2]:
    full = filter_dataframe(full)
    columns = column_selector(full, ["Nombre recinto","Aforo", "Localidad", "Población", "Techado", "Fecha","Día de la semana", "Fans", "clima", "Precio", "Disponible"])

    show_table(full_es,  columns)

with tabs[-1]:

    col = st.columns(2)
    with col[0]:
        with st.expander(''):
            time = st.checkbox("Representar información temporal")

        if time:
            max_day = max(full['day'])
            min_date = full[full['day']==0]['date'].unique()[0]
            max_date = full[full['day']==max_day]['date'].unique()[0]
            date = st.date_input("Selecciona el día a mostrar",min_value=min_date, max_value = max_date)
            full['date'] = full['date'].dt.date

            display_circles, radius, color_column, tips, colormap = maps.circle_config_form(full, True, 5000)
            # color_column = st.selectbox("Color", full.columns)
        
    with col[1]:
        if not time:
            tips = {
                "Nombre": 'name',
                "Aforo": 'capacity',
                "Techado": 'roofed',
            }
            map = maps.create_map()
            circles, colormap = maps.get_circles(data=full, tips=tips, radius = 2000)
            maps.show_map(map, feature_group_to_add=circles, use_container_width=True, returned_objects=[])

        if time:
            tips = {
                "Nombre": 'name',
                "Aforo": 'capacity',
                "Localidad": "town",
                "Habitantes": color_column,
                "Clima": 'weather',
                "Precio": 'cost',
                "Fans": 'fans',
                "Techado": 'roofed',
                "Disponibilidad": 'availability',
            }
            map = maps.create_map()
            circles, colormap = maps.get_circles(data=full, tips=tips, color_column = color_column, radius = radius)
            colorbar = maps.create_colorbar(colormap,full[color_column], caption=color_column,)
            colorbar.add_to(map)
            maps.show_map(map, feature_group_to_add=circles, use_container_width=True, returned_objects=[])



