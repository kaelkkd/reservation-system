# Reservation API

A RESTful API for managing reservations of rooms, places, and buildings.

The API is built with Django REST Framework, supports JWT authentication, uses Redis for caching, Celery for background tasks, and provides interactive Swagger documentation.
At the moment, the default development database is SQLite (with plans to migrate to PostgreSQL).

---

## Features

* **JWT Authentication** for secure login and access
* **Reservation management** (create, list, filter by user)
* **Location caching** with Redis for faster responses
* **Celery** for background task processing
  *(currently configured to display emails in the terminal)*
* **Interactive Swagger docs**
* **Django Admin panel**
* **SQLite** database for development

---

## Tech Stack

* [Django](https://www.djangoproject.com/)
* [Django REST Framework](https://www.django-rest-framework.org/)
* [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
* [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/)
* [React](https://react.dev/)
* [Redis](https://redis.io/) (caching)
* [Celery](https://docs.celeryq.dev/)
* [SQLite](https://www.sqlite.org/) (default DB)
* [Docker](https://www.docker.com/)

---

## Using with Docker (recommended)

### 1. Clone the repository

```bash
git clone https://github.com/kaelkkd/reservation-system
cd reservation-system/reservations
```

### 2. Setting up the containers
With Docker and compose installed, run
```bash
docker compose up -d --build
```

Once the containers are running, you can access:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Swagger UI: http://localhost:8000/swagger/
- Admin panel: http://localhost:8000/admin/

The Docker setup runs the following services:
- Django backend
- Celery worker
- Redis
- React frontend

## Running locally (using `uv`)

> This project uses **[`uv`](https://github.com/astral-sh/uv)** for dependency management and virtual environments.

### 1. Clone the repository

```bash
git clone https://github.com/kaelkkd/reservation-system
cd reservation-system/reservations
```
After cloning, create a `.env` file based on `.env.example`.

---

### 2. Create a virtual environment and install dependencies

```bash
uv venv
source .venv/bin/activate   #Linux and macOS
# .venv\Scripts\Activate.ps1  # Windows (PowerShell)

uv pip install -e .
```

This installs the project in editable mode, along with all dependencies defined in `pyproject.toml`.

---

### 3. Run migrations

```bash
python manage.py migrate
```

---

### 4. Start Redis with Docker (required for cache and celery)
Celery also uses Redis as a message broker, therefore redis must be running before starting Celery.

```bash
docker run --name django-redis -d -p 6379:6379 redis
```

---

### 5. Start the development server

```bash
python manage.py runserver
```

---

### 6. Start Celery

```bash
celery -A reservations worker --loglevel=INFO
```

If you are on Windows and the OS blocks multiprocessing:

```bash
celery -A reservations worker --pool=solo -l info
```

---

## Frontend Setup

### 7. Install frontend dependencies

```bash
cd reservation-system/frontend
npm install
```

---

### 8. Configure the API URL

Create a `.env` file in the frontend directory:

```env
VITE_API_URL="http://localhost:8000"
```

---

### 9. Start the frontend server

```bash
npm run dev
```

---

## Authentication

The API uses JWT authentication.

### Obtain token

```http
POST /api/login/
{
  "email": "your_email",
  "password": "your_password"
}
```

### Refresh token

```http
POST /api/login/refresh/
{
  "refresh": "your_refresh_token"
}
```

Include the token in requests:

```http
Authorization: Bearer <access_token>
```

---

## API Documentation

Once the backend server is running:

* Swagger UI:
[http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)

---

## Example Endpoints

### Profiles

* `GET /api/profiles/me` → retrieve user profile
* `PUT /api/profiles/me` → update profile

```json
{
  "country": "UK",
  "address_line": "Main Avenue, 112",
  "display_name": "UK User",
  "bio": "First user from the UK!"
}
```

---

### Locations

* `GET /api/locations/` → list all locations
* `GET /api/locations/{id}/` → retrieve location details
  *(cached using Redis)*

---

### Reservations

* `GET /api/reservations/` → list user reservations
* `POST /api/reservations/` → create a reservation

```json
{
  "location_id": 1,
  "start_date": "2025-10-01",
  "end_date": "2025-10-02",
  "number_of_people": 5
}
```

* `DELETE /api/reservations/{id}/` → cancel a reservation

---

## Admin Panel

The project includes Django’s built-in admin interface:

[http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## Running Tests

```bash
python manage.py test
```

---

## Roadmap

* [x] Automated tests
* [x] User roles & permissions
* [x] Reservation conflict checks
* [x] React frontend
* [ ] Switch database to PostgreSQL
* [ ] Extend Swagger documentation with examples

