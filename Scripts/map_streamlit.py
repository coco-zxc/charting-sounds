import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import gravis as gv
#- - - - - - - - - - - CSS CODE FOR CUSTOMIZATION - - - - - - - - - - - - 
page_bg_image = f"""
<style>
[data-testid="stAppViewContainer"]{{
background-image: url("https://raw.githubusercontent.com/coco-zxc/charting-sounds/main/Images/background.png");
}}

[data-testid="stHeader"]{{
background-color:rgba(34,34,34,100);
}}

</style>
"""

st.markdown(page_bg_image,unsafe_allow_html=True)
st.markdown("""
# Charting Sounds
_by [George García](https://www.linkedin.com/in/jl-gg/)_
""")
#- - - - - - - - - - - INITIAL FILES & VARIABLES - - - - - - - - - - - - - -

relationship_matrix = pd.read_csv("Data/relationship_matrix.csv").set_index('0')
relationship_matrix.replace(np.nan,0,inplace=True)
relationship_matrix = relationship_matrix + relationship_matrix.transpose()

number_of_genres = st.slider("Number of Genres to display",10,500,value=250,step=10,key="main_slider")
relationship_matrix = relationship_matrix.iloc[0:number_of_genres,0:number_of_genres]
distance_threshold = 100

st.write("Choose what genres to see: ")
col1, col2 , col3 = st.columns(3)
selected_genres = col1.multiselect(label="Select genre(s)",options = relationship_matrix.index.values)
levels = col2.slider("Degrees of Separation",0,10,1)
node_color = col3.color_picker("Select your color",value = "#48C9B0")

# - - - - - - - - - - - GENERATE NETWORK - - - - - - - - - - - - - -
G = nx.Graph()
for genre in relationship_matrix.index.values:
    G.add_node(genre)

for genre in relationship_matrix.index.values:

    close_genres_filter = relationship_matrix.loc[:,genre] < distance_threshold
    close_genres = pd.Series(relationship_matrix.loc[:,genre][close_genres_filter])
    close_genres = close_genres.sort_values().index
    close_genres = close_genres.drop(genre)
    
    for close_genre in close_genres:
        G.add_edge(genre,close_genre)
# - - - - - - - - - - - - - FUNCTIONS FOR MY SANITY - - - - - - - - -

def distance_to_top_three(genre):
    scalar = 15
    color_min, color_max = 16,240

    try: d_rap    = np.clip(nx.shortest_path_length(G,genre,"rap") * scalar,color_min,color_max) 
    except: d_rap = color_max
    try: d_rock   = np.clip(nx.shortest_path_length(G,genre,"rock") * scalar,color_min,color_max) 
    except: d_rock = color_max
    try: d_pop    = np.clip(nx.shortest_path_length(G,genre,"latin pop") * scalar,color_min,color_max) 
    except: d_pop = color_max

    red,green,blue = hex(255 - d_rap)[2:],hex(255 - d_rock)[2:],hex(255 - d_pop)[2:]

    return red,green,blue

def default_map():
    # - - - - - - - - - - DEFINE GRAPH METADATA - - - - - - - - - - - - 
    graph_gjgf = gv.convert.networkx_to_gjgf(G)
    graph_gjgf["graph"]["metadata"] = {
        "background_color" : "#151515",
        "node_color" : "#444444",
        "node_label_color" : "white",
        "edge_color" : "white"
    }


    # DEFINE NODE STYLING (SIZE COLOR AND LABEL SIZE)

    for genre in relationship_matrix.index.values:

        node_size = len(G.edges([f'{genre}'])) * 4 + 10
        red,green,blue = distance_to_top_three(genre)

        graph_gjgf["graph"]["nodes"][f"{genre}"]["metadata"] = {
            "hover" : genre,
            "color" : f'#{red}{green}{blue}',
            "size": node_size,
            "label_size": 100 if genre in ["pop","rock","rap","latin pop"] else 10
            }

    map_object = gv.vis(graph_gjgf,
                        show_details_toggle_button = False,
                        show_menu_toggle_button = False,
                        edge_curvature=0.3,
                        gravitational_constant = -4000
                        )

    map_html = map_object.to_html()

    return map_html

def rooted_map(selected_genres,levels = 0):
    
    i = 0
    roots = list(selected_genres)
    display_genres = roots[:]


    while i < levels:
        for genre in roots:
            filter = relationship_matrix.loc[:,genre] < distance_threshold
            display_genres.extend(list(relationship_matrix.loc[:,genre][filter].index.values))
        
        display_genres = pd.Series(display_genres).unique().tolist()
        roots = display_genres[:]
        i = i+1
        
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
        graph_gjgf["graph"]["nodes"][f"{genre}"]["metadata"] = {
            "hover": genre,
            "color": node_color if genre in selected_genres else "#888888",
            "size": len(G_copy.edges([f'{genre}'])) * 4 + 10
        }

    map_object = gv.vis(graph_gjgf,
                        show_details_toggle_button = False,
                        show_menu_toggle_button = False,
                        edge_curvature=0.3,
                        gravitational_constant = -4000
                        )

    map_html = map_object.to_html()

    return map_html

# - - - - - - - - - LOGIC FOR WHICH MAP TO DISPLAY + REST OF STREAMLIT APP - - - - - - - - - 
if list(selected_genres) == []:
    map_html = default_map()
    components.html(map_html,height = 480)
else:
    map_html = rooted_map(selected_genres,levels)
    components.html(map_html,height = 480)


st.write("""
Welcome to charting sounds! This app is an attempt to visualize all (or at least a lot!) of musical genres in an interactive map for users to explore and find new music.
""")
st.markdown('''
This entire project would only be possible thanks to the work done by Glenn McDonald over at [Every Noise at Once](https://everynoise.com)
The following table shows the relationships between different musical genres as *distances*. Smaller distances mean genres are closer, and larger distances mean those genres are distant.
This measure of "distance" is calculated based on the lists of genres found [here](https://everynoise.com/everynoise1d.cgi?scope=all). More details about the calculation can be found on my gihub [here](https://github.com/coco-zxc/charting-sounds)
''')
st.dataframe(relationship_matrix)
st.write()
