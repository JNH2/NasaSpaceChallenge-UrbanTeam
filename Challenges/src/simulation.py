import osmnx as ox
import networkx as nx
import random
from typing import Tuple, List
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

def define_zurich_block_polygon() -> List[Tuple[float, float]]:
    # Define the coordinates of the block polygon in Zurich
    block_polygon = [#from Bahnhofstrasse to Burklipltz to Sechselautenplatz
        (47.3718, 8.5372), # Paradeplatz 
        (47.3695, 8.5385),  # Burkliplatz
        (47.3665, 8.5410),  # Sechselautenplatz
        (47.3735, 8.5400),   # Bellevue
        (47.3735, 8.5400),  # Bahnhofquai
        (47.3718, 8.5372),  # Back to Paradeplatz
    ]
    print(f"---simulation: Defined a custom polygon with {len(block_polygon) - 1} vertices for blockade:from Bahnhofstrasse paradeplatz, Burkliplatz, Sechselautenplatz, Bellevue to back to Bahnhofquai.")
    return block_polygon

def simulate_and_apply_blockades_polygon(G: nx.MultiDiGraph, block_polygon: List[Tuple[float, float]]) -> nx.MultiDiGraph:
    # Simulate random blockades within the defined polygon
    lon_lat = [(lon, lat) for lat, lon in block_polygon] #change to (lon, lat) format for shapely
    polygon = Polygon(lon_lat) # Create a shapely polygon
    print("\n---Simulating blockades within the defined polygon...")
    # Find edges within the polygon and remove them from the graph
    gdf_edges = ox.graph_to_gdfs(G, nodes=False, edges=True) # Get edges as GeoDataFrame
    edges_in_polygon = gdf_edges[gdf_edges.geometry.intersects(polygon)] # Find edges intersecting the polygon
    edges_to_remove = [(row['u'], row['v'], row['key']) for index, row in edges_in_polygon.iterrows()]
    G.remove_edges_from(edges_to_remove)
    print(f"Removed {len(edges_to_remove)} edges within the simulatd Bahnhofstrasse/Burkliplatz/Sechselautenplatz zone.")
    return G

def add_crowding_attribute(G: nx.MultiDiGraph) -> nx.MultiDiGraph:
    print("\n---Adding crowding attributes to edges...")
    #  Add a 'crowding' attribute to each edge in the graph
    for u, v, key, data in G.edges(keys=True, data=True): #u and v are the nodes, key is the edge key, data is the edge attributes
        # Simulate crowding level as a random integer between 1 and 10
        data['crowding_level'] = random.randint(1, 10)
    return G