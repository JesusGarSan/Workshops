import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium


st.set_page_config(layout="wide")

df = pd.read_csv("venues/data/venue_data_scrap.csv")
df.columns = ["Nombre recinto", "Localidad", "Aforo", "Techado", "Latitud", "Longitud", "URL"]



tabs = st.tabs(["Datos de recintos", "Mapa"])
with tabs[0]:
    st.dataframe(df)

with tabs[1]:
    folium_map = folium.Map(location=[40.453513844033566, -3.6898475724292292],
                            zoom_start=6,  tiles="CartoDB positron")
    st_folium(folium_map, use_container_width=True)



