# Project Name

This project is a web application that visualizes the shortest path using D3.js on the frontend and Flask on the backend.

## Project Structure

```
├── README.md
├── backend
│   ├── app.py
│   ├── data
│   ├── requirements.txt
│   └── venv
└── frontend
    ├── index.html
    ├── script.js
    └── style.css
```

## Prerequisites

- Python 3.x

## Setup

### Backend

1. **Navigate to the Backend Directory:**

    ```bash
    cd backend
    ```

2. **Set up Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `python` and `venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Flask Application:**

    ```bash
    python app.py
    ```

### Frontend

1. **Navigate to the Frontend Directory:**

    ```bash
    cd frontend
    ```

2. **Open `index.html` in a browser to view the application.**