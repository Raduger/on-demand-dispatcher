# init_db.py
# Initializes dispatcher.db with correct schema (SAFE & MATCHED)

import sqlite3

DB_NAME = "dispatcher.db"

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

# ---------------- REQUESTS TABLE ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    phone TEXT,
    canton TEXT,
    urgency TEXT,
    message TEXT,
    created_at TEXT NOT NULL,
    status TEXT DEFAULT 'Pending'
)
""")

# ---------------- ADMIN TABLE ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS admin (
    pin TEXT PRIMARY KEY
)
""")

# Default admin PIN
c.execute("""
INSERT OR IGNORE INTO admin (pin)
VALUES ('200170')
""")

# ---------------- DRIVERS TABLE ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS drivers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    available INTEGER DEFAULT 0
)
""")

# ---------------- COVERAGE TABLE ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS coverage (
    canton TEXT PRIMARY KEY,
    enabled INTEGER DEFAULT 1
)
""")

# ---------------- BLACKLIST TABLE ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS blacklist (
    company TEXT PRIMARY KEY
)
""")

# ---------------- WHITELIST TABLE ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS whitelist (
    company TEXT PRIMARY KEY
)
""")

# ---------------- OPTIONAL: SEED CANTONS ----------------
cantons = ["ZH","BE","LU","UR","SZ","OW","NW","GL","ZG","FR","SO","BS","BL","SH","AR","AI","SG","GR","AG","TG","TI","VD","VS","NE","GE","JU"]
for canton in cantons:
    c.execute("INSERT OR IGNORE INTO coverage (canton, enabled) VALUES (?, ?)", (canton, 1))

conn.commit()
conn.close()

print("✅ dispatcher.db initialized successfully with correct schema and cantons seeded")
