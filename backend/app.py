from flask import Flask, jsonify, send_from_directory
import json
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')

CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/graph')
def get_graph():
    with open('data/graph.json') as f:
        graph = json.load(f)
    return jsonify(graph)

@app.route('/api/shortest-path/<source>/<target>')
def get_shortest_path(source, target):
    # Implement your shortest path algorithm here
    # For now, return a dummy path
    path = [source, "Node2", "Node3", target]
    return jsonify(path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
