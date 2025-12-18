# -*- coding: utf-8 -*-
# app.py
# On-Demand Driver Dispatcher – STABLE v3

import streamlit as st
import sqlite3
from datetime import datetime
from PIL import Image

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="On-Demand Driver Dispatcher",
    layout="centered",
    page_icon="🚚"
)

# ---------------- LOGO & TITLE ----------------
header_container = st.container()
with header_container:
    cols = st.columns([1, 4, 1])
    try:
        logo = Image.open("truck.jpeg")  # Your custom logo
        cols[0].image(logo, width=80)
    except FileNotFoundError:
        cols[0].markdown("🚚")  # Fallback emoji
    cols[1].markdown(
        "<h1 style='text-align:center; color:#2E86C1;'>On-Demand Driver Dispatcher</h1>",
        unsafe_allow_html=True
    )

# ---------------- DATABASE ----------------
conn = sqlite3.connect("dispatcher.db", check_same_thread=False)
c = conn.cursor()

# Ensure tables exist
c.execute("""
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    phone TEXT,
    canton TEXT,
    urgency TEXT,
    message TEXT,
    created_at TEXT,
    status TEXT DEFAULT 'Pending',
    assigned_driver TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS drivers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    available INTEGER DEFAULT 0,
    canton TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS admin (
    pin TEXT PRIMARY KEY
)
""")
c.execute("INSERT OR IGNORE INTO admin (pin) VALUES ('200170')")
conn.commit()

# ---------------- LANGUAGE ----------------
LANG = st.sidebar.selectbox(
    "Language / Sprache / Langue / Lingua",
    ["EN", "DE", "FR", "IT"]
)

# Translation dictionary (same as before, including 'fill_all')
T = {
    "EN": {
        "title": "On-Demand Driver Dispatcher",
        "mode": "Mode",
        "dispatcher": "Dispatcher",
        "driver": "Driver",
        "admin": "Admin",
        "company": "Company",
        "phone": "Phone",
        "canton": "Canton",
        "urgency": "Urgency",
        "details": "Job details",
        "submit": "Submit request",
        "pending": "Requests",
        "agree_company": "I accept the Transport Company Agreement",
        "agree_driver": "I accept the Driver Agreement",
        "must_accept": "You must accept both agreements",
        "success": "Request submitted",
        "pin": "Admin PIN",
        "invalid": "Invalid PIN",
        "add_driver": "Add driver",
        "driver_name": "Driver name",
        "available": "Available today",
        "fill_all": "Please fill all required fields"
    },
    "DE": {
        "title": "Fahrer-Dispositionsplattform",
        "mode": "Modus",
        "dispatcher": "Disposition",
        "driver": "Fahrer",
        "admin": "Admin",
        "company": "Firma",
        "phone": "Telefon",
        "canton": "Kanton",
        "urgency": "Dringlichkeit",
        "details": "Auftragsdetails",
        "submit": "Anfrage senden",
        "pending": "Anfragen",
        "agree_company": "Ich akzeptiere die Transportfirmen-Vereinbarung",
        "agree_driver": "Ich akzeptiere die Fahrer-Vereinbarung",
        "must_accept": "Beide Vereinbarungen sind Pflicht",
        "success": "Anfrage gesendet",
        "pin": "Admin-PIN",
        "invalid": "Ungültiger PIN",
        "add_driver": "Fahrer hinzufügen",
        "driver_name": "Fahrername",
        "available": "Heute verfügbar",
        "fill_all": "Bitte alle Pflichtfelder ausfüllen"
    },
    "FR": {
        "title": "Plateforme de dispatch chauffeurs",
        "mode": "Mode",
        "dispatcher": "Dispatch",
        "driver": "Chauffeur",
        "admin": "Admin",
        "company": "Entreprise",
        "phone": "Téléphone",
        "canton": "Canton",
        "urgency": "Urgence",
        "details": "Détails",
        "submit": "Envoyer",
        "pending": "Demandes",
        "agree_company": "J’accepte l’accord entreprise",
        "agree_driver": "J’accepte l’accord chauffeur",
        "must_accept": "Accords obligatoires",
        "success": "Demande envoyée",
        "pin": "PIN admin",
        "invalid": "PIN incorrect",
        "add_driver": "Ajouter chauffeur",
        "driver_name": "Nom chauffeur",
        "available": "Disponible aujourd’hui",
        "fill_all": "Veuillez remplir tous les champs obligatoires"
    },
    "IT": {
        "title": "Piattaforma di assegnazione autisti",
        "mode": "Modalità",
        "dispatcher": "Assegnazione",
        "driver": "Autista",
        "admin": "Admin",
        "company": "Azienda",
        "phone": "Telefono",
        "canton": "Cantone",
        "urgency": "Urgenza",
        "details": "Dettagli",
        "submit": "Invia",
        "pending": "Richieste",
        "agree_company": "Accetto l’accordo azienda",
        "agree_driver": "Accetto l’accordo autista",
        "must_accept": "Accordi obbligatori",
        "success": "Richiesta inviata",
        "pin": "PIN admin",
        "invalid": "PIN non valido",
        "add_driver": "Aggiungi autista",
        "driver_name": "Nome autista",
        "available": "Disponibile oggi",
        "fill_all": "Compila tutti i campi obbligatori"
    }
}

