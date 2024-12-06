from flask import Flask, jsonify, send_from_directory
import json
from flask_cors import CORS
import os
from database import db, PathPerformance 

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
