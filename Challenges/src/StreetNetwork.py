import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

#help(ox)
#help(nx)

def load_zurich_walk_network(place) -> nx.MultiDiGraph:
   # Configure OSMnx settings
   ox.settings.use_cache = True
   ox.settings.log_console = True
  
   # Download the street network data for the specified place
   G = ox.graph_from_place(place, network_type='walk')
   print("n---nodes:", len(G.nodes))
   print("n---edges:", len(G.edges))
   return G

def plot_and_save_network(G: nx.MultiDiGraph, filename):
   print("\n---Plotting the street network...")
   fig, ax = ox.plot_graph(
   G,
   bgcolor = 'w',
   node_size = 0,
   edge_color = '#666666',
   edge_linewidth = 0.5,
   show = True,
   close = False
   )
   fig.savefig(filename, dpi=300, bbox_inches='tight')
   print("Street network plot saved as 'zurich_walk_network.png'")

def find_nearest_nodes(G: nx.MultiDiGraph, orig_lat: float, orig_lon: float, target_lat: float, target_lon: float) -> tuple[int, int]:
   orig_node_id = ox.nearest_nodes(G, orig_lon, orig_lat)
   target_node_id = ox.nearest_nodes(G, target_lon, target_lat)#find the target node 
   return orig_node_id, target_node_id
