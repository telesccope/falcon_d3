
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

---

### Frontend

1. **Navigate to the Frontend Directory:**

    ```bash
    cd frontend
    ```

2. **Open the Application in a Browser:**

    Open `index.html` in your web browser to access the application.

---

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