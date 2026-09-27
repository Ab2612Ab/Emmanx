# 🐍 Python Website SEO Analyzer

A real-world SEO auditing REST API built with **Python + FastAPI + BeautifulSoup**.

## What it demonstrates
- Python backend development
- FastAPI REST APIs
- HTML parsing with BeautifulSoup
- HTTP requests and website fetching
- SEO metadata analysis
- H1 structure checks
- Image alt-text checks
- HTTPS and viewport checks
- Canonical URL detection
- Automated scoring and recommendations
- Pydantic validation
- Vercel serverless deployment

## API
- GET / — API information
- GET /health — health check
- POST /analyze — analyze a public website
- GET /docs — interactive Swagger documentation

## Example
POST /analyze
```json
{"url":"https://example.com"}
```

The analyzer returns an SEO score, individual checks, detected page metadata, and actionable recommendations.

## Tech stack
**Python 3 · FastAPI · BeautifulSoup · Requests · Pydantic · Vercel**

This project intentionally uses Python for the analysis engine so GitHub visitors can inspect a practical Python backend rather than a toy script.

## Production note
The current version performs live analysis without storing user data. A production expansion could add authentication, PostgreSQL/Supabase history, scheduled audits, Lighthouse integration, and PDF reports.
