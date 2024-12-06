from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PathPerformance(db.Model):
    __tablename__ = 'path_performance'
    
    id = db.Column(db.Integer, primary_key=True)
    start_node = db.Column(db.String(64), nullable=False)
    end_node = db.Column(db.String(64), nullable=False)
    algorithm = db.Column(db.String(64), nullable=False)
    steps = db.Column(db.Integer, nullable=False)
    execution_time = db.Column(db.Float, nullable=False)  # Time in seconds
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PathPerformance {self.algorithm} from {self.start_node} to {self.end_node}>'
