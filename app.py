# -*- coding: utf-8 -*-
# app.py
# On-Demand Driver Dispatcher – STABLE v3 (Admin + Driver Portal)

import streamlit as st
import sqlite3
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="On-Demand Driver Dispatcher",
    layout="centered"
)

# ---------------- DATABASE ----------------
conn = sqlite3.connect("dispatcher.db", check_same_thread=False)
c = conn.cursor()

# ---------------- LANGUAGE ----------------
LANG = st.sidebar.selectbox(
    "Language / Sprache / Langue / Lingua",
    ["EN", "DE", "FR", "IT"]
)

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
        "success": "Request submitted",
        "agree_company": "I accept the Transport Company Agreement",
        "agree_driver": "I accept the Driver Agreement",
        "must_accept": "You must accept both agreements",
        "fill_all": "Please fill all required fields",
        "driver_pin": "Driver PIN",
        "invalid_pin": "Invalid PIN",
        "assigned_jobs": "Your assigned jobs",
        "complete": "Mark job completed",
        "admin_pin": "Admin PIN",
        "invalid": "Invalid PIN",
        "assign": "Assign driver",
        "completed": "Completed"
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
        "success": "Anfrage gesendet",
        "agree_company": "Ich akzeptiere die Transportfirmen-Vereinbarung",
        "agree_driver": "Ich akzeptiere die Fahrer-Vereinbarung",
        "must_accept": "Beide Vereinbarungen sind Pflicht",
        "fill_all": "Bitte alle Pflichtfelder ausfüllen",
        "driver_pin": "Fahrer-PIN",
        "invalid_pin": "Ungültiger PIN",
        "assigned_jobs": "Zugewiesene Aufträge",
        "complete": "Auftrag abschließen",
        "admin_pin": "Admin-PIN",
        "invalid": "Ungültiger PIN",
        "assign": "Fahrer zuweisen",
        "completed": "Abgeschlossen"
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
        "success": "Demande envoyée",
        "agree_company": "J’accepte l’accord entreprise",
        "agree_driver": "J’accepte l’accord chauffeur",
        "must_accept": "Accords obligatoires",
        "fill_all": "Veuillez remplir tous les champs",
        "driver_pin": "PIN chauffeur",
        "invalid_pin": "PIN incorrect",
        "assigned_jobs": "Missions assignées",
        "complete": "Mission terminée",
        "admin_pin": "PIN admin",
        "invalid": "PIN incorrect",
        "assign": "Assigner chauffeur",
        "completed": "Terminée"
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
        "submit": "Invia richiesta",
        "success": "Richiesta inviata",
        "agree_company": "Accetto l’accordo azienda",
        "agree_driver": "Accetto l’accordo autista",
        "must_accept": "Accordi obbligatori",
        "fill_all": "Compila tutti i campi",
        "driver_pin": "PIN autista",
        "invalid_pin": "PIN non valido",
        "assigned_jobs": "Lavori assegnati",
        "complete": "Segna completato",
        "admin_pin": "PIN admin",
        "invalid": "PIN non valido",
        "assign": "Assegna autista",
        "completed": "Completato"
    }
}

# ---------------- COMPANIES ----------------
companies = [
    "Planzer Holding AG", "Galliker Transport AG", "Kühne + Nagel (Schweiz) AG",
    "DB Schenker Schweiz AG", "Gebrüder Weiss AG", "Rhenus Logistics Schweiz AG",
    "CEVA Logistics Switzerland", "DSV Air & Sea AG", "Gondrand International AG",
    "Welti-Furrer AG", "Schöni Transport AG", "Bertschi AG",
    "Emil Egger AG", "Sieber Transport AG", "Post CH AG"
]

# ---------------- UI ----------------
st.title(T[LANG]["title"])
mode = st.radio(T[LANG]["mode"], [
    T[LANG]["dispatcher"],
    T[LANG]["driver"],
    T[LANG]["admin"]
])

