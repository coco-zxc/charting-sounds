import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import gravis as gv
from colour import Color

spotify_id_reference = pd.read_csv("Data/spotify_id_reference_table.csv").set_index("genre_name")

st.sidebar.markdown("""
                    # Welcome to _Charting Sounds_!
                    Explore music genres on the right. Use the player below to listen to the genres you find.
                    """)

spotify_embed_selection = st.sidebar.selectbox("Listen to:",options=spotify_id_reference.index.values)


playlist_id = spotify_id_reference.at[spotify_embed_selection,"spotify_id"]
spotify_embed_html = f'<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/{playlist_id}?utm_source=generator" width="100%" height="440" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'
st.sidebar.write(spotify_embed_html,unsafe_allow_html=True)
st.sidebar.markdown("""
                    This project wouldn't be possible if it wasnt for the work done over at [Every Noise at Once](https://everynoise.com)
                    """)

#- - - - - - - - - - - CSS CODE FOR CUSTOMIZATION - - - - - - - - - - - - 
page_bg_image = f"""
<style>
[data-testid="stAppViewContainer"]{{
background-image: url("https://raw.githubusercontent.com/coco-zxc/charting-sounds/main/Images/background.png");
}}

[data-testid="stHeader"]{{
background-color:rgba(0,0,0,0);
}}
[data-testid="stSidebar"]{{
background-color: rgba(52, 73, 94,100);
}}

.block-container {{
                    padding-top: 1rem;
                }}
.css-1544g2n.e1akgbir4{{
                    margin-top: -90px;
}}

</style>
"""

st.markdown(page_bg_image,unsafe_allow_html=True)
st.markdown("# Charting Sounds")


#- - - - - - - - - - - INITIAL FILES & VARIABLES - - - - - - - - - - - - - -

@st.cache_data
def load_initial_data():

    relationship_matrix = pd.read_csv("Data/relationship_matrix.csv").set_index('0')
    relationship_matrix.replace(np.nan,0,inplace=True)
    relationship_matrix = relationship_matrix + relationship_matrix.transpose()

    return relationship_matrix

relationship_matrix = load_initial_data()

st.write("Click and drag to move the map/nodes around, scroll to zoom in or out")
custom_map_selected = st.checkbox("Custom Map")
distance_threshold = 100

if custom_map_selected:
    root_selector, degrees_of_separation_slider, custom_color = st.columns(3)
    selected_genres = root_selector.multiselect(label="Select Genres", options = relationship_matrix.index.values)
    degrees_of_separation = degrees_of_separation_slider.slider("Degrees of Separation",0,6,0)
    cache_identifier = str(selected_genres) + str(degrees_of_separation)
else:
    number_of_genres = st.slider("Genres to include (by popularity)",10,500,value=100,step=10,key="main_slider")
    relationship_matrix = relationship_matrix.iloc[0:number_of_genres,0:number_of_genres]
    cache_identifier = str(number_of_genres)

# - - - - - - - - - - - GENERATE NETWORK - - - - - - - - - - - - - -
@st.cache_data(ttl=600)
def generate_network(cache_identifier):
    G = nx.Graph()

    # Adds all nodes to Network
    for genre in relationship_matrix.index.values:
        G.add_node(genre)

    # Adds all edges to Network
    for genre in relationship_matrix.index.values:

        close_genres_filter = relationship_matrix.loc[:,genre] < distance_threshold
        close_genres = pd.Series(relationship_matrix.loc[:,genre][close_genres_filter])
        close_genres = close_genres.sort_values().index
        close_genres = close_genres.drop(genre)
        
        for close_genre in close_genres:
            G.add_edge(genre,close_genre)

    return G

G = generate_network(cache_identifier)
# - - - - - - - - - - - - - FUNCTIONS FOR MY SANITY - - - - - - - - -

def color_calculator(graph,origin_genre,target_genres):

    while len(target_genres) < 3:
        target_genres.append("")

    
    rgb = []
    node_color = Color()
    scalar = 20

    for target_genre in target_genres:
        if (target_genre in graph.nodes) and nx.has_path(graph,origin_genre,target_genre):
            distance = (255 - np.clip(nx.shortest_path_length(graph,origin_genre,target_genre) * scalar,16,240)) / 255
        else:
            distance = 0.25
        rgb.append(distance)
    
    node_color.set_blue(rgb[0])
    node_color.set_red(rgb[1])
    node_color.set_green(rgb[2])

    return node_color.get_hex_l()

@st.cache_data(ttl=600)  
def default_map(cache_identifier):
    # - - - - - - - - - - DEFINE GRAPH METADATA - - - - - - - - - - - - 
    graph_gjgf = gv.convert.networkx_to_gjgf(G)
    graph_gjgf["graph"]["metadata"] = {
        "background_color" : "#151515",
        "node_color" : "#444444",
        "node_label_color" : "white",
        "edge_color" : "gray"
    }


    # DEFINE NODE STYLING

    for genre in relationship_matrix.index.values:

        node_size = len(G.edges([f'{genre}'])) * 4 + 10

        graph_gjgf["graph"]["nodes"][f"{genre}"]["metadata"] = {
            "hover" : genre,
            "color" : color_calculator(G,genre,["latin pop","rock","rap"]),
            "size": node_size,
            "label_size": 100 if genre in ["pop","rock","rap","latin pop"] else np.clip(node_size / 4, 15,100)
            }

    map_object = gv.vis(graph_gjgf,
                        show_details_toggle_button = False,
                        show_menu_toggle_button = False,
                        edge_curvature=0.3,
                        gravitational_constant = -2000,
                        node_hover_neighborhood=True,
                        node_hover_tooltip=True
                        )

    map_html = map_object.to_html()

    return map_html

