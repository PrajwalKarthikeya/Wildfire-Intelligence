# Phase 7 Journey Journal: The API Backend

Up until now, our data has been locked inside a database and some local files. Our analytics were just printing to the terminal. To build a true web application (the dashboard), we needed a way for a website to ask for that data securely.

---

## 🧑‍🏫 Layman's Terms

Imagine our database is a giant library filled with millions of files. The web dashboard (the user interface) is a person standing outside the library. The person isn't allowed to just run inside and start grabbing files—they might mess things up, or accidentally look at our secret NASA passwords!

Instead, we built a **Librarian** (the API). 
When the website wants to know where the fires are, it asks the Librarian: *"Hey, can I get the latest fires?"* (`GET /fires/latest`). The Librarian goes into the database, safely grabs exactly what was asked for, formats it nicely, and hands it back out.

We built a super-fast Librarian using **FastAPI**. It is now actively running in the background, serving up our fire data, our ML risk maps, and our historical analytics to anyone who asks for it.

---

## 👩‍💻 Technical Terms

In Phase 7, we decoupled our frontend from our data persistence layer by building a robust REST API using **FastAPI** and **Uvicorn**.

### 1. Security & Architecture
*   **Action**: Created `backend/main.py`.
*   **Security**: By routing all data requests through FastAPI, the frontend never handles the `FIRMS_MAP_KEY` or the PostgreSQL/SQLite `DATABASE_URL`.
*   **CORS**: Implemented Cross-Origin Resource Sharing (CORS) middleware to ensure our future Next.js frontend (Phase 9) can legally request data from the API domain without browser blocking.

### 2. Endpoints Implemented
We built exactly what the architectural roadmap specified:
*   `GET /`: Health check endpoint.
*   `GET /fires/latest`: Queries the `fire_detections` table and returns the most recent detections as JSON.
*   `GET /fires/history`: Runs a SQL aggregation (grouping by hour) and returns the temporal distribution.
*   `GET /fires/clusters`: Runs a fast spatial aggregation to return the densest fire coordinates.
*   `GET /risk`: Reads and serves the `risk_grid.geojson` file we generated in Phase 6, delivering the ML output directly to the map client.
*   `GET /risk/{lat}/{lon}`: Accepts spatial parameters, calculates the closest bounding grid cell, and returns the specific ML features (`temperature`, `humidity`, `risk_score`) for that exact location.
*   `GET /analytics`: Serves the aggregated total fires and maximum Fire Radiative Power (FRP).

### The Result
The FastAPI server is currently running as a daemon process on port `8001`. It effortlessly interfaces with the SQLAlchemy engine we built in Phase 2, proving that our modular architecture is paying off.
