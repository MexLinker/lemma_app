# Node.js REST API Documentation

## Overview
The Node.js server (under `server/`) provides a REST interface to the `word_search` MySQL database and its date-stamped tables (`word_search_YYYYMMDD`). It supports health checks, table discovery, CRUD operations, and query/search.

## Configuration
- Edit `server/.env` (copy from `.env.example`):
  - `PORT` — server port (default: `3000`)
  - `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` — MySQL connection settings
  - `TABLE_NAME` (optional) — Force a specific table name; otherwise newest table is used

## Table Resolution
- By default, the server selects the newest table: `SELECT table_name FROM information_schema.tables WHERE table_schema = ? AND table_name LIKE 'word_search_%' ORDER BY table_name DESC LIMIT 1`.
- You can override per-request using query params:
  - `?table=word_search_YYYYMMDD`
  - `?date=YYYYMMDD`
- Or globally using `TABLE_NAME` in `.env`.

## Endpoints

### GET `/health`
- Returns server and DB connectivity.
- Response:
```json
{ "status": "ok", "port": 3000, "db": "up" }
```

### GET `/tables`
- Lists available `word_search_*` tables (newest first).
- Response:
```json
{ "tables": ["word_search_20251105", "word_search_20251104", "..."] }
```

### GET `/rows`
- Returns paginated rows from the selected table.
- Query params:
  - `limit` (default `50`, max `200`)
  - `offset` (default `0`)
  - `date=YYYYMMDD` or `table=word_search_YYYYMMDD`
- Response:
```json
{
  "table": "word_search_20251105",
  "limit": 50,
  "offset": 0,
  "rows": [ { "id": 1, "Lemma": "...", "...": "..." } ]
}
```

### GET `/rows/:id`
- Fetch a single row by primary key `id`.
- Optional query: `date` or `table`.
- Responses:
  - `200` with `{ table, row }`
  - `404` if not found

### GET `/search`
- Search by `Lemma` column (case-insensitive LIKE).
- Query params:
  - `q` or `lemma` — search string
  - Optional `date` or `table`
- Response:
```json
{ "table": "word_search_20251105", "q": "deficit", "rows": [ { ... } ] }
```

### POST `/rows`
- Insert a new row.
- Body: JSON with keys matching valid table columns (except `id`).
- Valid column names are verified via `information_schema.columns` before composing SQL.
- Response:
  - `201` with `{ table, id, row }` (inserted row)
  - `400` for invalid/missing columns

### PUT `/rows/:id`
- Update fields of an existing row.
- Body: JSON with keys matching valid table columns (except `id`).
- Response:
  - `200` with `{ table, updated: <count> }`
  - `400` for invalid body

### DELETE `/rows/:id`
- Delete a row by `id`.
- Response:
  - `200` with `{ table, deleted: <count> }`

## Examples

### List tables
```
GET http://localhost:3000/tables
```

### Get first 50 rows from latest table
```
GET http://localhost:3000/rows?limit=50
```

### Search by lemma
```
GET http://localhost:3000/search?q=inflation
```

### Insert a row
```
POST http://localhost:3000/rows
Content-Type: application/json

{ "Lemma": "example", "Summary": "demo" }
```

### Update a row
```
PUT http://localhost:3000/rows/123
Content-Type: application/json

{ "Summary": "updated text" }
```

### Delete a row
```
DELETE http://localhost:3000/rows/123
```

## Notes
- Column names may include spaces or punctuation (e.g., `meet?`, `The Dark Forest -- Cixin Liu.epub`). The server escapes them safely when building SQL.
- All text columns are stored as `VARCHAR(1000)`; large payloads should be kept within that limit.
- For best performance, use pagination and targeted searches.