@st.cache_data(ttl=600)
def rooted_map(cache_identifier):

    roots = list(selected_genres)
    display_genres = roots[:]

    for i in range(0,degrees_of_separation):
        for genre in roots:
            filter = relationship_matrix.loc[:,genre] < distance_threshold
            display_genres.extend(list(relationship_matrix.loc[:,genre][filter].index.values))
        display_genres = pd.Series(display_genres).unique().tolist()
        roots = display_genres[:]
        
    G_copy = G.subgraph(display_genres)

    # DEFINE GRAPH METADATA
    graph_gjgf = gv.convert.networkx_to_gjgf(G_copy)
    graph_gjgf["graph"]["metadata"] = {
        "background_color" : "#151515",
        "node_color" : "#444444",
        "node_label_color" : "white",
        "edge_color" : "white"
    }


    for genre in display_genres:
        node_size = len(G_copy.edges([f'{genre}'])) * 4 + 10
        graph_gjgf["graph"]["nodes"][f"{genre}"]["metadata"] = {
            "hover": genre,
            "color": color_calculator(G_copy,genre,list(selected_genres)),
            "size": node_size,
            "label_size": 30 + len(G_copy.nodes)/2 if genre in list(selected_genres) else np.clip(node_size / 4, 15,100)
        }

    map_object = gv.vis(graph_gjgf,
                        show_details_toggle_button = False,
                        show_menu_toggle_button = False,
                        edge_curvature=0.3,
                        gravitational_constant = -2000,
                        node_hover_neighborhood=True,
                        node_hover_tooltip=True
                        )

    map_html = map_object.to_html()

    return map_html

# - - - - - - - - - LOGIC FOR WHICH MAP TO DISPLAY + REST OF STREAMLIT APP - - - - - - - - - 

if custom_map_selected:
    map_html = rooted_map(cache_identifier)
else:
    map_html = default_map(cache_identifier)

components.html(map_html,height = 480)


st.markdown("""
         ## About this project
Welcome to charting sounds! This app is an experiment to visualize all (or at least a lot!) of musical genres in an interactive map for users to explore and find new music.

While searching for a job in Data Science/Analysis, I decided to develop some projects that may serve as portfolio pieces. I wanted to create a "Map" of some sort where genres seamlessly connected to one another.
  
This is when I came across the work done by Glenn Mcdonald in [Every Noise at Once](https://everynoise.com). He created some "rooted lists" where genres were ranked in order of how "close" they were related to the genre in the No.1 spot.
""")

col1,col2 = st.columns(2)
col1.image("Images/everynoise_example1.gif")
col2.markdown("I loved the tool, but exploring it was a bit of a hassle. I was certain that a visual representation would be much easier to use.")
col2.markdown("Using a network would allow genres to be phisically close and connected to one another. With enough of these genres, a map can be created.")

st.markdown("""
## The Data
I started with some webscraping to store and analyze the lists in Every Noise at Once. The objective was to find a way to evaluate the "closeness" between genres.
I can then create a square grid, with the genres at the columns and rows, and the values as the "closeness" value.
  
The result of this was a Distance Table, the values refer to the distance between each genre. Similar genres have small distances, unrelated genres have larger distances.
Here's the resulting table:

""")

st.dataframe(relationship_matrix)

st.write("With this data, I can create a Graph (Mathematical Network) with the help of some python libraries ([NetworkX](https://networkx.org) and [GraVis](https://robert-haas.github.io/gravis-docs/)). Streamlit was the extremely useful into making this into an interactive experience, as well as some introduction into HTML, JavaScript and CSS.")


st.markdown("""
## Interesting findings
### 1. Pop isn't *that* popular
""")
st.image("Images/pop_is_not_popular.png")
st.markdown("""
While surprising at first, it makes sense that the most "popular" genre is not closely related to many other genres. There are clusters of genres, but pop seems to only be a bridge between them.
It is similar to how "popular" kids have a lot of "friends" but they don't have many *friends*. To be popular, they need to be sufficiently watered down to appeal to a wider audience.
            
An alternative explanation is that the other genres have a much stronger identity than pop. Genres that **sound** like pop are categorized under the "pop" label instead of being given their own name.
""")

st.markdown("""
### 2. Clusters, Ilands, and Gateway Genres
""")
col1,col2,col3 = st.columns(3)
col1.image("Images/cluster1.png")
col2.image("Images/cluster2.png")
col3.image("Images/cluster3.png")

st.markdown("""
There are "clusters" or "islands" of genres. These clumps of genres suggest that these are music types that tend to be listened to together, likely by the same demographics.
Some of these clusters become part of something bigger depending on the number of genres that are included in the graph. When these islands connect to the main map, the genres that connect them are "Gateway" genres to those clusters.
""")

st.markdown("""
### 3. Latin pop, the new "Pop"?

Since the data used here comes from spotify statistics, it may be skewed based on user demographics. This makes more sense when we look at the dominance of latin american music.
Spotify's user base is largely latin american, so genres from latin american may more dominant when compared to the entire music industry.
This is all speculation, I do not have access to spotify's demographic data.
""")
