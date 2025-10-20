# Reservation API

A RESTful API for managing reservations of rooms, places, and buildings.
The API is built with Django REST Framework, supports JWT authentication, uses Redis caching for location data, and comes with an interactive Swagger documentation.
Currently, it runs on an SQLite database (default development setup).

---

## Features

* **JWT Authentication** for secure login and access
* **Reservation management** (create, list, filter by user)
* **Location caching** with Redis for faster responses
* **Celery** for task queuing (in the moment, is set to only display the emails on terminal)
* **Interactive Swagger docs** (auto-generated API documentation)
* **Django Admin panel** for easy management
* **SQLite** database for development (will be changed to PostgreSQL soon)

---

## Tech Stack

* [Django](https://www.djangoproject.com/)
* [Django REST Framework](https://www.django-rest-framework.org/)
* [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
* [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/)
* [React](https://react.dev/)
* [Redis](https://redis.io/) (for caching)
* [Celery](https://docs.celeryq.dev/)
* [SQLite](https://www.sqlite.org/) (default DB)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/kaelkkd/reservation-system
cd reservation-system/reservation
```

### 2. Create a virtual environment & install dependencies

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

### 3. Run migrations

```bash
python manage.py migrate
```

### 4. Start Redis (Docker example)

```bash
docker run --name django-redis -d -p 6379:6379 redis
```

### 5. Start the development server

```bash
python manage.py runserver
```

### 6. Start Celery 
```bash
celery -A reservation worker --loglevel=INFO
```
If on Windows and the OS deny the acess
```bash
celery -A reservation worker --pool=solo -l info
```

### 7. Install front end dependencies

```bash
cd cd reservation-system/frontend
npm install
```

### 8. Start the front end server

```bash
npm run dev
```

---

## Authentication

The API uses **JWT** authentication.

### Obtain token

```http
POST /api/login/ HTTP/1.1
{
  "umail": "your_email",
  "password": "your_password"
}
```

### Refresh token

```http
POST /api/login/refresh/ HTTP/1.1
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

Once the server is running, you can access interactive Swagger documentation at:

* Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

---

## Example Endpoints

### Profiles
* `GET /api/profiles/me` → returns user profile
* `PUT /api/profiles/me` → update the user profile
  ```json
  {
    "country": "UK",
    "address_line": "Main Avenue, 112",
    "display_name": "UK User",
    "bio": "First user from the UK!"
  }
  ```

### Locations

* `GET /api/locations/` → list all locations
* `GET /api/locations/{id}/` → retrieve location details (cached in Redis)

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

The project includes the default Django admin interface.
Access it at: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## Running Tests

```bash
python manage.py test
```

---

## Roadmap

* [x] Add automated tests
* [x] Add user roles & permissions (admin vs normal user)
* [x] Reservation conflict checks
* [x] Add a React frotnend
* [ ] Switch database to PostgreSQL
* [ ] Extend Swagger docs with examples




