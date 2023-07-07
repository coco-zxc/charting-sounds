import numpy as np
import pandas as pd

genres_by_root = pd.read_csv("/Users/georgegg/Documents/Projects/Where's my Sound ?/root_table.csv",index_col=0)
genres_by_root.columns = genres_by_root.iloc[0]
genres_by_root.drop("po",axis=1,inplace=True)
genres_by_root.drop("animal singing",axis=1,inplace=True)
genres_by_root = genres_by_root.transpose().drop_duplicates(subset=0,keep=False).transpose()

clean_table=[]

for genre in genres_by_root.columns.values:
    
    index_to_delete = genres_by_root[genres_by_root[genre] == "animal singing"].index.values
    clean_table.append(genres_by_root[genre].drop(index_to_delete).reset_index(drop=True))
    #print(f'{genre} has been cleaned')

clean_df = pd.DataFrame(clean_table).transpose()
clean_df.to_csv("root_table_clean.csv")



