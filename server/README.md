# Lemma App Node Server

This folder contains a lightweight Node.js server exposing REST APIs for the `word_search` MySQL database.

## Quick Start
- Open a terminal in `lemma_app/server`:
  - `cd server`
- Copy and edit environment:
  - Windows: `copy .env.example .env`
  - macOS/Linux: `cp .env.example .env`
- Install deps and start:
  - `npm install`
  - `npm start`
- Dev mode with auto-reload:
  - `npm run dev`

## Port Configuration
- Edit `PORT` in `server/.env` (default `3000`).
- Example:
  - `PORT=4000`
- Then restart: `npm start`.

## Verify
- Health check: `http://localhost:3000/health` (or your configured port)
- List tables: `http://localhost:3000/tables`
- Rows: `http://localhost:3000/rows?limit=50`

## Environment Variables
- `PORT` — server port
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
- `TABLE_NAME` (optional) — force a specific `word_search_*` table