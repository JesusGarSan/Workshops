import streamlit as st
import pandas as pd
import copy
from base_app import maps
from base_app.tables import *
import matplotlib.pyplot as plt


st.set_page_config("Talleres | Recintos", layout="wide", page_icon="🎫")

data = pd.read_csv("venues/data/full_data.csv")
data["date"] = pd.to_datetime(data['date'], format='%Y-%m-%d').dt.date

# Usemos el nombre en español de las variables
data.columns = ["Nombre recinto","Aforo", "Localidad", "Población", "Techado", "Latitud", "Longitud", "Fans", "Calidad","Día", "Fecha", "# Día de la semana","Día de la semana", "Clima", "Precio", "Disponible"]

data = copy.copy(data)

fechas = pd.unique(data["Día"])
recintos = pd.unique(data["Nombre recinto"])

tabs = st.tabs(["Datos de recintos", "Datos localidades", "Datos completos", "Mapa"])
text = {"title": "Columnas a mostrar", "placeholder": "Selecciona una opción"}
with tabs[0]: # Datos recintos
    recintos = data[data["Día"]==fechas[0]]
    recintos.reset_index(inplace=True)
    columns = ["Nombre recinto", "Localidad", "Aforo", "Calidad", "Techado"]
    selected_columns = column_selector(recintos, columns, key="recintos",
                              text=text)
    
    with st.expander("Ordenar"):
        recintos = sort_dataframe(recintos, columns, sorting_directions=["Ascendente", "Descendiente"],
                            text={"title":"Ordenar según:",
                                    "direction":"Sentido de:",
                                    "placeholder":"Elige las columnas según las que ordenar"}, key="recintos")
    show_table(recintos, selected_columns)

with tabs[1]: # Datos localidades
    localidades = data[(data["Día"]==fechas[0])].drop_duplicates(subset="Localidad")
    localidades.reset_index(inplace=True)
    columns = ["Localidad", "Población", "Fans"]
    selected_columns = column_selector(localidades, columns, key="localidades",
                              text=text)
    
    with st.expander("Ordenar"):
        localidades = sort_dataframe(localidades, columns, sorting_directions=["Ascendente", "Descendiente"],
                            text={"title":"Ordenar según:",
                                    "direction":"Sentido de:",
                                    "placeholder":"Elige las columnas según las que ordenar"}, key="localidades")
    show_table(localidades, selected_columns)

with tabs[2]: # Datos espacio temporales completos
    columns = ["Nombre recinto", "Localidad", "Población", "Aforo", "Fans", "Calidad", "Techado", "Clima", "Fecha", "Día de la semana", "Precio", "Disponible"]
    selected_columns = column_selector(data,columns, key="full",
                              text=text)

    with st.expander("Ordenar"):
        data = sort_dataframe(data, columns,sorting_directions=["Ascendente", "Descendiente"],
                            text={"title":"Ordenar según:",
                                    "direction":"Sentido de:",
                                    "placeholder":"Elige las columnas según las que ordenar"}, key="full")

    show_table(data,  selected_columns,
               column_config={ "Precio": st.column_config.NumberColumn( "Precio",  format="%.0f €")})





with tabs[-1]:

    col = st.columns(2)
    with col[0]:
        with st.expander("Configuración de visualización"):
            COL = st.columns(2)
            radius = COL[0].number_input("Radio de los círculos (metros)", min_value=0, value=5000, step=100)
            colormap_options = plt.colormaps()
            index = colormap_options.index("hot")
            colormap = COL[1].selectbox("Mapa de colores", colormap_options,index)

        max_day = max(data['Día'])
        min_date = data[data['Día']==0]['Fecha'].unique()[0]
        max_date = data[data['Día']==max_day]['Fecha'].unique()[0]
        date = st.date_input("Selecciona el día a mostrar",min_value=min_date, max_value = max_date)
        data_filtered = data[data["Fecha"]==date]

        COL = st.columns(2)

        options = ["Nombre recinto", "Disponible", "Localidad", "Población", "Aforo", "Fans", "Calidad", "Techado", "Clima", "Fecha", "Día de la semana", "Precio"]
        color_column = COL[0].selectbox("Variable para colorear", options,index=None, placeholder="Escoge una opción")
        columns = COL[1].multiselect("Información a mostrar", data.columns, placeholder="Escoge una opción", default="Nombre recinto")
        tips = maps.columns_to_tips(columns)

        # filter = st.checkbox("Filtrar datos")
        # if filter:
        #     text={"title":"Variable a filtrar",
        #         "values": "Valores de ",
        #         "placeholder": "Elige una opción",
        #         "regex": "Substring o regex en "}
        #     data_filtered = filter_dataframe(data, text)
        #     data_filtered["Fecha"] = pd.to_datetime(data['Fecha'], format='%Y-%m-%d').dt.date


        
    with col[1]:

        map = maps.create_map()
        map = maps.add_fullscreen_button(map)
        circles, colormap = maps.get_circles(data=data_filtered, tips=tips, color_column = color_column, radius = radius, latitude_column='Latitud', longitude_column='Longitud')
        if colormap:
            colorbar = maps.create_colorbar(colormap,data_filtered[color_column], caption=color_column,)
            colorbar.add_to(map)
        maps.show_map(map, feature_group_to_add=circles, use_container_width=True, returned_objects=[])





