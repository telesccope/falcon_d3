from flask import Flask, jsonify, send_from_directory
import json
from flask_cors import CORS
import os
import geopandas as gpd
import networkx as nx
import math

from database import db
from utils import dijkstra_with_steps, astar_with_steps, bellman_ford_with_steps, euclidean_heuristic, floyd_warshall_with_steps, calculate_total_weight

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_folder='../frontend', static_url_path='')

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "data/performance.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/graph', methods=['GET'])
def get_all_graphs():
    graph_files = os.listdir('data/graph')
    graph_ids = [os.path.splitext(filename)[0] for filename in graph_files if filename.endswith('.geojson')]
    return jsonify(graph_ids)

@app.route('/api/graph/<graph_id>', methods=['GET'])
def get_graph(graph_id):
    try:
        with open(f'data/graph/{graph_id}.geojson') as f:
            graph = json.load(f)
        return jsonify(graph)
    except FileNotFoundError:
        return jsonify({'error': 'Graph not found'}), 404

@app.route('/api/algorithms', methods=['GET'])
def get_all_algorithms():
    algorithms = ['Dijkstra', 'A*', 'Bellman-Ford', 'Floyd-Warshall']
    return jsonify(algorithms)

@app.route('/api/shortest-path/<string:graph>/<string:algorithm>/<string:source>/<string:target>')
def get_shortest_path(graph, algorithm, source, target):
    # Load the graph from the geojson file
    try:
        gdf = gpd.read_file(f'./data/graph/{graph}.geojson')
    except FileNotFoundError:
        return jsonify({'error': 'Graph not found'}), 404

    # Create a directed graph
    G = nx.DiGraph()
    edges = []

    for _, row in gdf.iterrows():
        geom = row.geometry
        if geom.geom_type == 'LineString':
            # Iterate over each pair of consecutive coordinates
            coords = list(geom.coords)
            for i in range(len(coords) - 1):
                start_node = tuple(round(coord, 3) for coord in coords[i])
                end_node = tuple(round(coord, 3) for coord in coords[i + 1])
                length = math.dist(start_node, end_node)  # Calculate the distance between points
                edges.append((start_node, end_node, length))
                edges.append((end_node, start_node, length))
                fid = row['fid']
                #print(f"Added edge from {start_node} to {end_node} with length {length}")

    G.add_weighted_edges_from(edges)

    # Convert source and target to tuples
    source = tuple(map(float, source.split(',')))
    target = tuple(map(float, target.split(',')))

    # Normalize source and target coordinates
    source = tuple(round(coord, 3) for coord in source)
    target = tuple(round(coord, 3) for coord in target)
    print(f"Source: {source}, Target: {target}")
    #print(f"Graph nodes: {G.nodes}")
    # Check if source and target exist in the graph
    if source not in G or target not in G:
        #同时return source，taget和graph的nodes
        return jsonify({'error': 'Source or target not found', 'source': source, 'target': target, 'nodes': list(G.nodes)}), 400

    if algorithm == 'Dijkstra':
        steps, path, time_taken = dijkstra_with_steps(G, source, target)
        total_weight = calculate_total_weight(G, path)
    elif algorithm == 'A*':
        steps, path, time_taken = astar_with_steps(G, source, target, heuristic=euclidean_heuristic)
        total_weight = calculate_total_weight(G, path)
    elif algorithm == 'BellmanFord':
        steps, path, total_weight, time_taken = bellman_ford_with_steps(G, source, target)
        total_weight = calculate_total_weight(G, path)
    else:
        return jsonify({'error': 'Algorithm not supported'}), 400

    # Return all information
    return jsonify({
        'steps': steps,
        'path': path,
        'total_weight': round(total_weight,3),
        'time_taken': round(time_taken*1000,3)
    })


def create_tables():
    """Create database tables."""
    with app.app_context():
        db.create_all()
    print('Database tables created.')

def insert_dummy_data():
    """Insert dummy data into the database."""
    with app.app_context():
        example_data = [
            PathPerformance(start_node='A', end_node='D', algorithm='Dijkstra', steps=3, execution_time=0.002),
            PathPerformance(start_node='B', end_node='E', algorithm='A*', steps=4, execution_time=0.003)
        ]
        db.session.bulk_save_objects(example_data)
        db.session.commit()
    print('Inserted dummy data into the database.')

if __name__ == '__main__':
    create_tables()  # Create tables on startup
    # insert_dummy_data()
    app.run(debug=True, host='0.0.0.0', port=5001)
