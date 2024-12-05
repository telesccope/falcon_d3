from flask import Flask, jsonify
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    app.run(debug=True, port=5000)
