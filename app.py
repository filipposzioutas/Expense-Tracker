import streamlit as st
import pandas as pd
import csv
from datetime import date
import os
import matplotlib.pyplot as plt

CSV_FILE = "expenses.csv"

# ---------------- Sidebar ----------------
st.sidebar.title("Μενού")
page = st.sidebar.radio(
    "Επιλέξτε σελίδα", ["Προσθήκη Εξόδου", "Προβολή Συνόλων"]
)

# ---------------- Helper Functions ----------------
def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Ημερομηνία", "Ποσό", "Κατηγορία", "Περιγραφή"])

def save_expense(exp_date, amount, category, description):
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([exp_date, amount, category, description])

init_csv()

# ---------------- Pages ----------------
if page == "Προσθήκη Εξόδου":
    st.title("💸 Σωστή Οικονομία")
    st.write("Παρακολουθήστε το εισόδημά σας και τα καθημερινά έξοδα")

    st.subheader("➕ Προσθήκη νέου εξόδου")

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
            st.warning("⚠️ Το ποσό πρέπει να είναι μεγαλύτερο από 0")

# ---------------- View Totals ----------------
else:
    st.title("📊 Συνολικά Έξοδα")

    try:
        # ⬇️ ΔΙΑΒΑΖΟΥΜΕ ΧΩΡΙΣ HEADERS
        df = pd.read_csv(
            CSV_FILE,
            header=0,
            names=["Ημερομηνία", "Ποσό", "Κατηγορία", "Περιγραφή"]
        )

        if df.empty:
            st.info("Δεν υπάρχουν έξοδα ακόμα.")
            st.stop()

        # ⬇️ ΒΕΒΑΙΩΝΟΜΑΣΤΕ ΟΤΙ ΤΟ ΠΟΣΟ ΕΙΝΑΙ ΑΡΙΘΜΟΣ
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
            st.success(f"🟢 Υπόλοιπο προϋπολογισμού: €{remaining:.2f}")
        else:
            st.error(f"🔴 Υπέρβαση προϋπολογισμού: €{abs(remaining):.2f}")

        # -------- Pie Chart --------
        st.subheader("🍕 Έξοδα ανά Κατηγορία")

        category_summary = df.groupby("Κατηγορία")["Ποσό"].sum()

        fig, ax = plt.subplots()
        ax.pie(
            category_summary,
            labels=category_summary.index,
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")

        st.pyplot(fig)

    except Exception as e:
        st.error("Παρουσιάστηκε σφάλμα κατά την ανάγνωση των δεδομένων.")
        st.exception(e)
