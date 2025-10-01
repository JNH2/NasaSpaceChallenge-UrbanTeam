import StreetNetwork as sn
import networkx as nx
import osmnx as ox
from typing import List, Tuple
import matplotlib.pyplot as plt
import simulation as sim        

def composite_cost_function(u, v, data, alpha: float):
    length_cost = data['length']
    crowding_cost = data['crowding_level']
    total_cost = (alpha * length_cost) + ((1 - alpha) * 100 * crowding_cost)
    return total_cost

def calculate_shortest_path_composite(G: nx.MultiDiGraph, orig_node: int, target_node: int, alpha:float) -> Tuple[List, float]:
    print(f"\n--Processor: Calculating composite cost shortest path (Alpha = {alpha:.2f})...)")
    route = ox.shortest_path(G, orig_node, target_node, weight=lambda u, v, data: composite_cost_function(u, v, data, alpha = alpha))
    total_composite_cost = sum(composite_cost_function(u, v, G.get_edge_data(u, v, 0), alpha =alpha) for u, v in zip(route[:-1], route[1:], route[1:]))
    print(f"Path calcuated. Total Composite Cost: {total_composite_cost: .2f}")
    return route, total_composite_cost

def plot_composite_route(G: nx.MultiDiGraph, route: List, filename: str, cost:float):
    print("\n---Visualizatig the final composite path...")
    fig, ax = ox.plot_graph_route(
        G,
        route,
        route_color='r',
        route_linewidth=4,
        node_size=0,
        bgcolor='w',
        edge_color='#666666',
        edge_linewidth=0.5,
        show=True,
        close=False
    )
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Composite cost shortest path plot saved as '{filename}'")


def run_analysis():
    place = "Zurich, Switzerland"
    orig_lat, orig_lon = 47.378, 8.540 #start point: HB
    target_lat, target_lon = 47.366, 8.548 #end point: Sechslautenplatz
    ALPHA = 0.5
    G = sn.load_zurich_walk_network(place)
    #sn.plot_and_save_network(G, filename = "zurih_walk_network_encapsulated.png")
    orig_node, target_node = sn.find_nearest_nodes(G, orig_lat, orig_lon, target_lat, target_lon)
    
    print(f"Start node ID(HB): {orig_node}")
    print(f"End node ID(Sechsautenplatz): {target_node}")

if __name__ == "__main__":
    run_analysis()

    G_modified = G.copy()
    G_modified = sim.add_crowding_attribute(G_modified)
    block_polygon = sim.define_zurich_block_polygon()
    G_modified = sim.simulate_and_apply_blockades_polygon(G_modified, block_polygon)    
    
    route_composite, cost_composite = calculate_shortest_path_composite(G_modified, orig_node, target_node, alpha=ALPHA)
    plot_composite_route(G_modified, route_composite, filename = "zurich_composite_path.png", cost=cost_composite)

if __name__ == "__main__":
    run_analysis()