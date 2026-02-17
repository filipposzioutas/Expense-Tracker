import streamlit as st
import pandas as pd
import csv
from datetime import date
import os
import uuid
import matplotlib.pyplot as plt

# ---------------- Session-based file ----------------
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

USER_CSV = os.path.join(DATA_DIR, f"expenses_{st.session_state.user_id}.csv")

# ---------------- Sidebar ----------------
st.sidebar.title("Μενού")
page = st.sidebar.radio(
    "Επιλέξτε σελίδα", ["Προσθήκη Εξόδου", "Προβολή Συνόλων"]
)

# ---------------- Helper Functions ----------------
def init_csv():
    if not os.path.exists(USER_CSV):
        with open(USER_CSV, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Ημερομηνία", "Ποσό", "Κατηγορία", "Περιγραφή"])

def save_expense(exp_date, amount, category, description):
    with open(USER_CSV, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([exp_date, amount, category, description])

init_csv()

# ---------------- Pages ----------------
if page == "Προσθήκη Εξόδου":
    st.title("💸 Σωστή Οικονομία")
    st.write("Τα δεδομένα αποθηκεύονται **μόνο στη δική σας συσκευή**")

    selected_date = st.date_input(
        "Επιλέξτε ημερομηνία",
        value=date.today()
    )

    amount = st.number_input("Ποσό εξόδου (€)", min_value=0, step=1)
    category = st.selectbox(
        "Κατηγορία",
        ["Φαγητό", "Μετακίνηση", "Ενοίκιο", "Διασκέδαση", "Άλλο"]
    )
    description = st.text_input("Περιγραφή (προαιρετικά)")

    if st.button("Προσθήκη εξόδου"):
        if amount > 0:
            save_expense(selected_date, amount, category, description)
            st.success("✅ Η έξοδος αποθηκεύτηκε!")
        else:
            st.warning("⚠️ Το ποσό πρέπει να είναι > 0")

# ---------------- View Totals ----------------
else:
    st.title("📊 Τα έξοδά μου")

    try:
        df = pd.read_csv(
            USER_CSV,
            names=["Ημερομηνία", "Ποσό", "Κατηγορία", "Περιγραφή"],
            header=0
        )

        if df.empty:
            st.info("Δεν έχετε προσθέσει έξοδα ακόμα.")
            st.stop()

        df["Ποσό"] = pd.to_numeric(df["Ποσό"], errors="coerce").fillna(0)

        st.dataframe(df, use_container_width=True)

        total_expenses = df["Ποσό"].sum()

        income = st.number_input(
            "Εισάγετε το μηνιαίο εισόδημά σας (€)",
            min_value=0,
            step=50
        )

        remaining = income - total_expenses

        st.write(f"💰 **Συνολικά έξοδα:** €{total_expenses:.2f}")

        if remaining >= 0:
            st.success(f"🟢 Υπόλοιπο: €{remaining:.2f}")
        else:
            st.error(f"🔴 Υπέρβαση: €{abs(remaining):.2f}")

        # -------- Chart --------
        st.subheader("🍕 Έξοδα ανά Κατηγορία")

        summary = df.groupby("Κατηγορία")["Ποσό"].sum()

        fig, ax = plt.subplots()
        ax.pie(
            summary,
            labels=summary.index,
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")

        st.pyplot(fig)

    except Exception as e:
        st.error("Σφάλμα ανάγνωσης δεδομένων")
        st.exception(e)
