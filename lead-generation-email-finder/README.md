# Lead Generation & Email Finder API

An advanced **Python + FastAPI** prospecting backend for researching publicly available business contact information, generating likely company email patterns, validating email syntax/domain signals, scoring lead completeness, and processing bulk contact candidates.

## What this project demonstrates

- Python backend engineering
- FastAPI REST API architecture
- Pydantic validation
- Public website crawling
- HTML parsing with BeautifulSoup
- Email extraction with regular expressions
- Domain normalization
- Public-host/SSRF protection
- Email-pattern generation
- Lead scoring
- Bulk processing
- Financial-grade structured JSON responses
- Error handling and timeouts
- Automated API tests
- Vercel serverless configuration

## Core features

### 1. Public company discovery

`POST /discover/company`

Accepts a public business website and extracts:

- Domain
- Page title
- Meta description
- Publicly exposed email addresses
- Public `mailto:` and `tel:` links
- Industry/location supplied by the researcher
- Small text preview

### 2. Email finder

`POST /find-email`

Given a person's first name, last name, and company domain, generates common business email patterns such as:

- first.last@domain
- firstlast@domain
- flast@domain
- first@domain
- last@domain

The API clearly labels these as candidates rather than verified mailboxes.

### 3. Bulk email finder

`POST /find-email/bulk`

Processes up to 100 supplied people in one request.

### 4. Email verification signals

`POST /verify-email`

Checks email syntax and domain-resolution signals without sending an email. It deliberately reports deliverability as **unknown** rather than falsely claiming that a mailbox exists.

### 5. Lead scoring

`POST /score-lead`

Scores how complete/actionable a lead record is based on supplied signals such as:

- Website
- Public email
- Job title
- Seniority signal
- Industry
- Location
- Company size

The score measures data completeness, not expected sales conversion.

### 6. Public email extraction

`GET /extract-emails?website=...`

Extracts email addresses visibly present in a public webpage.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | / | API information |
| GET | /health | Health check |
| POST | /discover/company | Analyze a public company website |
| POST | /find-email | Generate email candidates |
| POST | /find-email/bulk | Generate candidates in bulk |
| POST | /verify-email | Syntax/domain signals |
| POST | /score-lead | Score lead-data completeness |
| GET | /extract-emails | Extract public webpage emails |

## Run locally

```bash
pip install -r requirements.txt
uvicorn api.index:app --reload
pytest
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

## Responsible-use design

This project is designed around **public business information** and researcher-supplied professional data. It does not attempt to bypass authentication, access private databases, guess sensitive personal information, or send verification emails. Email-pattern results are explicitly candidates and should be independently verified before use.

The public website fetcher blocks private/local network targets to reduce SSRF risk and uses request timeouts.

## Production architecture

For a production lead platform, add:

- PostgreSQL/Supabase
- Authentication and workspace isolation
- Redis job queues
- Background crawling
- Rate limiting
- Provider adapters for licensed enrichment/verification APIs
- Domain and contact deduplication
- Search history
- CSV/CRM export
- Consent/suppression lists
- Audit logs
- Usage limits and billing
- GDPR/CCPA and applicable anti-spam compliance controls

## Important limitation

This portfolio implementation does not claim that a generated email address exists or is deliverable. It extracts only emails exposed by the public page and generates common business patterns. A production product should use an authorized email-verification/enrichment provider for stronger verification.