# =========================
# Companies list
# =========================
companies = [
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

# ---------------- UI ----------------
st.title(T[LANG]["title"])
mode = st.radio(T[LANG]["mode"], [T[LANG]["dispatcher"], T[LANG]["driver"], T[LANG]["admin"]])

# ---------------- DISPATCHER ----------------
if mode == T[LANG]["dispatcher"]:
    company = st.selectbox(T[LANG]["company"], companies)
    phone = st.text_input(T[LANG]["phone"])
    canton = st.selectbox(T[LANG]["canton"], ["SO", "BE", "AG", "BL", "BS", "JU"])
    urgency = st.selectbox(T[LANG]["urgency"], ["Normal", "Urgent", "Emergency"])
    message = st.text_area(T[LANG]["details"])

    st.markdown("### Agreements")
    st.markdown({
        "EN": "**Transport Company Agreement**\n- Drivers are independent contractors\n- Hourly billing applies\n- Payment due within 14 days\n\n**Driver Agreement**\n- Driver works as freelancer\n- Accepts dispatched jobs voluntarily",
        "DE": "**Transportfirmen-Vereinbarung**\n- Fahrer sind unabhängige Auftragnehmer\n- Abrechnung auf Stundenbasis\n- Zahlung innerhalb von 14 Tagen\n\n**Fahrer-Vereinbarung**\n- Fahrer arbeitet als Freelancer\n- Akzeptiert freiwillig zugewiesene Aufträge",
        "FR": "**Accord entreprise de transport**\n- Les chauffeurs sont des travailleurs indépendants\n- Facturation horaire\n- Paiement dû sous 14 jours\n\n**Accord chauffeur**\n- Le chauffeur travaille en freelance\n- Accepte volontairement les missions",
        "IT": "**Accordo azienda di trasporto**\n- Gli autisti sono liberi professionisti\n- Fatturazione oraria\n- Pagamento entro 14 giorni\n\n**Accordo autista**\n- L'autista lavora come freelancer\n- Accetta volontariamente i lavori assegnati"
    }[LANG])

    agree_company = st.checkbox(T[LANG]["agree_company"])
    agree_driver = st.checkbox(T[LANG]["agree_driver"])

    if st.button(T[LANG]["submit"]):
        # Validate fields
        if not company or not phone or not canton or not message:
            st.error(T[LANG]["fill_all"])
        elif not (agree_company and agree_driver):
            st.error(T[LANG]["must_accept"])
        else:
            c.execute("""
                INSERT INTO requests (
                    company, phone, canton, urgency, message, created_at, status
                ) VALUES (?,?,?,?,?,?,?)
            """, (company, phone, canton, urgency, message, datetime.now().isoformat(), "Pending"))
            conn.commit()
            st.success(T[LANG]["success"])

    rows = c.execute("SELECT company, urgency, created_at FROM requests ORDER BY id DESC").fetchall()
    st.table(rows)

# ---------------- DRIVER ----------------
elif mode == T[LANG]["driver"]:
    name = st.text_input(T[LANG]["driver_name"])
    canton = st.selectbox("Canton", ["SO", "BE", "AG", "BL", "BS", "JU"])
    available = st.checkbox(T[LANG]["available"])

    if st.button(T[LANG]["add_driver"]):
        if not name or not canton:
            st.error(T[LANG]["fill_all"])
        else:
            c.execute("INSERT INTO drivers VALUES (NULL, ?, ?, ?)", (name, int(available), canton))
            conn.commit()
            st.success(T[LANG]["success"])

    rows = c.execute("SELECT name, canton, available FROM drivers ORDER BY id DESC").fetchall()
    st.table([(r[0], r[1], "Yes" if r[2] else "No") for r in rows])

# ---------------- ADMIN ----------------
else:
    pin = st.text_input(T[LANG]["pin"], type="password")
    real_pin = c.execute("SELECT pin FROM admin").fetchone()[0]

    if pin != real_pin:
        st.error(T[LANG]["invalid"])
    else:
        st.success("Access granted")
        st.subheader(T[LANG]["pending"])
        st.table(c.execute("SELECT * FROM requests ORDER BY id DESC").fetchall())
        st.subheader("Drivers")
        st.table(c.execute("SELECT * FROM drivers ORDER BY id DESC").fetchall())
