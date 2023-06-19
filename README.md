# Charting Sounds

<img width="1131" alt="Screenshot 2023-06-19 at 16 40 26" src="https://github.com/coco-zxc/charting-sounds/assets/109617201/1e396ca8-cb5e-4e77-a727-d3d6406e38d8">

Inspired by Glenn McDonald's Every Noise at Once. This project plots musical genres as a mathematical Network, showcasing the relationships between musical genres.

This project uses the information found at [Every Noise at Once](https://everynoise.com) to display musical genres found on Spotify as a Mathematical Network.

This is done through 3 different steps: 
1. Gather data found at Every Noise at Once through Web Scraping. [see here](https://github.com/coco-zxc/charting-sounds/blob/main/every_noise_at_once.py)
2. Calculate the "distance" between musical genres and generate a relationship matrix (heatmap) [see here](https://github.com/coco-zxc/charting-sounds/blob/main/genre_distance_calculator.py)
3. Use PyVis to generate an interactive network that users can explore to find new music. [see here](https://github.com/coco-zxc/charting-sounds/blob/main/map.py)

Notes: While this is still uncertain, the final objective of this project is to use Spotify's developer API to give 30s of sample music for each genre. This has not yet been developed as of the publication of this README file.

Acknowledgements - This project would not have been possible without the previous work of Glenn McDonald, creator of Every Noise at Once.
