from database import Node, Edge, ShortestPathResult
from utils import insert_network_data
import json

class DatabaseManager:
    def __init__(self, db):
        self.db = db

    def add_node(self, name, coordinates):
        """Adds a new node to the database."""
        node = Node(Name=name, Coordinates=coordinates)
        self.db.session.add(node)
        self.db.session.commit()
        return node

    def add_edge(self, source_node_id, destination_node_id, distance, bidirectional):
        """Adds a new edge to the database."""
        edge = Edge(
            SourceNodeID=source_node_id,
            DestinationNodeID=destination_node_id,
            Distance=distance,
            Bidirectional=bidirectional
        )
        self.db.session.add(edge)
        self.db.session.commit()
        return edge

    def get_all_nodes(self):
        """Fetches all nodes from the database."""
        return Node.query.all()

    def get_all_edges(self):
        """Fetches all edges from the database."""
        return Edge.query.all()

    def get_node_by_id(self, node_id):
        """Fetches a node by its ID."""
        return self.db.session.get(Node, node_id)
    
    def get_node_by_coordinates(self, coordinates):
        """Fetches a node by its coordinates."""
        coord_str = f"{coordinates[0]},{coordinates[1]}"
        return Node.query.filter_by(Coordinates=coord_str).first()


    def get_edge_by_id(self, edge_id):
        """Fetches an edge by its ID."""
        return self.db.session.get(Edge, edge_id)

    def add_shortest_path_result(self, algorithm, start_node_id, end_node_id, path, total_weight, steps, time):
        """Adds a shortest path result to the database."""
        result = ShortestPathResult(
            Algorithm=algorithm,
            StartNodeID=start_node_id,
            EndNodeID=end_node_id,
            Path=json.dumps(path),  
            TotalWeight=total_weight,
            Steps=steps,
            Time=time
        )
        self.db.session.add(result)
        self.db.session.commit()
        return result

    def get_all_shortest_path_results(self):
        """Fetches all shortest path results from the database."""
        return ShortestPathResult.query.all()
    
    def get_statistics(self):
        from sqlalchemy.sql import func
        from sqlalchemy.orm import aliased

        results = (
            self.db.session.query(
                ShortestPathResult.Algorithm,
                func.count(ShortestPathResult.ResultID).label("total_records"),
                func.avg(ShortestPathResult.Steps).label("average_steps"),
                func.avg(func.length(ShortestPathResult.Path) - func.length(func.replace(ShortestPathResult.Path, ',', '')) + 1).label("average_path_length"), 
                func.avg(ShortestPathResult.Time).label("average_time"),
                func.avg(ShortestPathResult.TotalWeight).label("average_weight")  
            )
            .group_by(ShortestPathResult.Algorithm)
            .all()
        )

        statistics = [
            {
                "algorithm": result.Algorithm,
                "total_records": result.total_records,
                "average_steps": round(result.average_steps, 2) if result.average_steps else 0,
                "average_path_length": round(result.average_path_length, 2) if result.average_path_length else 0,
                "average_time": round(result.average_time, 4) if result.average_time else 0,
                "average_weight": round(result.average_weight, 3) if result.average_weight else 0,  
            }
            for result in results
        ]

        return statistics

    

if __name__ == '__main__':
    from app import db, app
    """
    import geopandas as gpd
    import json
    with app.app_context():
        db_manager = DatabaseManager(db)

        gdf = gpd.read_file('./data/graph/complete_graph.geojson')

        # 将 GeoDataFrame 转换为 GeoJSON 格式的字典
        geojson_data = json.loads(gdf.to_json())

        # 插入网络图数据
        insert_network_data(geojson_data, db_manager)
    """
    with app.app_context():
        db_manager = DatabaseManager(db)
        print(db_manager.get_statistics())
