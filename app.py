import streamlit as st
import pandas as pd
import csv
import os
import uuid
from datetime import date
import matplotlib.pyplot as plt

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

EXPENSES_FILE = os.path.join(DATA_DIR, "expenses_" + st.session_state.user_id + ".csv")
INCOME_FILE = os.path.join(DATA_DIR, "income_" + st.session_state.user_id + ".txt")

st.sidebar.title("Μενού")
page = st.sidebar.radio("Επιλογή Σελίδας", ["Προσθήκη Έξοδου", "Σύνολο"])


def init_expenses():
    if not os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "amount", "category", "description"])


def save_expense(d, a, c, desc):
    with open(EXPENSES_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([d, a, c, desc])


def save_income(value):
    with open(INCOME_FILE, "w", encoding="utf-8") as f:
        f.write(str(value))


def load_income():
    if os.path.exists(INCOME_FILE):
        with open(INCOME_FILE, "r", encoding="utf-8") as f:
            return float(f.read())
    return None


init_expenses()

if page == "Προσθήκη Έξοδου":
    st.title("Expense Tracker")

    income = load_income()
    if income is None:
        income = 0

    income_input = st.number_input("Monthly income", min_value=0, step=50, value=int(income))
    if st.button("Save income"):
        save_income(income_input)
        st.success("Income saved")

    st.divider()

    expense_date = st.date_input("Ημερομηνία", value=date.today())
    amount = st.number_input("Ποσό", min_value=0, step=1)
    category = st.selectbox( "Κατηγορία", ["Φαγητό", "Μετακίνηση", "Ενοίκιο", "Διασκέδαση", "Άλλο"])
    description = st.text_input("Περιγραφή")

    if st.button("Προσθήκη Έξοδου"):
        if amount > 0:
            save_expense(expense_date, amount, category, description)
            st.success("Expense added")

else:
    st.title("Σύνολο")

    income = load_income()
    if income is None:
        st.warning("Παρακαλώ εισάγετε το εισόδημα σας")
        st.stop()

    df = pd.read_csv(EXPENSES_FILE)
    if df.empty:
        st.info("Δεν έχετε έξοδα")
        st.stop()

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    st.dataframe(df)

    total = df["amount"].sum()
    remaining = income - total

    st.write(f"💵 Εισόδημα: {income}")
    st.write(f"💸 Σύνολο εξόδων: {total}")
    st.write(f"💰 Υπόλοιπο: {remaining}")

    summary = df.groupby("category")["amount"].sum()

    fig, ax = plt.subplots()
    ax.pie(summary, labels=summary.index, autopct="%1.1f%%")
    ax.axis("equal")
    st.pyplot(fig)

