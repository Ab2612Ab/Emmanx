# 🐍 Appointment Booking API

A real-world REST API built with **Python + FastAPI**, designed to demonstrate backend engineering skills on GitHub.

## What this project demonstrates

- Python backend development
- FastAPI REST APIs
- Pydantic request validation
- Email validation
- Appointment conflict detection
- Availability checking
- Appointment cancellation
- HTTP status codes and API error handling
- Automatic OpenAPI documentation
- CORS configuration
- Vercel serverless deployment

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | / | API information |
| GET | /health | Health check |
| GET | /services | Available services |
| GET | /availability | Check whether a time is free |
| POST | /appointments | Create an appointment |
| GET | /appointments | List appointments |
| GET | /appointments/{id} | Get one appointment |
| DELETE | /appointments/{id} | Cancel an appointment |
| GET | /docs | Interactive Swagger API docs |
| GET | /redoc | ReDoc API documentation |

## Example request

```json
{
  "customer_name": "Jane Doe",
  "customer_email": "jane@example.com",
  "service": "Website Review",
  "starts_at": "2030-06-20T14:00:00Z",
  "duration_minutes": 60
}
```

## Tech stack

**Python 3 · FastAPI · Pydantic · Vercel**

> Note: the current demo uses process memory for appointments so the repository can run without external infrastructure. For production, the storage layer should be replaced with PostgreSQL/Supabase, Redis, or another persistent datastore.

## Developer

Built by **Taiwo Emmanuel — Web Designer & Full-Stack Developer**.

The project intentionally uses Python as the backend so visitors can inspect a complete Python API implementation directly in the repository.
