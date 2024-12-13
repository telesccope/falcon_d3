
# Shortest Path Visualization Web Application

This project is a web application that visualizes the shortest path between points on a graph. The frontend uses HTML, CSS, and JavaScript (with D3.js for visualization), while the backend is built with Flask. The application supports multiple shortest path algorithms, including Dijkstra, A*, and Bellman-Ford.

## Project Structure

```
├── README.md
├── backend
│   ├── __pycache__/         # Compiled Python files (ignored in production)
│   ├── app.py               # Main Flask application
│   ├── create_history.py    # Script for generating historical data
│   ├── data/                # Directory containing graph data
│   ├── database.py          # Database connection and schema
│   ├── database_manager.py  # Helper functions for interacting with the database
│   ├── requirements.txt     # Python dependencies
│   ├── utils.py             # Utility functions for algorithms and data processing
│   └── venv/                # Virtual environment for Python dependencies
└── frontend
    ├── about.html           # About page
    ├── assets/              # Static assets (CSS, JS, images, etc.)
    ├── index.html           # Main page for selecting start and end points
    ├── results.html         # Page to display the shortest path results
    ├── select_algorithm.html # Page for selecting the algorithm
    ├── select_points.html   # Page for selecting points on the graph
    └── statistics.html      # Page for visualizing algorithm performance statistics
```

---

## Prerequisites

- Python 3.x
- A modern web browser (e.g., Chrome, Firefox, Edge)

---

## Setup

### Backend

1. **Navigate to the Backend Directory:**

    ```bash
    cd backend
    ```

2. **Set up Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Flask Application:**

    ```bash
    python app.py
    ```

    The backend server will run on `http://127.0.0.1:5000` by default.

5. **API Design**
# API Documentation

| **Endpoint**                                   | **Method** | **Description**                                                                                       | **Parameters**                                                                                                                                                                                                                           |
|------------------------------------------------|------------|-------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/`                                            | GET        | Serves the frontend index page.                                                                       | None                                                                                                                                                                                                                                    |
| `/api/graph`                                   | GET        | Retrieves a list of all available graph IDs.                                                          | None                                                                                                                                                                                                                                    |
| `/api/graph/<graph_id>`                        | GET        | Retrieves the details of a specific graph by its ID.                                                  | - `graph_id` (string): The ID of the graph to retrieve.                                                                                                                                                                                |
| `/api/algorithms`                              | GET        | Retrieves a list of all supported shortest path algorithms.                                           | None                                                                                                                                                                                                                                    |
| `/api/shortest-path/<graph>/<algorithm>/<source>/<target>` | GET        | Calculates the shortest path between two nodes using the specified algorithm.                         | - `graph` (string): The graph ID to use. <br> - `algorithm` (string): The algorithm to use (`Dijkstra`, `A* (Euclidean)`, `A* (Manhattan)`, `BellmanFord`). <br> - `source` (string): Source node as "x,y". <br> - `target` (string): Target node as "x,y". |
| `/api/statistics`                              | GET        | Retrieves performance statistics for the algorithms from the database.                                | None                                                                                                                                                                                                                                    |

---

### Frontend

1. **Navigate to the Frontend Directory:**

    ```bash
    cd frontend
    ```

2. **Open the Application in a Browser:**

    Open `index.html` in your web browser to access the application.

---

## Frontend Stack

### HTML
- **Purpose**: Used for structuring the content of the page.

### CSS
- **Purpose**: Used for styling and layout of the page.

### JavaScript
- **Purpose**: Implements interactive functionality.

### D3.js
- **Purpose**: Used for drawing network graphs and data visualization.

## Backend Tech Stack

### Flask
- **Purpose**: A lightweight Python web framework used to build the backend API.

### SQLAlchemy
- **Purpose**: An ORM (Object-Relational Mapper) used for database management and interaction.

### SQLite
- **Purpose**: A lightweight database used to store performance and algorithm statistics.

### GeoPandas
- **Purpose**: A Python library used for handling geospatial data, specifically GeoJSON files.

### NetworkX
- **Purpose**: A Python library used for creating and analyzing graph structures.

---

### Design Suggestions
1. Use icons or logos for each library or tool to make the explanation visually appealing.
2. Create a flowchart or diagram to show how these technologies interact (e.g., Flask handles API requests, GeoPandas processes geospatial data, NetworkX computes graph algorithms, etc.).


---

### Design Suggestions
1. Add a small icon or a concise code snippet for each technology.
2. Use arrows or a flowchart to illustrate the collaboration between these technologies.

## Features

1. **Shortest Path Algorithms:**
   - Dijkstra
   - A* (with Manhattan and Euclidean heuristics)
   - Bellman-Ford

2. **Interactive Visualization:**
   - Visualize the graph and shortest paths using D3.js.

3. **Performance Statistics:**
   - Compare the performance of different algorithms in terms of time and steps.

4. **Customizable Graph:**
   - Load custom graph data from GeoJSON files.

---

## Development Notes

1. **Graph Data:**
   - The graph data is stored in the `backend/data` directory. Modify or replace the GeoJSON files to use custom graphs.

2. **Database:**
   - The application uses SQLite for storing historical results and statistics. The database schema is defined in `database.py`.

3. **Algorithm Implementation:**
   - The shortest path algorithms are implemented in the `utils.py` file.

---


## Acknowledgments

- [D3.js](https://d3js.org/) for interactive data visualization.
- [Flask](https://flask.palletsprojects.com/) for the backend framework.
- [NetworkX](https://networkx.org/) for graph algorithms and data structures.