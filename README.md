# CampusOS

**AI-powered campus operations platform** — ticket management, resource booking, and a document-grounded AI assistant, built with FastAPI, React, PostgreSQL (pgvector), Redis, and Docker.

![CI](https://github.com/PraveshRathore668/CampusOS/actions/workflows/tests.yml/badge.svg)

## What it does

CampusOS digitizes common university operations:

- **Tickets** — students submit maintenance/IT complaints; a trained ML model (TF-IDF + Logistic Regression) automatically predicts category and priority
- **Booking** — students reserve labs, rooms, and facilities, with database-level double-booking prevention (PostgreSQL unique constraint, not application-level checks)
- **AI Assistant** — a Retrieval-Augmented Generation (RAG) chatbot that answers student questions grounded in uploaded campus documents, with source citations, using pgvector for semantic search and Gemini for generation
- **Role-based access** — STUDENT / FACULTY / ADMIN roles with JWT authentication and route-level authorization

## Tech stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, SQLAlchemy, PostgreSQL + pgvector |
| Auth | JWT (access/refresh tokens), bcrypt password hashing |
| ML | scikit-learn (TF-IDF + Logistic Regression), sentence-transformers |
| RAG | pgvector similarity search, Google Gemini API |
| Caching | Redis |
| Frontend | React, React Router, Axios |
| Infra | Docker Compose, GitHub Actions CI |
| Testing | pytest (16 tests: auth, tickets, booking) |

## Architecture

```
React Frontend (nginx)
        │
        ▼
FastAPI Backend ──────► Redis (caching)
        │
        ▼
PostgreSQL + pgvector
  (users, tickets, bookings, documents, embeddings)
```

## Running locally with Docker

```bash
git clone https://github.com/PraveshRathore668/CampusOS.git
cd CampusOS
cp .env.example .env   # fill in your own secrets
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend API docs: http://localhost:8000/docs

## Running tests

```bash
pip install -r requirements.txt
python3 -m pytest tests/ -v
```

Tests run automatically on every push via GitHub Actions (see badge above).

## Key engineering decisions

- **Double-booking prevention** is enforced with a PostgreSQL `UNIQUE` constraint rather than an application-level availability check, avoiding the race condition where two simultaneous requests both pass a check before either commits.
- **AI classification is a fallback, not an override** — if a student manually specifies a ticket's category/priority, that choice is respected; the model only fills in gaps.
- **RAG generation is provider-agnostic by design** — the LLM call is isolated behind a single function interface, so switching providers only requires changing one file.
- **Redis caching** on read-heavy endpoints measured a ~74x speedup (201ms → 2.7ms) on cached responses.

## Project structure

```
app/
  models/    — SQLAlchemy table definitions
  schemas/   — Pydantic request/response shapes
  api/       — route handlers by feature
  core/      — auth, JWT, caching utilities
  ml/        — ticket classifier training + inference
  rag/       — embeddings, chunking, retrieval, generation
frontend/    — React application
tests/       — pytest suite
.github/workflows/ — CI pipeline
```

## Status

Actively developed as a portfolio project. Days 1–7 of an 8-day build plan are complete (backend, auth, ML classification, RAG, frontend, Docker, testing/CI); deployment is in progress.
