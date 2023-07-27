import requests
from json import loads
import pandas as pd
from time import sleep
from numpy import NaN
from spotify_api_test import get_token

relationship_matrix = pd.read_csv("Data/relationship_matrix_3000_genres.csv").set_index('0')
relationship_matrix.replace(NaN,0,inplace=True)
relationship_matrix = relationship_matrix + relationship_matrix.transpose()

token = get_token()
def search_playlist_id(search_query:str):

    base_url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    query = f"?q={search_query}&type=playlist&limit=5"
    url = base_url + query

    try:
        response = requests.get(url=url,headers=headers)
        if response.status_code == 429:
            sleep(30)
            response = requests.get(url=url,headers=headers)
        else:
            sleep(0.1)

        items = loads(response.content)["playlists"]["items"]
    
    except:
        items = {0:{"name":NaN,"id":NaN }}

    
    
    if len(items) < 5:
        return NaN,NaN
    else:
        for i in range(0,len(items)):
            if "Mix" in str(items[i]["name"]):
                None
            else:
                return items[i]["name"],items[i]["id"]




        


genres = relationship_matrix.index.values
genre_playlist_id_table = pd.DataFrame(columns=["genre_name","playlist_name","spotify_id"],index=range(1,len(genres)+1))
genre_playlist_id_table.loc[:,"genre_name"] = genres
genre_playlist_id_table.set_index("genre_name",inplace=True)


for i,genre in enumerate(genres):
    playlist_name,spotify_id = search_playlist_id(genre)
    genre_playlist_id_table.at[genre,"playlist_name"] = playlist_name
    genre_playlist_id_table.at[genre,"spotify_id"] = spotify_id
    print(f'Genre {genre} appended with ID {spotify_id}. Playlist name: {playlist_name}. Progress: {i}/{len(genres)}')

print(genre_playlist_id_table.head())

genre_playlist_id_table.to_csv("spotify_id_reference_table.csv")


