import gravis as gv

graph1 = {
    'graph':{
        'directed': True,
        'metadata': {
            'arrow_size': 5,
            'background_color': 'black',
            'edge_size': 3,
            'edge_label_size': 14,
            'edge_label_color': 'white',
            'node_size': 15,
            'node_color': 'white',
        },
        'nodes': {
            1: {'metadata': {'shape': 'rectangle', 'y': 200}},
            2: {},
            3: {},
            4: {'metadata': {'shape': 'rectangle', 'y': 200}},
            5: {'metadata': {'shape': 'hexagon', 'y': 0}},
        },
        'edges': [
            {'source': 1, 'target': 2, 'metadata': {'color': '#d73027', 'de': 'Das',   'en': 'This'}},
            {'source': 2, 'target': 3, 'metadata': {'color': '#f46d43', 'de': 'ist',   'en': 'is'}},
            {'source': 3, 'target': 1, 'metadata': {'color': '#fdae61', 'de': 'das',   'en': 'the'}},
            {'source': 1, 'target': 4, 'metadata': {'color': '#fee08b', 'de': 'Haus',  'en': 'house'}},
            {'source': 4, 'target': 3, 'metadata': {'color': '#d9ef8b', 'de': 'vom',   'en': 'of'}},
            {'source': 3, 'target': 5, 'metadata': {'color': '#a6d96a', 'de': 'Ni-.',  'en': 'San-'}},
            {'source': 5, 'target': 2, 'metadata': {'color': '#66bd63', 'de': 'ko-',   'en': 'ta'}},
            {'source': 2, 'target': 4, 'metadata': {'color': '#1a9850', 'de': 'laus.', 'en': 'Claus.'}},
        ],
    }
}

gv.vis(graph1).export_html("gravis_tester.html")