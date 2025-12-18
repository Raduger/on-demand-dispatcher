# init_db.py
# Initializes dispatcher.db with correct schema and defaults
# init_db.py
# Updates dispatcher.db with full schema and companies

import sqlite3

DB_NAME = "dispatcher.db"
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

# ---------------- REQUESTS TABLE ----------------
# Add 'status' and 'assigned_driver' if missing
try:
    c.execute("ALTER TABLE requests ADD COLUMN status TEXT DEFAULT 'Pending'")
except sqlite3.OperationalError:
    pass  # Column already exists

try:
    c.execute("ALTER TABLE requests ADD COLUMN assigned_driver TEXT")
except sqlite3.OperationalError:
    pass  # Column already exists

# ---------------- DRIVERS TABLE ----------------
# Add 'canton' if missing
try:
    c.execute("ALTER TABLE drivers ADD COLUMN canton TEXT")
except sqlite3.OperationalError:
    pass  # Column already exists

# ---------------- COMPANIES TABLE ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
""")

# Insert all companies
all_companies = [
    "Planzer Holding AG",
    "Galliker Transport AG",
    "Kühne + Nagel (Schweiz) AG",
    "DB Schenker Schweiz AG",
    "Gebrüder Weiss AG",
    "Rhenus Logistics Schweiz AG",
    "CEVA Logistics Switzerland",
    "DSV Air & Sea AG",
    "Panalpina (DSV Panalpina)",
    "Gondrand International AG",
    "Welti-Furrer AG",
    "Schöni Transport AG",
    "F. Murpf AG",
    "Camion Transport AG",
    "Bertschi AG",
    "Emil Egger AG",
    "Karl Meyer AG",
    "Sieber Transport AG",
    "Post CH AG (Swiss Post Logistics)",
    "DPD (Schweiz) AG",
    "UPS SCS (Switzerland) GmbH",
    "FedEx Express Switzerland",
    "DHL Logistics (Schweiz) AG",
    "GLS Switzerland",
    "Quickmail AG",
    "Friderici Spécial SA",
    "Militzer & Münch Schweiz AG",
    "Hellmann Worldwide Logistics AG",
    "Nippon Express (Schweiz) AG"
]

for company in all_companies:
    c.execute("INSERT OR IGNORE INTO companies (name) VALUES (?)", (company,))

conn.commit()
conn.close()
print("✅ Database updated successfully with all companies and schema fixes!")
