import streamlit as st
import pandas as pd
import csv
from datetime import date
import os
import uuid
import matplotlib.pyplot as plt

# ---------------- Session-based files ----------------
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

EXPENSES_CSV = os.path.join(DATA_DIR, f"expenses_{st.session_state.user_id}.csv")
INCOME_FILE = os.path.join(DATA_DIR, f"income_{st.session_state.user_id}.txt")

# ---------------- Sidebar ----------------
st.sidebar.title("Μενού")
page = st.sidebar.radio(
    "Επιλέξτε σελίδα", ["Προσθήκη Εξόδου", "Προβολή Συνόλων"]
)

# ---------------- Helper Functions ----------------
def init_expenses():
    if not os.path.exists(EXPENSES_CSV):
        with open(EXPENSES_CSV, "w", newline="", enco_