# =========================
# DISPATCHER
# =========================
if mode == T[LANG]["dispatcher"]:
    company = st.selectbox(T[LANG]["company"], companies)
    phone = st.text_input(T[LANG]["phone"])
    canton = st.selectbox(T[LANG]["canton"], ["SO", "BE", "AG", "BL", "BS", "JU"])
    urgency = st.selectbox(T[LANG]["urgency"], ["Normal", "Urgent", "Emergency"])
    message = st.text_area(T[LANG]["details"])

    st.markdown("### Agreements")
    st.markdown("""
    **Transport Company Agreement**
    - Drivers are independent contractors  
    - Hourly billing applies  
    - Payment due within 14 days  

    **Driver Agreement**
    - Driver works as freelancer  
    - Accepts dispatched jobs voluntarily  
    """)

    agree_company = st.checkbox(T[LANG]["agree_company"])
    agree_driver = st.checkbox(T[LANG]["agree_driver"])

    if st.button(T[LANG]["submit"]):
        if not phone or not message:
            st.error(T[LANG]["fill_all"])
        elif not (agree_company and agree_driver):
            st.error(T[LANG]["must_accept"])
        else:
            c.execute("""
                INSERT INTO requests
                (company, phone, canton, urgency, message, created_at, status)
                VALUES (?,?,?,?,?,?,?)
            """, (
                company, phone, canton, urgency,
                message, datetime.now().isoformat(), "Pending"
            ))
            conn.commit()
            st.success(T[LANG]["success"])

# =========================
# DRIVER PORTAL (PIN)
# =========================
elif mode == T[LANG]["driver"]:
    pin = st.text_input(T[LANG]["driver_pin"], type="password")

    driver = c.execute(
        "SELECT name FROM drivers WHERE pin=?",
        (pin,)
    ).fetchone()

    if not driver and pin:
        st.error(T[LANG]["invalid_pin"])

    if driver:
        driver_name = driver[0]
        st.subheader(T[LANG]["assigned_jobs"])

        jobs = c.execute("""
            SELECT id, company, canton, urgency
            FROM requests
            WHERE assigned_driver=? AND status!='Completed'
        """, (driver_name,)).fetchall()

        for j in jobs:
            st.write(f"**{j[1]}** – {j[2]} ({j[3]})")
            if st.button(T[LANG]["complete"], key=f"drv_{j[0]}"):
                c.execute(
                    "UPDATE requests SET status='Completed' WHERE id=?",
                    (j[0],)
                )
                c.execute(
                    "UPDATE drivers SET available=1 WHERE name=?",
                    (driver_name,)
                )
                conn.commit()
                st.experimental_rerun()

# =========================
# ADMIN
# =========================
else:
    pin = st.text_input(T[LANG]["admin_pin"], type="password")
    admin_pin = c.execute("SELECT pin FROM admin").fetchone()[0]

    if pin != admin_pin:
        st.error(T[LANG]["invalid"])
    else:
        st.success("Access granted")

        requests = c.execute("""
            SELECT id, company, canton, urgency, status, assigned_driver
            FROM requests
            WHERE status!='Completed'
            ORDER BY id DESC
        """).fetchall()

        drivers = c.execute("""
            SELECT name FROM drivers WHERE available=1
        """).fetchall()

        driver_names = [d[0] for d in drivers]

        for r in requests:
            st.write(f"**{r[1]}** – {r[2]} ({r[3]}) | {r[4]}")

            if not r[5] and driver_names:
                chosen = st.selectbox(
                    T[LANG]["assign"],
                    driver_names,
                    key=f"a_{r[0]}"
                )
                if st.button("Assign", key=f"b_{r[0]}"):
                    c.execute("""
                        UPDATE requests
                        SET assigned_driver=?, status='Assigned'
                        WHERE id=?
                    """, (chosen, r[0]))
                    c.execute("""
                        UPDATE drivers SET available=0 WHERE name=?
                    """, (chosen,))
                    conn.commit()
                    st.experimental_rerun()

            if r[5]:
                if st.button(T[LANG]["complete"], key=f"c_{r[0]}"):
                    c.execute(
                        "UPDATE requests SET status='Completed' WHERE id=?",
                        (r[0],)
                    )
                    c.execute(
                        "UPDATE drivers SET available=1 WHERE name=?",
                        (r[5],)
                    )
                    conn.commit()
                    st.experimental_rerun()
