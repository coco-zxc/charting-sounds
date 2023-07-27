# - - - - - - - - - - - - INITIAL IMPORTS - - - - - - - - - - - - -

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import chartingsounds as cs

st.set_page_config(page_title="Charting Sounds",page_icon="🎧",layout="wide")
#- - - - - - - - - - - CSS CODE FOR CUSTOMIZATION - - - - - - - - - - - - 
with open("Scripts/style.html","r") as file:
    page_styling = file.read()

st.markdown(page_styling,unsafe_allow_html=True)
st.markdown("# Charting Sounds")

# - - - - - - - - - - - - - - SIDE BAR: EMBEDDED PLAYER - - - - - - - - - - - - - - -

spotify_id_reference = pd.read_csv("Data/spotify_id_reference_table.csv").set_index("genre_name")

st.sidebar.markdown("""
                    # Welcome to _Charting Sounds_!
                    Explore music genres on the right. Use the player below to listen to the genres you find.
                    """)

spotify_embed_selection = st.sidebar.selectbox("Listen to:",options=spotify_id_reference.index.values)

playlist_id = spotify_id_reference.at[spotify_embed_selection,"spotify_id"]
spotify_embed_html = f'<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/{playlist_id}?utm_source=generator" width="100%" height="440" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'

st.sidebar.write(spotify_embed_html,unsafe_allow_html=True)
st.sidebar.markdown("This project wouldn't be possible if it wasnt for the work done over at [Every Noise at Once](https://everynoise.com)")

#- - - - - - - - - - - INITIAL FILES & VARIABLES - - - - - - - - - - - - - -

@st.cache_data
def load_initial_data():

    relationship_matrix = pd.read_csv("Data/relationship_matrix_3000_genres.csv").set_index('0')
    genres_by_popularity = relationship_matrix.index.values
    relationship_matrix.replace(np.nan,0,inplace=True)
    relationship_matrix = relationship_matrix.transpose()+relationship_matrix
    relationship_matrix = relationship_matrix[genres_by_popularity].loc[genres_by_popularity]


    return pd.DataFrame(relationship_matrix)

relationship_matrix = load_initial_data()

col1,col2 = st.columns(2)
col2.markdown("<p><br>Click and drag to move the map/nodes around, scroll to zoom in or out</p>",unsafe_allow_html=True)

map_type = col1.selectbox("Select a Map to explore:",options=["Default Map","Custom Map","Path Finder"])

match map_type:
    case "Default Map":

        number_of_genres = st.slider("Genres to include (by popularity)",10,3000,value=100,step=10)
        relationship_matrix = relationship_matrix.iloc[0:number_of_genres,0:number_of_genres]
        cache_identifier = str(number_of_genres)

        st.write("Large map! Please be Patient while it loads") if number_of_genres > 1000 else None


    case "Custom Map":

        col1, col2, col3 = st.columns(3)

        selected_genres = col1.multiselect(label="Select Genres",options = relationship_matrix.index.values)
        degrees_of_separation = col2.slider("Degrees of Separation",0,6,0)
        cache_identifier = str(selected_genres) + str(degrees_of_separation)
    
    case "Path Finder":
        u1,col1,u2,col2,u3= st.columns([1,2,2,2,1])
        genre1 = col1.selectbox(label="Source",options=relationship_matrix.index.values)
        genre2 = col2.selectbox(label="Destination",options=relationship_matrix.index.values)
        cache_identifier = genre1+genre2




# - - - - - - - - - - - - - GENERATE GRAPH - - - - - - - - - - - - - 

graph = cs.generate_network(relationship_matrix,100)

# - - - - - - - - - LOGIC FOR WHICH MAP TO DISPLAY + REST OF STREAMLIT APP - - - - - - - - - 

@st.cache_data(ttl=600)
def generate_html_map(map_type:str,cache_identifier):
    match map_type:
        case "Default Map":
            map_html = cs.default_map(relationship_matrix,graph)
        case "Custom Map":
            map_html = cs.rooted_map(graph,relationship_matrix,selected_genres,degrees_of_separation,50)
        case "Path Finder":
            map_html = cs.path_finder_map(graph,genre1,genre2)
    return map_html


map_html = generate_html_map(map_type,cache_identifier)
components.html(map_html,height = 480)