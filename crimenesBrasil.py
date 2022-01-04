#data
import pandas as pd
#plotting
import streamlit as st
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import seaborn as sns
#geospatial
import folium
import geopy
#clustering
from sklearn.cluster import KMeans
#---Configuracion
sns.set_theme()
pd.set_option('display.max_columns', 36)
pd.options.mode.chained_assignment = None 

city= "Sao Paulo"
locator=geopy.geocoders.Nominatim(user_agent="MyCoder")
location=locator.geocode(city)
location=[location.latitude,location.longitude]
#---leer data
df=pd.read_csv("https://raw.githubusercontent.com/jhorelrevilla/Clustering-de-crimenes-en-Brasil/main/data/dataset.csv")
#---function
def generate_map(df,num_cluster):
    map_=folium.Map(location=location,tiles="cartodbpositron")
    kmeans=KMeans(num_cluster,random_state=0).fit(df[['latitude','longitude']])
    df['cluster']=kmeans.labels_
    colors = [
        'red',
        'blue',
        'lightblue',
        'orange',
        'beige',
        'green',
        'purple',
        'cadetblue',
        'black',
        'pink'
    ]
    df.apply(
        lambda x:
        folium.CircleMarker(
            location=[x['latitude'],x['longitude']],
            radius=2,
            fill_color=colors[x['cluster']],
            fill=True,
            fill_opacity=1.0,
            color=False
        ).add_to(map_),
        axis=1
    )
    return map_

sidebar = st.sidebar
df_display = sidebar.checkbox("Mostrar datos", value=True)

n_clusters = sidebar.slider(
    "Selecciona el número de clusters",
    min_value=2,
    max_value=10,
)
# -----------------------------------------------------------
# Main
# -----------------------------------------------------------
# Create a title for your app
st.title("Clusterizado K-Means Interactivo")

# A description
st.write("Datos utilizados:")
# Display the dataframe
if df_display:
    st.write(df)

#st.write(generate_map(df,n_clusters))
folium_static(generate_map(df,n_clusters))