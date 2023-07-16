# Charting Sounds

Checkout the working prototype [here](https://chartingsounds.streamlit.app/)

<img width="1131" alt="Screenshot 2023-06-19 at 16 40 26" src="https://github.com/coco-zxc/charting-sounds/assets/109617201/1e396ca8-cb5e-4e77-a727-d3d6406e38d8" href="https://chartingsounds.streamlit.app/">

Inspired by the work of Glenn McDonald, this project was meant to visualize musical genres as a mathematical Network, showcasing their relationships in a simple format.

This is done through 3 different steps: 
1. Gather data found at Every Noise at Once through Web Scraping. [see here](https://github.com/coco-zxc/charting-sounds/blob/main/every_noise_at_once.py)
2. Calculate a "distance" between musical genres and generate a relationship matrix (heatmap) [see here](https://github.com/coco-zxc/charting-sounds/blob/main/genre_distance_calculator.py)
3. Use GraVis to generate an interactive network that users can explore to find new music and share through Streamlit.

## Acknowledgements
This project would not have been possible without the previous work of Glenn McDonald, creator of [Every Noise at Once](https://everynoise.com)
