# Resolve AI — Customer Support Agent Dashboard

Portfolio-ready React + TypeScript support operations dashboard.

## Features
- Agent inbox with status and priority filters
- Customer conversation workspace
- Public reply composer and AI draft action
- AI Support Copilot
- Ticket resolution analytics
- SLA-style priority queue
- Customers, Knowledge Base and Analytics modules
- Responsive agent workspace
- API-ready frontend

## Stack
React, TypeScript, Vite, Recharts, Lucide React.

## Run
npm install
npm run dev

The dashboard uses local demo data so it runs without secrets. It is designed to connect to the existing Python `ai-business-assistant-support-tickets` API through a frontend service layer.

Production upgrades: authentication/RBAC, PostgreSQL/Supabase, real LLM/RAG, email/live-chat webhooks, SLA escalation, attachments, audit logs and CSAT analytics.
