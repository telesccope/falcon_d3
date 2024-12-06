from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app
from database import db, PathPerformance

class DatabaseManager:
    def __init__(self, db):
        self.db = db

    def add_performance(self, start_node, end_node, algorithm, steps, execution_time):
        performance = PathPerformance(
            start_node=start_node,
            end_node=end_node,
            algorithm=algorithm,
            steps=steps,
            execution_time=execution_time
        )
        self.db.session.add(performance)
        self.db.session.commit()
        return performance

    def get_all_performances(self):
        return PathPerformance.query.all()

    def get_performance_by_id(self, performance_id):
        return self.db.session.get(PathPerformance, performance_id)

    def get_performances_by_algorithm(self, algorithm):
        return PathPerformance.query.filter_by(algorithm=algorithm).all()

    def delete_performance(self, performance_id):
        performance = self.get_performance_by_id(performance_id)
        if performance:
            self.db.session.delete(performance)
            self.db.session.commit()
            return True
        return False

if __name__ == '__main__':
    with app.app_context():
        db_manager = DatabaseManager(db)

        # Add a new performance record
        new_performance = db_manager.add_performance(
            start_node='A',
            end_node='B',
            algorithm='Dijkstra',
            steps=10,
            execution_time=0.005
        )
        print(f'Added: {new_performance}')

        # Query all performances
        performances = db_manager.get_all_performances()
        for performance in performances:
            print(performance)

        # Query performances by algorithm
        dijkstra_performances = db_manager.get_performances_by_algorithm('Dijkstra')
        for performance in dijkstra_performances:
            print(performance)

        # Delete a performance
        success = db_manager.delete_performance(new_performance.id)
        print(f'Deletion successful: {success}')
