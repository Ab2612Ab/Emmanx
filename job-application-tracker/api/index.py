from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, EmailStr, Field

app = FastAPI(
    title="Job Application Tracker API",
    version="1.0.0",
    description="Python/FastAPI API for tracking job applications, interviews, offers, and follow-ups.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ApplicationStatus(str, Enum):
    applied = "applied"
    screening = "screening"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"
    withdrawn = "withdrawn"


class JobApplicationCreate(BaseModel):
    company: str = Field(min_length=1, max_length=120)
    role: str = Field(min_length=1, max_length=160)
    location: Optional[str] = Field(default=None, max_length=120)
    job_url: Optional[str] = Field(default=None, max_length=500)
    contact_name: Optional[str] = Field(default=None, max_length=120)
    contact_email: Optional[EmailStr] = None
    status: ApplicationStatus = ApplicationStatus.applied
    applied_date: date = Field(default_factory=date.today)
    follow_up_date: Optional[date] = None
    salary_min: Optional[int] = Field(default=None, ge=0)
    salary_max: Optional[int] = Field(default=None, ge=0)
    notes: Optional[str] = Field(default=None, max_length=5000)


class JobApplication(JobApplicationCreate):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime


class StatusUpdate(BaseModel):
    status: ApplicationStatus


applications: dict[str, JobApplication] = {}


def validate_salary(payload: JobApplicationCreate) -> None:
    if (
        payload.salary_min is not None
        and payload.salary_max is not None
        and payload.salary_min > payload.salary_max
    ):
        raise HTTPException(status_code=422, detail="salary_min cannot exceed salary_max")


@app.get("/")
def root():
    return {
        "name": "Job Application Tracker API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {"status": "ok", "applications": len(applications)}


@app.post("/applications", response_model=JobApplication, status_code=201)
def create_application(payload: JobApplicationCreate):
    validate_salary(payload)
    now = datetime.utcnow()
    application = JobApplication(
        id=str(uuid4()),
        created_at=now,
        updated_at=now,
        **payload.model_dump(),
    )
    applications[application.id] = application
    return application


@app.get("/applications", response_model=list[JobApplication])
def list_applications(
    status: Optional[ApplicationStatus] = None,
    company: Optional[str] = Query(default=None, max_length=120),
):
    results = list(applications.values())
    if status:
        results = [item for item in results if item.status == status]
    if company:
        needle = company.strip().lower()
        results = [item for item in results if needle in item.company.lower()]
    return sorted(results, key=lambda item: item.applied_date, reverse=True)


@app.get("/applications/{application_id}", response_model=JobApplication)
def get_application(application_id: str):
    application = applications.get(application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@app.patch("/applications/{application_id}/status", response_model=JobApplication)
def update_status(application_id: str, payload: StatusUpdate):
    application = applications.get(application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    application.status = payload.status
    application.updated_at = datetime.utcnow()
    applications[application_id] = application
    return application


@app.delete("/applications/{application_id}", status_code=204)
def delete_application(application_id: str):
    if application_id not in applications:
        raise HTTPException(status_code=404, detail="Application not found")
    del applications[application_id]


@app.get("/dashboard")
def dashboard():
    counts = {status.value: 0 for status in ApplicationStatus}
    for application in applications.values():
        counts[application.status.value] += 1

    total = len(applications)
    active = sum(
        counts[item]
        for item in ("applied", "screening", "interview", "offer")
    )
    response_rate = round(
        ((total - counts["applied"]) / total) * 100, 1
    ) if total else 0

    return {
        "total_applications": total,
        "active_applications": active,
        "response_rate_percent": response_rate,
        "by_status": counts,
    }
