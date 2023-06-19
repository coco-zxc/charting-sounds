import numpy as np
import pandas as pd

def init():
    global genres_by_root
    global genres_by_popularity
    genres_by_root = pd.read_csv("/Users/georgegg/Documents/Projects/Where's my Sound ?/root_table.csv",index_col=0)
    genres_by_root.columns = genres_by_root.iloc[0]
    
    genres_by_root = genres_by_root.drop("po",axis=1)
    genres_by_popularity = genres_by_root.iloc[0]

def calculate_distance_between_genres(genre1,genre2):
    '''
    This funtion takes two genre strings as parameters and scores how closely they are related
    '''
    distance1 = genres_by_root[genre1][genres_by_root[genre1] == genre2].index[0]
    distance2 = genres_by_root[genre2][genres_by_root[genre2] == genre1].index[0]
    
    scale = 5
    score = (distance1//scale) * (distance2//scale)
    
    return score

def main():
    init()
    
    #select the amount of genres to include:
    top_genres = genres_by_popularity[0:2000]
    #initialize squared DF
    number_of_genres = len(top_genres)
    genre_relationship_matrix = pd.DataFrame(index=range(number_of_genres),columns=range(number_of_genres))
    genre_relationship_matrix.set_index(top_genres,inplace=True)
    genre_relationship_matrix.columns = top_genres

    
    for i1,genre1 in enumerate(top_genres):
        print(f"Calculating distances for genre: '{genre1}'")

        for genre2 in top_genres[i1:]:
            genre_relationship_matrix.at[genre2,genre1] = calculate_distance_between_genres(genre1,genre2)
        
        print(f"'{genre1}' done")

    genre_relationship_matrix.to_csv("relationship_matrix.csv")

if __name__ == "__main__":
    main()