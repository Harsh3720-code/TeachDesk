# ADR-0003: SQLAlchemy 2.0 (async) and Alembic for data access

- **Status:** Accepted
- **Date:** 2026-09-28
- **Decider:** Project owner

## Context

TeachDesk stores documents and their vector embeddings (pgvector), drafts and
their approval state, and an audit record of every request and model call, in
Postgres 16. The web layer is FastAPI, which is asynchronous. The schema will
change as each milestone lands, so changes must be versioned and repeatable.

## Options considered

1. **SQLAlchemy 2.0 with the async engine, plus Alembic.** Typed ORM models,
   first-class pgvector column type, versioned migrations, and non-blocking
   database I/O that matches FastAPI's execution model.
2. **SQLAlchemy 2.0 synchronous, plus Alembic.** Same modelling and migrations;
   simpler to debug, but database calls block and FastAPI must run those
   endpoints in a thread pool.
3. **psycopg 3 with raw SQL and plain SQL migrations.** Maximum control and no
   ORM layer, but more hand-written SQL, manual row mapping and a home-grown
   migration process.

## Decision

**Option 1 — SQLAlchemy 2.0 (async) with Alembic.**

- ORM models use SQLAlchemy 2.0 typed declarative mapping (`Mapped[...]`).
- The async engine uses an asyncio Postgres driver; the specific driver will be
  chosen when the database layer is built.
- Vector columns use the `pgvector` SQLAlchemy integration.
- Every schema change is an Alembic migration, reviewed in the pull request
  that needs it. The application never creates tables implicitly.

## Consequences

- Database code must be async end to end; blocking calls inside request
  handlers are defects.
- Tests need an async-capable setup and a real Postgres with pgvector rather
  than SQLite, because vector search cannot be emulated faithfully.
- Alembic autogenerate output is a starting point only and is always reviewed
  by hand, particularly for vector indexes and extensions.
