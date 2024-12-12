from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Node(db.Model):
    __tablename__ = 'node'
    
    NodeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255), nullable=False)
    Coordinates = db.Column(db.String(255), nullable=False) 

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


class ShortestPathResult(db.Model):
    __tablename__ = 'shortest_path_result'
    
    ResultID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Algorithm = db.Column(db.String(255), nullable=False)
    StartNodeID = db.Column(db.Integer, db.ForeignKey('node.NodeID'), nullable=False)
    EndNodeID = db.Column(db.Integer, db.ForeignKey('node.NodeID'), nullable=False)
    Path = db.Column(db.Text, nullable=False)  
    TotalWeight = db.Column(db.Float, nullable=False)
    Steps = db.Column(db.Integer, nullable=False)
    Time = db.Column(db.Float, nullable=False)

    start_node = db.relationship('Node', foreign_keys=[StartNodeID])
    end_node = db.relationship('Node', foreign_keys=[EndNodeID])

    def __repr__(self):
        return f"<ShortestPathResult {self.Algorithm} from {self.StartNodeID} to {self.EndNodeID}>"
