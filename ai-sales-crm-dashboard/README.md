# Pipeline AI — Sales CRM Dashboard

A polished React + TypeScript sales CRM interface designed as a portfolio-ready frontend.

## Features
- Responsive sales dashboard
- Revenue and activity charts
- Lead scoring and pipeline statuses
- Search/filter-ready lead table
- Add-lead workflow with AI enrichment guidance
- AI Sales Assistant drawer
- Overview, Leads, Companies, Opportunities, Activities and Analytics navigation
- Mobile sidebar and responsive layouts
- API-ready architecture

## Stack
React, TypeScript, Vite, Recharts, Lucide React.

## Run
npm install
npm run dev

The UI uses local typed demo data so it runs without secrets. Connect it to the existing Python lead-generation API in this repository through a VITE_API_URL service layer when the backend is deployed.

Recommended production upgrades: Supabase/PostgreSQL persistence, authentication/RBAC, real LLM integration, email sequencing, CSV import/export, activity timelines, server-side pagination and audit logs.
