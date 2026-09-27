# Job Application Tracker API

A practical **Python + FastAPI** backend for managing a job search pipeline.

It lets a user record applications, track their status, store recruiter/contact details, schedule follow-ups, and view a simple application dashboard.

## Features

- Create job applications
- Track status: applied, screening, interview, offer, rejected, withdrawn
- Filter applications by status or company
- View an individual application
- Update application status
- Delete applications
- Store job URLs, recruiter details, salary range, notes, and follow-up dates
- Dashboard statistics
- Email validation
- Input validation with Pydantic
- CORS support
- Health endpoint
- Swagger API documentation
- Automated tests
- Vercel-ready serverless configuration

## Python skills demonstrated

This project demonstrates:

- Python API development
- FastAPI
- Pydantic data models and validation
- Python enums
- Datetime/date handling
- REST API design
- Error handling
- In-memory data management
- Automated API testing

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | / | API information |
| GET | /health | Health check |
| POST | /applications | Create an application |
| GET | /applications | List/filter applications |
| GET | /applications/{id} | Get one application |
| PATCH | /applications/{id}/status | Change application status |
| DELETE | /applications/{id} | Delete an application |
| GET | /dashboard | Application pipeline statistics |

## Run locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn api.index:app --reload
```

Open Swagger:

```
http://127.0.0.1:8000/docs
```

Run tests:

```bash
pytest
```

## Example request

```json
{
  "company": "Acme Labs",
  "role": "Python Developer",
  "location": "Remote",
  "job_url": "https://example.com/jobs/python-developer",
  "contact_name": "Jane Recruiter",
  "contact_email": "jane@example.com",
  "status": "applied",
  "follow_up_date": "2026-10-05",
  "salary_min": 70000,
  "salary_max": 90000,
  "notes": "Follow up one week after applying."
}
```

## Deployment

The project includes a `vercel.json` configuration for deploying the FastAPI entry point on Vercel.

**Important:** the current version stores applications in memory. Serverless instances are not a persistent database. For a production application, replace the in-memory store with PostgreSQL, Supabase, or another durable database.

## Project structure

```text
job-application-tracker/
├── api/
│   └── index.py
├── tests/
│   └── test_api.py
├── requirements.txt
├── vercel.json
└── README.md
```
