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

## Node Version Notes
- Recommended: Node.js LTS `18` or `20`. Minimum: `14`.
- Check your version: `node -v` and `npm -v`.
- If you see syntax errors (e.g., optional chaining `?.`), upgrade Node.

### Ubuntu Upgrade Options
- nvm (per-user):
  - `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash`
  - `source ~/.bashrc`
  - `nvm install 20 && nvm use 20`
- NodeSource (system-wide):
  - `curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -`
  - `sudo apt-get install -y nodejs`

### Override Port Without .env
- Linux/macOS: `PORT=4000 npm start`
- Windows (PowerShell): `set PORT=4000 && npm start`

## Run in Background (nohup)
Use `nohup` to keep the server running after logout. Create a `logs/` directory first.

### npm start via nohup
```
mkdir -p logs
nohup npm start > logs/server.out 2> logs/server.err < /dev/null & echo $! > server.pid
```
- Stop: `kill $(cat server.pid) && rm -f server.pid`
- Tail logs: `tail -f logs/server.out` (stdout), `tail -f logs/server.err` (stderr)

### node directly via nohup
```
mkdir -p logs
nohup node src/index.js > logs/node.out 2> logs/node.err < /dev/null & echo $! > node.pid
```
- Stop: `kill $(cat node.pid) && rm -f node.pid`

### Inline port override (nohup)
- Using `.env`: as configured
- Override inline: `nohup env PORT=5035 npm start > logs/server.out 2>&1 < /dev/null & echo $! > server.pid`

### Health check
```
curl -s http://localhost:3000/health  # or your PORT
```