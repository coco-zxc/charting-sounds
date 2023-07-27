import numpy as np
import pandas as pd
import networkx as nx
from colour import Color
import gravis as gv


def generate_network(relationship_matrix:pd.DataFrame,distance_threshold:int):
    '''
    This funtion takes a relationship matrix and a distance threshold, creating a NetworkX graph object in return.
    '''
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

def color_calculator(graph:nx.Graph,origin_genre:str,target_genres:list):

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


def default_map(relationship_matrix:pd.DataFrame,graph:nx.Graph):
    # - - - - - - - - - - DEFINE GRAPH METADATA - - - - - - - - - - - - 
    graph_gjgf = gv.convert.networkx_to_gjgf(graph)
    graph_gjgf["graph"]["metadata"] = {
        "background_color" : "#151515",
        "node_color" : "#444444",
        "node_label_color" : "white",
        "edge_color" : "gray"
    }


    # DEFINE NODE STYLING

    for genre in relationship_matrix.index.values:

        node_size = len(graph.edges([f'{genre}'])) * 4 + 10

        graph_gjgf["graph"]["nodes"][f"{genre}"]["metadata"] = {
            "hover" : genre,
            "color" : color_calculator(graph,genre,["latin pop","rock","rap"]),
            "size": node_size,
            "label_size": 100 if genre in ["pop","rock","rap","latin pop"] else np.clip(node_size / 4, 15,100)
            }

    map_object = gv.vis(graph_gjgf,
                        show_details_toggle_button = False,
                        show_menu_toggle_button = False,
                        edge_curvature=0.3,
                        gravitational_constant = -2000,
                        node_hover_neighborhood=True,
                        node_hover_tooltip=True,
                        large_graph_threshold=1000)

    map_html = map_object.to_html()

    return map_html


def rooted_map(graph:nx.Graph,relationship_matrix:pd.DataFrame,selected_genres,degrees_of_separation:int,distance_threshold):

    roots = list(selected_genres)
    display_genres = roots[:]

    for i in range(0,degrees_of_separation):
        for genre in roots:
            filter = relationship_matrix.loc[:,genre] < distance_threshold
            display_genres.extend(list(relationship_matrix.loc[:,genre][filter].index.values))
        display_genres = pd.Series(display_genres).unique().tolist()
        roots = display_genres[:]
        
    G_copy = graph.subgraph(display_genres)

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
                        node_hover_tooltip=True,
                        large_graph_threshold=1000
                        )

    map_html = map_object.to_html()

    return map_html

def path_finder_map(graph:nx.Graph,genre1:str,genre2:str):
    paths = nx.all_shortest_paths(graph,genre1,genre2)

    display_genres = []
    for path in paths:
        display_genres.extend(path)

    sub_graph = graph.subgraph(display_genres)
    graph_gjgf = gv.convert.networkx_to_gjgf(sub_graph)
    graph_gjgf["graph"]["metadata"] = {
        "background_color" : "#151515",
        "node_color" : "#444444",
        "node_label_color" : "white",
        "edge_color" : "white"
    }
    for genre in display_genres:
        graph_gjgf["graph"]["nodes"][f"{genre}"]["metadata"] = {
            "color":color_calculator(graph,genre,[genre1,genre2]),
            "size": 50 if genre in [genre1,genre2] else 30,
            "label_size":50 if genre in [genre1,genre2] else 12
        }

    
    map_object = gv.vis(graph_gjgf,
                        show_details_toggle_button = False,
                        show_menu_toggle_button = False,
                        edge_curvature=0.3,
                        gravitational_constant = -2000,
                        node_hover_neighborhood=True,
                        node_hover_tooltip=True,
                        large_graph_threshold=1000)
    map_html = map_object.to_html()
    return map_html
