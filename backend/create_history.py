import networkx as nx
import geopandas as gpd
from utils import generate_random_point_pairs, calculate_total_weight, dijkstra_with_steps, astar_with_steps, manhattan_heuristic, euclidean_heuristic, bellman_ford_with_steps, floyd_warshall_with_steps
from database_manager import DatabaseManager

G = nx.DiGraph()
edges = []

starts = []
ends = []

gdf = gpd.read_file('./data/graph/complete_graph.geojson')

for _, row in gdf.iterrows():
    geom = row.geometry

    if geom.geom_type == 'LineString':
        start_node = tuple(geom.coords[0])
        end_node = tuple(geom.coords[-1])
        length = geom.length
        edges.append((start_node, end_node, length))
        edges.append((end_node, start_node, length))

        starts.append(start_node)
        ends.append(end_node)
    else:
        raise ValueError(f"Unexpected geometry type: {geom.geom_type}")
    
G.add_weighted_edges_from(edges)

start_pairs, end_pairs = generate_random_point_pairs(starts,ends)

'''
start_node = (462555.702, 89140.515)
end_node = (463122.297, 88799.614)
'''

import json
from app import app, db
with app.app_context():
    db_manager = DatabaseManager(db)
    for i in range(1000):
        start_node = start_pairs[i]
        end_node = end_pairs[i]
        print(f"Start Node: {start_node}")
        start_node_record = db_manager.get_node_by_coordinates(start_node)
        end_node_record = db_manager.get_node_by_coordinates(end_node)

        if not start_node_record or not end_node_record:
            raise ValueError(f"Node not found for coordinates: {start_node} or {end_node}")
        
        start_node_id = start_node_record.NodeID
        end_node_id = end_node_record.NodeID
        
        # Dijkstra
        dijkstra_steps, dijkstra_path, dijkstra_time = dijkstra_with_steps(G, start_node, end_node)
        dijkstra_total_weight = calculate_total_weight(G, dijkstra_path)
        db_manager.add_shortest_path_result(
            algorithm="Dijkstra",
            start_node_id=start_node_id,
            end_node_id=end_node_id,
            path=dijkstra_path,
            total_weight=dijkstra_total_weight,
            steps=len(dijkstra_steps),
            time=dijkstra_time
        )

        # A* (Manhattan)
        astar_steps, astar_path, astar_time = astar_with_steps(G, start_node, end_node, heuristic=manhattan_heuristic)
        astar_total_weight = calculate_total_weight(G, astar_path)
        db_manager.add_shortest_path_result(
            algorithm="A* (Manhattan)",
            start_node_id=start_node_id,
            end_node_id=end_node_id,
            path=astar_path,
            total_weight=astar_total_weight,
            steps=len(astar_steps),
            time=astar_time
        )

        # A* (Euclidean)
        astar_steps2, astar_path2, astar_time2 = astar_with_steps(G, start_node, end_node, heuristic=euclidean_heuristic)
        astar_total_weight2 = calculate_total_weight(G, astar_path2)
        db_manager.add_shortest_path_result(
            algorithm="A* (Euclidean)",
            start_node_id=start_node_id,
            end_node_id=end_node_id,
            path=astar_path2,
            total_weight=astar_total_weight2,
            steps=len(astar_steps2),
            time=astar_time2
        )

