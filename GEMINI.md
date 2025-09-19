# GRIP - Global Resource Intelligence Platform

## Project Overview

GRIP (Global Resource Intelligence Platform) is a web application designed for analyzing and visualizing global commodity data. It provides a dashboard to monitor commodity prices, trends, and predictions. The project is composed of a React frontend and a Python/Flask backend.

### Key Technologies

*   **Frontend:** React, Vite, Tailwind CSS, Recharts, Framer Motion
*   **Backend:** Python, Flask, SQLAlchemy, pandas, scikit-learn, PyMuPDF

### Architecture

The application follows a client-server architecture:

*   **`grip-frontend`:** A React-based single-page application (SPA) that provides the user interface. It fetches data from the backend API and visualizes it using charts and interactive components.
*   **`grip-backend`:** A Flask-based web server that exposes a REST API. It handles data collection, processing, and analysis. The backend seems to be capable of extracting data from PDF files, likely from sources like the USGS (United States Geological Survey). It uses a database (likely SQLite, given the configuration) to store commodity data.
*   **`ui-goals`:** This directory contains React components that seem to be the target UI design. They are more advanced and feature-rich than the current frontend implementation.

## Building and Running

### Backend (`grip-backend`)

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the development server:**
    ```bash
    # TODO: Add the command to run the backend server.
    # It's likely one of the following:
    # flask run
    # python app.py
    ```

### Frontend (`grip-frontend`)

1.  **Install dependencies:**
    ```bash
    npm install
    ```

2.  **Run the development server:**
    ```bash
    npm run dev
    ```

## Development Conventions

*   The frontend uses ESLint for code linting.
*   The backend uses a `venv` for virtual environment management.
*   The project is organized into separate directories for the frontend and backend, which is a good practice for maintaining a clean codebase.
*   The `ui-goals` directory suggests a component-based approach to UI development, with a focus on reusability and modularity.
