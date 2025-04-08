import streamlit as st
import pandas as pd
import copy
from base_app import maps
from base_app.tables import *
import matplotlib.pyplot as plt


st.set_page_config("Talleres | Recintos", layout="wide", page_icon="🎫")

data = pd.read_csv("venues/data/full_data.csv")

data_es = copy.copy(data)
data_es.columns = ["Nombre recinto","Aforo", "Localidad", "Población", "Techado", "Latitud", "Longitud", "Calidad","Día", "Fecha", "# Día de la semana","Día de la semana", "Fans", "Clima", "Precio (€)", "Disponible"]

fechas = pd.unique(data_es["Día"])
recintos = pd.unique(data_es["Nombre recinto"])

tabs = st.tabs(["Datos de recintos", "Datos localidades", "Datos completos", "Mapa", "Gráficos"])
with tabs[0]:
    recintos = data_es[data_es["Día"]==fechas[0]]
    columns = column_selector(recintos, ["Nombre recinto", "Localidad", "Aforo", "Calidad", "Techado"], key="recintos")
    show_table(recintos, columns)

with tabs[1]:
    localidades = data_es[(data_es["Día"]==fechas[0]) ]
    columns = column_selector(localidades, ["Localidad", "Población", "Fans"], key="localidades")
    show_table(localidades, columns)

with tabs[2]:
    columns = ["Nombre recinto", "Disponible", "Localidad", "Población", "Aforo", "Fans", "Calidad", "Techado", "Clima", "Fecha", "Día de la semana", "Precio (€)"]
    columns = column_selector(data_es,columns, key="full")

    show_table(data_es,  columns)





with tabs[-2]:

    col = st.columns(2)
    with col[0]:
        with st.expander("Configuración de visualización"):
            COL = st.columns(2)
            radius = COL[0].number_input("Radio de los círculos (metros)", min_value=0, value=5000, step=100)
            colormap_options = plt.colormaps()
            index = colormap_options.index("hot")
            colormap = COL[1].selectbox("Mapa de colores", colormap_options,index)

            pass

        max_day = max(data_es['Día'])
        min_date = data_es[data_es['Día']==0]['Fecha'].unique()[0]
        max_date = data_es[data_es['Día']==max_day]['Fecha'].unique()[0]
        date = st.date_input("Selecciona el día a mostrar",min_value=min_date, max_value = max_date)

        COL = st.columns(2)

        color_column = COL[0].selectbox("Variable para colorear", data_es.columns,index=None, placeholder="Escoge una opción")
        columns = COL[1].multiselect("Información a mostrar", data_es.columns, placeholder="Escoge una opción", default="Nombre recinto")
        tips = maps.columns_to_tips(columns)



        
    with col[1]:

        map = maps.create_map()
        # Fullscreen
        import folium
        folium.plugins.Fullscreen(
        position="topleft",
        title="Expand me",
        title_cancel="Exit me",
        force_separate_button=True,
        ).add_to(map)
        if True: 
            circles, colormap = maps.get_circles(data=data_es, tips=tips, color_column = color_column, radius = radius, latitude_column='Latitud', longitude_column='Longitud')
            if colormap:
                colorbar = maps.create_colorbar(colormap,data_es[color_column], caption=color_column,)
                colorbar.add_to(map)
            maps.show_map(map, feature_group_to_add=circles, use_container_width=True, returned_objects=[])








with tabs[-1]:
    col = st.columns(4)
    eje_x = col[0].selectbox("Eje X:", data_es.columns.to_list())
    eje_y = col[1].selectbox("Eje Y:", data_es.columns.to_list())
    orden = col[2].selectbox("Orden:", ["Ascentende", "Descendente"], 1)
    n_elementos = col[3].number_input("Número de elementos:", 5)

    selection = data_es.sort_values([eje_y],ascending=True).head(n_elementos)

    with st.expander("Filtros:"):
        pass

    X = selection[eje_x].to_list()
    Y = selection[eje_y].to_numpy()

    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots(figsize=(16,3))
    ax.bar(range(n_elementos), Y)
    ax.set_xticks(np.arange(n_elementos)-0.5, X, rotation=40)
    ax.grid(True)

    st.pyplot(fig, use_container_width=True)

    pass
