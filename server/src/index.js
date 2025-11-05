const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const mysql = require('mysql2/promise');

dotenv.config();

const PORT = parseInt(process.env.PORT || '3000', 10);
const DB_HOST = process.env.DB_HOST || '121.4.251.254';
const DB_PORT = parseInt(process.env.DB_PORT || '5034', 10);
const DB_USER = process.env.DB_USER || 'root';
const DB_PASSWORD = process.env.DB_PASSWORD || 'root';
const DB_NAME = process.env.DB_NAME || 'word_search';
const TABLE_NAME_OVERRIDE = process.env.TABLE_NAME || null;

const pool = mysql.createPool({
  host: DB_HOST,
  port: DB_PORT,
  user: DB_USER,
  password: DB_PASSWORD,
  database: DB_NAME,
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
});

async function getLatestTableName() {
  // Prefer INFORMATION_SCHEMA with a stable alias; fallback to SHOW TABLES
  const [rows] = await pool.query(
    "SELECT TABLE_NAME AS name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = ? AND TABLE_NAME LIKE 'word_search_%' ORDER BY TABLE_NAME DESC LIMIT 1",
    [DB_NAME]
  );
  if (rows && rows[0] && rows[0].name) return rows[0].name;
  // Fallback: SHOW TABLES LIKE (column name is dynamic); map values only
  const [showRows] = await pool.query("SHOW TABLES LIKE 'word_search_%'");
  const names = Array.isArray(showRows)
    ? showRows.map(r => Object.values(r)[0]).filter(Boolean)
    : [];
  return names.sort().reverse()[0] || null;
}

async function resolveTableName(query) {
  if (TABLE_NAME_OVERRIDE) return TABLE_NAME_OVERRIDE;
  if (query && query.table) return String(query.table);
  if (query && query.date) return `word_search_${String(query.date)}`;
  return await getLatestTableName();
}

async function getColumns(table) {
  const [rows] = await pool.query(
    'SELECT COLUMN_NAME FROM information_schema.columns WHERE table_schema = ? AND table_name = ?',
    [DB_NAME, table]
  );
  return rows.map(r => r.COLUMN_NAME);
}

const app = express();
app.use(cors());
app.use(express.json({ limit: '1mb' }));

app.get('/health', async (req, res) => {
  let db = 'down';
  try {
    const [rows] = await pool.query('SELECT 1 AS ok');
    if (rows && rows[0] && rows[0].ok === 1) db = 'up';
  } catch (e) {
    // leave db="down"
  }
  res.json({ status: 'ok', port: PORT, db });
});

app.get('/tables', async (req, res) => {
  try {
    const [rows] = await pool.query(
      "SELECT TABLE_NAME AS name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = ? AND TABLE_NAME LIKE 'word_search_%' ORDER BY TABLE_NAME DESC",
      [DB_NAME]
    );
    let tables = rows.map(r => r.name).filter(Boolean);
    if (!tables.length) {
      const [showRows] = await pool.query("SHOW TABLES LIKE 'word_search_%'");
      tables = Array.isArray(showRows)
        ? showRows.map(r => Object.values(r)[0]).filter(Boolean)
        : [];
      tables.sort().reverse();
    }
    res.json({ tables });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/rows', async (req, res) => {
  try {
    const table = await resolveTableName(req.query);
    if (!table) return res.status(404).json({ error: 'No word_search_* table found' });
    const limit = Math.min(parseInt(req.query.limit || '50', 10), 200);
    const offset = parseInt(req.query.offset || '0', 10);
    const [rows] = await pool.query(`SELECT * FROM \`${table}\` LIMIT ? OFFSET ?`, [limit, offset]);
    res.json({ table, limit, offset, rows });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/rows/:id', async (req, res) => {
  try {
    const table = await resolveTableName(req.query);
    if (!table) return res.status(404).json({ error: 'No table found' });
    const id = parseInt(req.params.id, 10);
    const [rows] = await pool.query(`SELECT * FROM \`${table}\` WHERE id = ?`, [id]);
    if (!rows.length) return res.status(404).json({ error: 'Not found' });
    res.json({ table, row: rows[0] });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/search', async (req, res) => {
  try {
    const table = await resolveTableName(req.query);
    if (!table) return res.status(404).json({ error: 'No table found' });
    const q = String(req.query.q || req.query.lemma || '').trim();
    if (!q) return res.status(400).json({ error: 'Missing q or lemma' });
    const [rows] = await pool.query(`SELECT * FROM \`${table}\` WHERE \`Lemma\` LIKE ? LIMIT 50`, [`%${q}%`]);
    res.json({ table, q, rows });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/rows', async (req, res) => {
  try {
    const table = await resolveTableName(req.query);
    if (!table) return res.status(404).json({ error: 'No table found' });
    const allowed = await getColumns(table);
    const body = req.body || {};
    const cols = Object.keys(body).filter(k => allowed.includes(k) && k !== 'id');
    if (!cols.length) return res.status(400).json({ error: 'No valid columns in body' });
    const values = cols.map(c => body[c]);
    const colSql = cols.map(c => `\`${c}\``).join(', ');
    const placeholders = cols.map(() => '?').join(', ');
    const sql = `INSERT INTO \`${table}\` (${colSql}) VALUES (${placeholders})`;
    const [result] = await pool.query(sql, values);
    const [rows] = await pool.query(`SELECT * FROM \`${table}\` WHERE id = ?`, [result.insertId]);
    res.status(201).json({ table, id: result.insertId, row: rows[0] });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.put('/rows/:id', async (req, res) => {
  try {
    const table = await resolveTableName(req.query);
    if (!table) return res.status(404).json({ error: 'No table found' });
    const allowed = await getColumns(table);
    const body = req.body || {};
    const cols = Object.keys(body).filter(k => allowed.includes(k) && k !== 'id');
    if (!cols.length) return res.status(400).json({ error: 'No valid columns in body' });
    const values = cols.map(c => body[c]);
    const setSql = cols.map(c => `\`${c}\` = ?`).join(', ');
    const id = parseInt(req.params.id, 10);
    const sql = `UPDATE \`${table}\` SET ${setSql} WHERE id = ?`;
    const [result] = await pool.query(sql, [...values, id]);
    res.json({ table, updated: result.affectedRows });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.delete('/rows/:id', async (req, res) => {
  try {
    const table = await resolveTableName(req.query);
    if (!table) return res.status(404).json({ error: 'No table found' });
    const id = parseInt(req.params.id, 10);
    const [result] = await pool.query(`DELETE FROM \`${table}\` WHERE id = ?`, [id]);
    res.json({ table, deleted: result.affectedRows });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});