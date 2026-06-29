# Travel Planner API

A RESTful API for managing travel projects and places using the [Art Institute of Chicago API](https://api.artic.edu/docs/) collection as a destination library.

Built with **FastAPI** · **SQLite (async)** · **Docker**

---

## Features

- **Travel Projects** — Create, read, update, and delete projects (with visited-place protection on delete)
- **Project Places** — Import artworks from the Art Institute of Chicago API; add notes; mark places as visited
- **Auto-completion** — A project is automatically marked as completed when all its places are visited
- **OpenAPI Documentation** — Auto-generated interactive API documentation at `/docs`
- **Docker Support** — Run the application with a single command

---

# Quick Start

## Option 1 — Docker

```bash
# 1. Clone the repository
git clone <repo-url>
cd travel_planner

# 2. Build the Docker image
docker build -t travel-planner .

# 3. Run the container
docker run -d -p 8000:8000 travel-planner
```

The API will be available at:

- **API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs

---

## Option 2 — Local Python

```bash
# Python 3.11+ required

python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

- **API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs

---

# API Reference

## Travel Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/projects/` | Create a new project (optionally with places) |
| `GET` | `/projects/` | List all projects |
| `GET` | `/projects/{id}` | Retrieve a project with all its places |
| `PATCH` | `/projects/{id}` | Update project name, description, or start date |
| `DELETE` | `/projects/{id}` | Delete a project (blocked if visited places exist) |

---

## Project Places

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/projects/{id}/places/` | Add a place (validated against the Art Institute API) |
| `GET` | `/projects/{id}/places/` | List project places |
| `GET` | `/projects/{id}/places/{pid}` | Retrieve a single place |
| `PATCH` | `/projects/{id}/places/{pid}` | Update notes or mark a place as visited |

---

# Project Structure

```text
travel_planner/
├── app/
│   ├── api/          # API routers (projects.py, places.py)
│   ├── db/           # Database configuration
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Art Institute API client (artic.py)
│   └── main.py       # FastAPI application entry point
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# Business Rules

- A project can contain **1–10 places**.
- A project **cannot be deleted** if any of its places are marked as **visited**.
- Adding an artwork that does not exist in the Art Institute of Chicago API returns **HTTP 400 Bad Request**.
- The same artwork cannot be added to the same project more than once.
- When **all places** in a project are marked as visited, the project is automatically updated with:

```python
is_completed = True
```

---

# Tech Stack

| Layer | Technology |
|------|------------|
| Framework | FastAPI |
| Database | SQLite (Async SQLAlchemy 2.0) |
| HTTP Client | httpx (async) |
| Validation | Pydantic v2 |
| ASGI Server | Uvicorn |

---

# Future Improvements

- User authentication
- Search and filtering
- Pagination
- PostgreSQL support
- Unit and integration tests
- CI/CD pipeline

---

# License

This project was created for educational purposes.