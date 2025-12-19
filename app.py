import streamlit as st
import sqlite3
import datetime
import os

# ---------------- CONFIG ----------------
DB_NAME = "dispatcher.db"
APP_TITLE = "On-Demand Dispatcher"
LOGO_PATH = "truck.jpeg"

COMPANIES = [
    "A", "B", "C", "D", "E", "F", "G", "I", "M", "S"
]

LANGUAGES = ["EN", "DE", "FR", "IT"]

# ---------------- DB CONNECTION ----------------
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
c = conn.cursor()

# ---------------- DB SCHEMA ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    phone TEXT NOT NULL,
    canton TEXT NOT NULL,
    urgency TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TEXT,
    status TEXT DEFAULT 'Pending',
    assigned_driver TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS drivers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    canton TEXT NOT NULL,
    available INTEGER DEFAULT 0
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS admin (
    pin TEXT PRIMARY KEY
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS coverage (
    canton TEXT PRIMARY KEY,
    enabled INTEGER DEFAULT 1
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS blacklist (
    company TEXT PRIMARY KEY
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS whitelist (
    company TEXT PRIMARY KEY
)
""")

c.execute("""
INSERT OR IGNORE INTO admin (pin) VALUES ('200170')
""")

conn.commit()

# ---------------- UI HEADER ----------------
st.set_page_config(page_title=APP_TITLE, layout="centered")

if os.path.exists(LOGO_PATH):
    st.image(LOGO_PATH, width=120)

st.title(APP_TITLE)

LANG = st.selectbox("Language", LANGUAGES)

# ---------------- AGREEMENTS ----------------
with st.expander("📄 Agreements"):
    st.subheader("Transport Company Agreement")
    st.write("""
• Drivers are independent contractors  
• Hourly billing applies  
• Payment due within 14 days  
""")

    st.subheader("Driver Agreement")
    st.write("""
• Driver works as freelancer  
• Accepts dispatched jobs voluntarily  
""")

# ---------------- ROLE SELECTION ----------------
role = st.radio("Login as:", ["Dispatcher", "Driver", "Admin"])

# =================================================
# 🚚 DISPATCHER
# =================================================
if role == "Dispatcher":
    st.subheader("📦 Create Dispatch Request")

    company = st.selectbox("Company", COMPANIES)
    phone = st.text_input("Phone")
    canton = st.selectbox("Canton", ["ZH", "BE", "LU", "AG", "SG", "TI"])
    urgency = st.selectbox("Urgency", ["Normal", "Urgent"])
    message = st.text_area("Message")

    if st.button("Submit Request"):
        if not all([company, phone, canton, urgency, message]):
            st.error("❌ All fields are required")
            st.stop()

        # blacklist check
        blocked = c.execute(
            "SELECT 1 FROM blacklist WHERE company=?",
            (company,)
        ).fetchone()
        if blocked:
            st.error("🚫 Company blocked")
            st.stop()

        # find available driver by canton
        driver = c.execute("""
            SELECT name FROM drivers
            WHERE canton=? AND available=1
            LIMIT 1
        """, (canton,)).fetchone()

        assigned = driver[0] if driver else "Unassigned"

        c.execute("""
            INSERT INTO requests
            (company, phone, canton, urgency, message, created_at, assigned_driver)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            company,
            phone,
            canton,
            urgency,
            message,
            datetime.datetime.now().isoformat(),
            assigned
        ))

        if driver:
            c.execute("""
                UPDATE drivers SET available=0 WHERE name=?
            """, (assigned,))

        conn.commit()
        st.success("✅ Request submitted")

# =================================================
# 🚛 DRIVER
# =================================================
elif role == "Driver":
    st.subheader("🚛 Driver Portal")

    name = st.text_input("Your Name")
    canton = st.selectbox("Your Canton", ["ZH", "BE", "LU", "AG", "SG", "TI"])
    available = st.checkbox("Available")

    if st.button("Save Availability"):
        if not name:
            st.error("Name required")
            st.stop()

        c.execute("""
            INSERT OR REPLACE INTO drivers (id, name, canton, available)
            VALUES (
                (SELECT id FROM drivers WHERE name=?),
                ?, ?, ?
            )
        """, (name, name, canton, int(available)))
        conn.commit()
        st.success("Status updated")

    st.subheader("📋 Assigned Jobs")
    jobs = c.execute("""
        SELECT id, company, canton, urgency, message
        FROM requests
        WHERE assigned_driver=? AND status='Pending'
    """, (name,)).fetchall()

    for j in jobs:
        st.write(j)
        if st.button(f"Mark completed #{j[0]}"):
            c.execute("""
                UPDATE requests SET status='Completed'
                WHERE id=?
            """, (j[0],))
            c.execute("""
                UPDATE drivers SET available=1 WHERE name=?
            """, (name,))
            conn.commit()
            st.success("Job completed")
            st.rerun()

# =================================================
# 🔐 ADMIN
# =================================================
elif role == "Admin":
    st.subheader("🔐 Admin Login")
    pin = st.text_input("PIN", type="password")

    valid = c.execute(
        "SELECT 1 FROM admin WHERE pin=?",
        (pin,)
    ).fetchone()

    if valid:
        st.success("Access granted")

        st.subheader("📊 Requests")
        rows = c.execute("""
            SELECT id, company, canton, urgency, status, assigned_driver
            FROM requests ORDER BY created_at DESC
        """).fetchall()
        for r in rows:
            st.write(r)

        st.subheader("🚛 Drivers")
        drivers = c.execute("""
            SELECT name, canton, available FROM drivers
        """).fetchall()
        for d in drivers:
            st.write(d)

    else:
        st.info("Enter admin PIN")

