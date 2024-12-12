import networkx as nx
import geopandas as gpd
import heapq
import math
import random
import time

def dijkstra_with_steps(graph, start, end):
    start_time = time.time()
    queue = [(0, start, [])]
    seen = set()
    min_dist = {start: 0}
    steps = []
    final_path = []

    while queue:
        (cost, node, path) = heapq.heappop(queue)
        
        if node in seen:
            continue
        
        seen.add(node)
        path = path + [node]
        steps.append((node, cost, path))
        
        if node == end:
            final_path = path
            break
        
        for neighbor, data in graph[node].items():
            if neighbor in seen:
                continue
            prev_cost = min_dist.get(neighbor, float('inf'))
            new_cost = cost + data['weight']
            if new_cost < prev_cost:
                min_dist[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor, path))
    
    end_time = time.time()
    return steps, final_path, end_time - start_time

def bellman_ford_with_steps(graph, start, end):
    start_time = time.time()
    steps = []
    distance = {node: float('inf') for node in graph}
    distance[start] = 0
    predecessor = {node: None for node in graph}

    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbor, data in graph[node].items():
                if distance[node] + data['weight'] < distance[neighbor]:
                    distance[neighbor] = distance[node] + data['weight']
                    predecessor[neighbor] = node
                    steps.append((node, neighbor, distance[neighbor]))

    # Check for negative weight cycles
    for node in graph:
        for neighbor, data in graph[node].items():
            if distance[node] + data['weight'] < distance[neighbor]:
                raise ValueError("Graph contains a negative weight cycle")

    # Reconstruct path
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = predecessor[current]

    end_time = time.time()
    return steps, path, distance[end], end_time - start_time

def floyd_warshall_with_steps(graph):
    start_time = time.time()
    dist = {u: {v: float('inf') for v in graph} for u in graph}
    next_node = {u: {v: None for v in graph} for u in graph}
    steps = []

    for u in graph:
        dist[u][u] = 0
        for v, data in graph[u].items():
            dist[u][v] = data['weight']
            next_node[u][v] = v

    for k in graph:
        for i in graph:
            for j in graph:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]
                    steps.append((i, j, dist[i][j]))

    end_time = time.time()
    return steps, dist, next_node, end_time - start_time

def astar_with_steps(graph, start, end, heuristic=None):
    start_time = time.time()
    if heuristic is None:
        heuristic = lambda u, v: 0
    
    queue = [(0, start, [])]
    seen = set()
    min_dist = {start: 0}
    steps = []
    final_path = []

    while queue:
        (cost, node, path) = heapq.heappop(queue)
        
        if node in seen:
            continue
        
        seen.add(node)
        path = path + [node]
        steps.append((node, cost, path))
        
        if node == end:
            final_path = path
            break
        
        for neighbor, data in graph[node].items():
            if neighbor in seen:
                continue
            prev_cost = min_dist.get(neighbor, float('inf'))
            new_cost = cost + data['weight']
            if new_cost < prev_cost:
                min_dist[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, end)
                heapq.heappush(queue, (priority, neighbor, path))
    
    end_time = time.time()
    return steps, final_path, end_time - start_time

def manhattan_heuristic(u, v):
    x1, y1 = u
    x2, y2 = v
    return abs(x1 - x2) + abs(y1 - y2)

def euclidean_heuristic(u, v):
    x1, y1 = u
    x2, y2 = v
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calculate_total_weight(graph, path):
    total_weight = 0
    for i in range(1, len(path)):
        node = path[i-1]
        next_node = path[i]
        edge_weight = graph[node][next_node]['weight']
        total_weight += edge_weight
    return total_weight

def generate_random_point_pairs(starts, ends, num_pairs=1000):
    '''
    Randomly generate a specified number of point pairs with different start and end points
    
    Parameters:
    starts (list): List of start points
    ends (list): List of end points
    num_pairs (int): Number of point pairs to generate, default is 1000
    
    Return:
    A tuple containing lists of start points and end points
    '''
    # Check if the length of input lists > num_pairs
    if len(starts) < num_pairs or len(ends) < num_pairs:
        raise ValueError('Input list length must be at least the number of point pairs.')
    
    start_indices = random.sample(range(len(starts)), num_pairs)
    end_indices = random.sample(range(len(ends)), num_pairs)

    # Ensure start and end points are different
    for i in range(num_pairs):
        while starts[start_indices[i]] == ends[end_indices[i]]:
            end_indices[i] = random.choice(range(len(ends)))

    start_pairs = [starts[idx] for idx in start_indices]
    end_pairs = [ends[idx] for idx in end_indices]

    return start_pairs, end_pairs


