import pandas as pd
import streamlit as st

relationship_matrix = pd.read_csv("Data/relationship_matrix_3000_genres.csv")
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
