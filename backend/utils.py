import networkx as nx
import geopandas as gpd
import heapq
import math

def dijkstra_with_steps(graph, start, end):
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
    
    return steps, final_path

def bellman_ford_with_steps(graph, start, end):
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

    return steps, path, distance[end]

def floyd_warshall_with_steps(graph):
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

    return steps, dist, next_node

def astar_with_steps(graph, start, end, heuristic=None):
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
    
    return steps, final_path

def topological_sort_with_steps(graph):
    from collections import deque

    in_degree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1

    queue = deque([u for u in graph if in_degree[u] == 0])
    sorted_list = []
    steps = []

    while queue:
        u = queue.popleft()
        sorted_list.append(u)
        steps.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    if len(sorted_list) != len(graph):
        raise ValueError("Graph is not a DAG")

    return steps, sorted_list

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

if __name__ == '__main__':
    # 创建一个有向图
    G = nx.DiGraph()
    edges = []
    gdf = gpd.read_file('./data/line5.geojson')

    for _, row in gdf.iterrows():
        geom = row.geometry

        if geom.geom_type == 'LineString':
            start_node = tuple(geom.coords[0])
            end_node = tuple(geom.coords[-1])
            length = geom.length
            edges.append((start_node, end_node, length))
            edges.append((end_node, start_node, length))
        else:
            raise ValueError(f"Unexpected geometry type: {geom.geom_type}")
        
    G.add_weighted_edges_from(edges)
    
    # 设置起始和结束节点
    start_node = (462555.702, 89140.515)
    end_node = (463122.297, 88799.614)

    # Dijkstra算法
    dijkstra_steps, dijkstra_path = dijkstra_with_steps(G, start_node, end_node)
    dijkstra_total_weight = calculate_total_weight(G, dijkstra_path)
    print(f"Dijkstra Path: {dijkstra_path}")
    print(f"Dijkstra Total Weight: {dijkstra_total_weight}")
    print(f"Dijkstra Steps: {len(dijkstra_steps)}")

    # A*算法（曼哈顿启发式）
    astar_steps, astar_path = astar_with_steps(G, start_node, end_node, heuristic=manhattan_heuristic)
    astar_total_weight = calculate_total_weight(G, astar_path)
    print(f"A* (Manhattan) Path: {astar_path}")
    print(f"A* (Manhattan) Total Weight: {astar_total_weight}")
    print(f"A* (Manhattan) Steps: {len(astar_steps)}")

    # A*算法（欧氏启发式）
    astar_steps2, astar_path2 = astar_with_steps(G, start_node, end_node, heuristic=euclidean_heuristic)
    astar_total_weight2 = calculate_total_weight(G, astar_path2)
    print(f"A* (Euclidean) Path: {astar_path2}")
    print(f"A* (Euclidean) Total Weight: {astar_total_weight2}")
    print(f"A* (Euclidean) Steps: {len(astar_steps2)}")

    # Bellman-Ford算法
    try:
        bellman_ford_steps, bellman_ford_path, bellman_ford_total_weight = bellman_ford_with_steps(G, start_node, end_node)
        print(f"Bellman-Ford Path: {bellman_ford_path}")
        print(f"Bellman-Ford Total Weight: {bellman_ford_total_weight}")
        print(f"Bellman-Ford Steps: {len(bellman_ford_steps)}")
    except ValueError as e:
        print(e)

    # Floyd-Warshall算法
    floyd_warshall_steps, floyd_warshall_dist, _ = floyd_warshall_with_steps(G)
    floyd_warshall_total_weight = floyd_warshall_dist[start_node][end_node]
    print(f"Floyd-Warshall Total Weight: {floyd_warshall_total_weight}")
    print(f"Floyd-Warshall Steps: {len(floyd_warshall_steps)}")

    # 比较路径是否相同
    print(f"Same path (Dijkstra vs A*): {dijkstra_path == astar_path}")
