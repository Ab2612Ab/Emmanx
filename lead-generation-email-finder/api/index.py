import ipaddress
import re
import socket
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(
    title="Lead Generation & Email Finder API",
    version="1.0.0",
    description="Advanced Python API for public lead discovery, contact extraction, email pattern generation, validation, and lead scoring.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

EMAIL_RE = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}\b")
GENERIC_PREFIXES = {"info", "hello", "contact", "sales", "support", "admin", "office", "team", "careers", "jobs", "hr"}

class CompanyLeadRequest(BaseModel):
    website: str = Field(min_length=4, max_length=500)
    company: Optional[str] = Field(default=None, max_length=160)
    industry: Optional[str] = Field(default=None, max_length=120)
    location: Optional[str] = Field(default=None, max_length=160)

class PersonRequest(BaseModel):
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    domain: str = Field(min_length=3, max_length=160)

class EmailVerificationRequest(BaseModel):
    email: EmailStr

class LeadScoreRequest(BaseModel):
    company: str = Field(min_length=1, max_length=160)
    website: Optional[str] = None
    email: Optional[EmailStr] = None
    job_title: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[int] = Field(default=None, ge=1)
    location: Optional[str] = None

class BulkPersonRequest(BaseModel):
    people: list[PersonRequest] = Field(min_length=1, max_length=100)

def normalize_domain(value: str) -> str:
    raw = value.strip()
    if "://" not in raw:
        raw = "https://" + raw
    parsed = urlparse(raw)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise HTTPException(status_code=422, detail="Provide a valid public HTTP/HTTPS website")
    return parsed.hostname.lower().rstrip(".")

def assert_public_host(host: str) -> None:
    try:
        addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    except socket.gaierror:
        raise HTTPException(status_code=422, detail="Website host could not be resolved")
    for item in addresses:
        ip = ipaddress.ip_address(item[4][0])
        if not ip.is_global:
            raise HTTPException(status_code=400, detail="Private or local network targets are not allowed")

def fetch_public_page(website: str) -> tuple[str, str]:
    domain = normalize_domain(website)
    assert_public_host(domain)
    url = "https://" + domain
    try:
        response = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "LeadResearchBot/1.0 (+public-business-research)"},
            allow_redirects=True,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"Could not fetch public website: {exc.__class__.__name__}")
    final_domain = normalize_domain(response.url)
    assert_public_host(final_domain)
    return response.text[:2_000_000], final_domain

def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())

def email_patterns(first: str, last: str, domain: str) -> list[str]:
    f, l = slug(first), slug(last)
    return [
        f"{f}.{l}@{domain}",
        f"{f}{l}@{domain}",
        f"{f[0]}{l}@{domain}",
        f"{f}@{domain}",
        f"{l}@{domain}",
    ]

def score_email(email: str, domain: str) -> int:
    local, host = email.lower().split("@", 1)
    score = 40 if host == domain.lower() else 10
    if local not in GENERIC_PREFIXES:
        score += 25
    if "." in local or len(local) > 3:
        score += 15
    if EMAIL_RE.fullmatch(email):
        score += 20
    return min(score, 100)

def title_score(title: str) -> int:
    senior = {"ceo", "founder", "owner", "director", "vp", "vice president", "head", "manager"}
    return 30 if any(term in title.lower() for term in senior) else 15

@app.get("/")
def root():
    return {
        "name": "Lead Generation & Email Finder API",
        "version": "1.0.0",
        "features": ["public contact extraction", "email pattern finder", "email scoring", "lead scoring", "bulk research"],
        "docs": "/docs",
        "health": "/health",
    }

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.post("/discover/company")
def discover_company(payload: CompanyLeadRequest):
    html, domain = fetch_public_page(payload.website)
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else None
    description_tag = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
    description = description_tag.get("content", "").strip() if description_tag else None
    text = soup.get_text(" ", strip=True)
    emails = sorted(set(EMAIL_RE.findall(html)), key=lambda e: (-score_email(e, domain), e))
    links = []
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()
        if href.startswith(("mailto:", "tel:")):
            links.append(href)
    return {
        "company": payload.company,
        "domain": domain,
        "industry": payload.industry,
        "location": payload.location,
        "title": title,
        "description": description,
        "public_emails": [{"email": e, "confidence": score_email(e, domain)} for e in emails[:50]],
        "contact_links": sorted(set(links))[:50],
        "page_text_preview": text[:500],
    }

@app.post("/find-email")
def find_email(payload: PersonRequest):
    domain = normalize_domain(payload.domain)
    candidates = email_patterns(payload.first_name, payload.last_name, domain)
    return {
        "person": f"{payload.first_name} {payload.last_name}",
        "domain": domain,
        "candidates": [
            {"email": email, "confidence": max(35, 80 - index * 8), "method": "common_company_pattern"}
            for index, email in enumerate(candidates)
        ],
        "note": "These are pattern-based candidates, not guaranteed mailbox verification.",
    }

@app.post("/find-email/bulk")
def find_email_bulk(payload: BulkPersonRequest):
    return {"results": [find_email(person) for person in payload.people]}

@app.post("/verify-email")
def verify_email(payload: EmailVerificationRequest):
    email = str(payload.email).lower()
    domain = email.split("@", 1)[1]
    try:
        mx_records = socket.getaddrinfo(domain, 25, type=socket.SOCK_STREAM)
        has_mx_host = bool(mx_records)
    except socket.gaierror:
        has_mx_host = False
    return {
        "email": email,
        "syntax_valid": bool(EMAIL_RE.fullmatch(email)),
        "domain": domain,
        "domain_resolves": has_mx_host,
        "deliverability": "unknown",
        "warning": "This endpoint does not send mail or claim that a mailbox exists.",
    }

@app.post("/score-lead")
def score_lead(payload: LeadScoreRequest):
    score = 0
    reasons = []
    if payload.website:
        score += 20
        reasons.append("Website supplied")
    if payload.email:
        score += 20
        reasons.append("Public contact email supplied")
    if payload.job_title:
        points = title_score(payload.job_title)
        score += points
        reasons.append("Decision-maker or senior title" if points == 30 else "Job title supplied")
    if payload.industry:
        score += 10
        reasons.append("Industry supplied")
    if payload.location:
        score += 10
        reasons.append("Location supplied")
    if payload.company_size:
        score += 10
        reasons.append("Company size supplied")
    return {
        "company": payload.company,
        "score": min(score, 100),
        "grade": "A" if score >= 80 else "B" if score >= 60 else "C" if score >= 40 else "D",
        "signals": reasons,
        "interpretation": "Higher score means more complete and actionable lead data; it is not a prediction of conversion.",
    }

@app.get("/extract-emails")
def extract_emails(website: str = Query(min_length=4, max_length=500)):
    html, domain = fetch_public_page(website)
    emails = sorted(set(EMAIL_RE.findall(html)))
    return {
        "domain": domain,
        "count": len(emails),
        "emails": [
            {"email": email, "type": "generic" if email.split("@")[0].lower() in GENERIC_PREFIXES else "named_or_other"}
            for email in emails[:100]
        ],
    }
