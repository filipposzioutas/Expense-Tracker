import streamlit as st
import pandas as pd
import csv
from datetime import date
import os
import uuid
import matplotlib.pyplot as plt

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

EXPENSES_CSV = os.path.join(DATA_DIR, f"expenses_{st.session_state.user_id}.csv")
INCOME_FILE = os.path.join(DATA_DIR, f"income_{st.session_state.user_id}.txt")

st.sidebar.title("Μενού")
page = st.sidebar.radio("Επιλέξτε σελίδα", ["Προσθήκη Εξόδου", "Προβολή Συνόλων"])


def init_expenses():
    if not os.path.exists(EXPENSES_CSV):
        with open(EXPENSES_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Ημερομηνία", "Ποσό", "Κατηγορία", "Περιγραφή"])


def load_income():
    if os.path.exists(INCOME_FILE):
        with open(INCOME_FILE, "r", encoding="utf-8") as f:
            return float(f.read())
    return None


def save_income(amount):
    with open(INCOME_FILE, "w", encoding="utf-8") as f:
        f.write(str(amount))


def save_expense(exp_date, amount, category, description):
    with open(EXPENSES_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([exp_date, amount, category, description])


init_expenses()

if page == "Προσθήκη Εξόδου":
    st.title("💸 Σωστή Οικονομία")

    st.subheader("💰 Μηνιαίο εισόδημα")
    current_income = load_income()

    income = st.number_input(
        "Εισάγετε το μηνιαίο εισόδημά σας (€)",
        min_value=0,
        step=50,
        value=int(current_income) if current_income is not None else 0
    )

    if st.button("💾 Αποθήκευση εισοδήματος"):
        save_income(income)
        st.success("Το εισόδημα αποθηκεύτηκε")

    st.divider()

    st.subheader("