def insert_network_data(data, db_manager):
    """Parses and inserts network data into the database."""
    nodes = {}  
    edges = []  

    for feature in data['features']:
        properties = feature['properties']
        geometry = feature['geometry']

        coordinates = geometry['coordinates']

        for idx, coord in enumerate(coordinates):
            coord_str = f"{coord[0]},{coord[1]}" 
            if coord_str not in nodes:
                node = db_manager.add_node(name=f"Node_{len(nodes) + 1}", coordinates=coord_str)
                nodes[coord_str] = node.NodeID

            if idx == 0:
                continue

            source = nodes[f"{coordinates[idx - 1][0]},{coordinates[idx - 1][1]}"]
            destination = nodes[coord_str]
            distance = properties['length']  
            bidirectional = True  

            edges.append((source, destination, distance, bidirectional))

    print(f"Inserted {len(nodes)} nodes")

    for edge in edges:
        db_manager.add_edge(
            source_node_id=edge[0],
            destination_node_id=edge[1],
            distance=edge[2],
            bidirectional=edge[3]
        )


if __name__ == '__main__':
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
    
    # Initialize total steps, paths, time, weight variables for each algorithm
    dijkstra_steps_sum = 0
    dijkstra_time_sum = 0
    dijkstra_total_weight_sum = 0
    astar_steps_sum = 0
    astar_time_sum = 0
    astar_total_weight_sum = 0
    astar_steps2_sum = 0
    astar_time2_sum = 0
    astar_total_weight2_sum = 0
    bellman_ford_steps_sum = 0
    bellman_ford_time_sum = 0
    bellman_ford_total_weight_sum = 0
    floyd_warshall_steps_sum = 0
    floyd_warshall_time_sum = 0
    floyd_warshall_total_weight_sum = 0

    '''
    start_node = (462555.702, 89140.515)
    end_node = (463122.297, 88799.614)
    '''

    for i in range(1000):
        start_node = start_pairs[i]
        end_node = end_pairs[i]

        # Dijkstra
        dijkstra_steps, dijkstra_path, dijkstra_time = dijkstra_with_steps(G, start_node, end_node)
        dijkstra_total_weight = calculate_total_weight(G, dijkstra_path)
        dijkstra_steps_sum += len(dijkstra_steps)
        dijkstra_total_weight_sum += dijkstra_total_weight
        dijkstra_time_sum += dijkstra_time
        
        # A* (Manhattan)
        astar_steps, astar_path, astar_time = astar_with_steps(G, start_node, end_node, heuristic=manhattan_heuristic)
        astar_total_weight = calculate_total_weight(G, astar_path)
        astar_steps_sum += len(astar_steps)
        astar_total_weight_sum += astar_total_weight
        astar_time_sum += astar_time

        # A* (Euclidean)
        astar_steps2, astar_path2, astar_time2 = astar_with_steps(G, start_node, end_node, heuristic=euclidean_heuristic)
        astar_total_weight2 = calculate_total_weight(G, astar_path2)
        astar_steps2_sum += len(astar_steps2)
        astar_total_weight2_sum += astar_total_weight2
        astar_time2_sum += astar_time2
        '''
        # Bellman-Ford
        bellman_ford_steps, bellman_ford_path, bellman_ford_total_weight, bellman_ford_time = bellman_ford_with_steps(G, start_node, end_node)
        bellman_ford_steps_sum += len(bellman_ford_steps)
        bellman_ford_total_weight_sum += bellman_ford_total_weight
        bellman_ford_time_sum += bellman_ford_time

        # Floyd-Warshall
        floyd_warshall_steps, floyd_warshall_dist, floyd_warshall_next_node, floyd_warshall_time = floyd_warshall_with_steps(G)
        floyd_warshall_total_weight = floyd_warshall_dist[start_node][end_node]
        floyd_warshall_steps_sum += len(floyd_warshall_steps)
        floyd_warshall_total_weight_sum += floyd_warshall_total_weight
        floyd_warshall_time_sum += floyd_warshall_time
        '''

    print(f"Dijkstra Steps: {dijkstra_steps_sum/1000}")
    print(f"Dijkstra Total Weight: {dijkstra_total_weight_sum/1000}")
    print(f"Dijkstra Time: {dijkstra_time_sum/1000}")

    print(f"A* (Manhattan) Steps: {astar_steps_sum/1000}")
    print(f"A* (Manhattan) Total Weight: {astar_total_weight_sum/1000}")
    print(f"A* (Manhattan) Time: {astar_time_sum/1000}")

    print(f"A* (Euclidean) Steps: {astar_steps2_sum/1000}")
    print(f"A* (Euclidean) Total Weight: {astar_total_weight2_sum/1000}")
    print(f"A* (Euclidean) Time: {astar_time2_sum/1000}")
    
    