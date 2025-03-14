import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium


st.set_page_config(layout="wide")

venues = pd.read_csv("venues/data/venue_data_scrap.csv")
venues.columns = ["Nombre recinto", "Localidad", "Aforo", "Techado", "Latitud", "Longitud", "URL"]

localidades = pd.read_csv("venues/data/town_data_scrap.csv")
localidades.columns = ["Localidad", "Población" ]

fused = pd.read_csv("venues/data/data_fused.csv")
fused.columns = ["Nombre recinto","Aforo", "Localidad", "Población", "Techado", "Latitud", "Longitud"]



tabs = st.tabs(["Datos de recintos", "Datos localidades", "Datos fusionados", "Mapa"])
with tabs[0]:
    st.dataframe(venues)

with tabs[1]:
    st.dataframe(localidades)

with tabs[2]:
    st.dataframe(fused)

with tabs[3]:
    folium_map = folium.Map(location=[40.453513844033566, -3.6898475724292292],
                            zoom_start=6,  tiles="CartoDB positron")
    st_folium(folium_map, use_container_width=True)



