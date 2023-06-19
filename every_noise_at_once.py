import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_genre_list_base():
    '''
    This funtion returns a list of genres in Every Noise at Once by Glenn McDonald. 
    The list contains all genres sorted by popularity (Descending)
    '''
    url = "https://everynoise.com/everynoise1d.cgi?scope=all"
    html = requests.get(url).text
    soup = BeautifulSoup(html,"html.parser")
    rows = soup.find_all("tr")

    genre_list_by_popularity=[]

    for row in rows:
        genre_name = row.find_all('td')[2].text
        genre_list_by_popularity.append(genre_name)

    return genre_list_by_popularity
def get_genres_by_root(root):
    '''
    This function returns a list of genres sorted by how closely related they are to "root".
    '''
    root=str(root).replace(" ","%20")

    url = f"https://everynoise.com/everynoise1d.cgi?scope=all&root={root}"
    html=requests.get(url).text
    soup=BeautifulSoup(html,"html.parser")


    genre_list=[]
    rows = soup.find_all("tr")
    for row in rows:
        data = row.find_all('td')
        genre = str(data[2].text)[:-1]
        genre_list.append(genre)
    
    return genre_list

def main():
    #Gets a nominal list of genres and counts the total number of genres to 
    #create a Dataframe of that size
    genres_by_popularity = get_genre_list_base()
    number_of_genres = len(genres_by_popularity)
    index_range = range(1,number_of_genres+1)
    root_table = pd.DataFrame(index=index_range)

    #Main loop that gets the list based on a root an appends the information into a dataframe
    for i,genre in enumerate(genres_by_popularity) :
        print(f'Current root is: "{genre}"')
        genres_by_root = get_genres_by_root(genre)

        #Note: lists from ENAO vary in length
        #The following if statement ensures all lists are the same size before being appended
        if len(genres_by_root) <= number_of_genres:
            list_extension = [np.nan] * (number_of_genres - len(genres_by_root))
            genres_by_root.extend(list_extension)
            genres_by_root = pd.DataFrame(genres_by_root)

        root_table = pd.concat([root_table , genres_by_root],axis=1,sort=True)
        print(f'{genre} information has been appended ({i+1}/{number_of_genres})')

        #This code runs for a while, in case of a connection error, this piece of code creates a CSV backup
        if (i+1)%10 == 0:
            root_table.to_csv("root_table_backup.csv")

    root_table.to_csv("root_table.csv")
        

if __name__ == "__main__":
    main()