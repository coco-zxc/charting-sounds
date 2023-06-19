import numpy as np
import pandas as pd
from pyvis.network import Network


relationship_matrix = pd.read_csv("/Users/georgegg/Documents/Projects/Where's my Sound ?/relationship_matrix_1000_genres.csv",index_col=0)
relationship_matrix.replace(np.nan,0,inplace=True)
relationship_matrix = (relationship_matrix + relationship_matrix.transpose()).astype("int")
relationship_matrix = relationship_matrix.iloc[0:200,0:200]

d1,d2 = 1,50000

def categorize_genres(genre=""):

    distances     = relationship_matrix.loc[:,genre]
    close_filter  = distances < d1
    medium_filter = distances.between(d1,d2,inclusive="both")
    far_filter    = distances > d2

    close_genres  = relationship_matrix[genre][close_filter] .sort_values().index.to_list()
    medium_genres = relationship_matrix[genre][medium_filter].sort_values().index.to_list()
    far_genres    = relationship_matrix[genre][far_filter]   .sort_values().index.to_list()

    return close_genres,medium_genres,far_genres

def main():
    #region Creates a dataframe that categorizes each genres' relative close, medium and far away genres
    
    number_of_genres = len(relationship_matrix.index.values)
    genre_table = pd.DataFrame(columns=["Genre","Close","Medium","Far"],index=range(0,number_of_genres))

    for i,genre in enumerate(relationship_matrix.index.values):

        close_genres,medium_genres,far_genres = categorize_genres(genre)

        genre_table.at[i,"Genre"] = genre
        genre_table.at[i,"Close"] = close_genres
        genre_table.at[i,"Medium"] = medium_genres
        genre_table.at[i,"Far"] = far_genres

    #endregion

    
    net = Network(
        neighborhood_highlight=True,
        select_menu=True,
        bgcolor="#222222",
        font_color="white"
        )
    
    genre_table.set_index("Genre",inplace=True)

    flat_list = [item for close_list in genre_table["Close"].values for item in close_list]

    for genre in genre_table.index.values:
        
        node_size = 10 + (len(genre_table.at[genre,"Close"]) + flat_list.count(genre)) * 2

        
        red   = 'ee' if 'rap' in genre_table.at[genre,"Close"] else 'bb' if 'rap' in genre_table.at[genre,"Medium"] else '88'
        green = 'ee' if 'rock' in genre_table.at[genre,"Close"] else 'bb' if 'rock' in genre_table.at[genre,"Medium"] else '88'
        blue  = 'ee' if 'pop' in genre_table.at[genre,"Close"] else 'bb' if 'pop' in genre_table.at[genre,"Medium"] else '88'
        
        if genre == 'rap':
            node_color = '#ff6666'
        elif genre == 'rock':
            node_color = '#66ff66'
        elif genre == 'pop':
            node_color = '#6666ff'
        else:
            node_color = f'#{red}{green}{blue}'

        net.add_node(genre,color=node_color,size=node_size,borderWidthSelected = 4)

    for close_list in genre_table["Close"].values:
        for genre in close_list[1:]:
            net.add_edge(close_list[0],genre)

    net.show_buttons(filter_=['physics'])
    net.show("Test1.html",notebook=False)

if __name__ == "__main__":
    main()