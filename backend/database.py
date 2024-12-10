from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Node(db.Model):
    __tablename__ = 'node'
    
    NodeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255), nullable=False)
    Coordinates = db.Column(db.String(255), nullable=False)  # Assuming point is stored as a string

    def __repr__(self):
        return f'<Node {self.Name}>'


class Edge(db.Model):
    __tablename__ = 'edge'
    
    EdgeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SourceNodeID = db.Column(db.Integer, db.ForeignKey('node.NodeID'), nullable=False)
    DestinationNodeID = db.Column(db.Integer, db.ForeignKey('node.NodeID'), nullable=False)
    Distance = db.Column(db.Float, nullable=False)
    Bidirectional = db.Column(db.Boolean, nullable=False)

    source_node = db.relationship('Node', foreign_keys=[SourceNodeID])
    destination_node = db.relationship('Node', foreign_keys=[DestinationNodeID])

    def __repr__(self):
        return f'<Edge {self.SourceNodeID} to {self.DestinationNodeID}>'


class Heuristic(db.Model):
    __tablename__ = 'heuristic'
    
    HeuristicID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SourceNodeID = db.Column(db.Integer, db.ForeignKey('node.NodeID'), nullable=False)
    DestinationNodeID = db.Column(db.Integer, db.ForeignKey('node.NodeID'), nullable=False)
    HeuristicValue = db.Column(db.Float, nullable=False)

    source_node = db.relationship('Node', foreign_keys=[SourceNodeID])
    destination_node = db.relationship('Node', foreign_keys=[DestinationNodeID])

    def __repr__(self):
        return f'<Heuristic from {self.SourceNodeID} to {self.DestinationNodeID}>'
