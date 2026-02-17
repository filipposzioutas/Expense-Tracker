import streamlit as st
import pandas as pd
import csv
from datetime import date
import matplotlib.pyplot as plt


CSV_FILE = "expenses.csv"

st.sidebar.title("Μενού")
page = st.sidebar.radio(
    "Επιλέξτε σελίδα", ["Προσθήκη Εξόδου", "Προβολή Συνόλων"])


def save_expense(date, amount, category, description):
    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, amount, category, description])


if page == "Προσθήκη Εξόδου":
    st.title("💸 Σωστή Οικονομία")
    st.write("Παρακολουθήστε το εισόδημά σας και τα καθημερινά έξοδα")

    income = st.number_input(
        "Εισάγετε το μηνιαίο εισόδημά σας (€)", min_value=0, step=50)

    selected_date = st.date_input("Επιλέξτε ημερομηνία", value=date.today())

    st.subheader("Προσθέστε ένα νέο έξοδο")
    amount = st.number_input("Ποσό εξόδου (€)", min_value=0, step=1)
    category = st.selectbox(
        "Κατηγορία", ["Φαγητό", "Μετακίνηση", "Ενοίκιο", "Διασκέδαση", "Άλλο"])
    description = st.text_input("Περιγραφή (προαιρετικά)")

    if st.button("Προσθήκη εξόδου"):
        save_expense(selected_date, amount, category, description)
        st.success("✅ Η έξοδος αποθηκεύτηκε!")

else:
    st.title("📊 Συνολικά Έξοδα")

    try:
        df = pd.read_csv(CSV_FILE, names=[
                         "Ημερομηνία", "Ποσό", "Κατηγορία", "Περιγραφή"])
        st.dataframe(df)

        total_expenses = df["Ποσό"].sum()

        income = st.number_input(
            "Εισάγετε το μηνιαίο εισόδημά σας (€)", min_value=0, step=50)
        remaining = income - total_expenses
        st.write(f"💰 Συνολικά έξοδα: €{total_expenses}")
        st.write(f"🟢 Υπόλοιπο προϋπολογισμού: €{remaining}")

        st.subheader("🍕 Έξοδα ανά Κατηγορία")
        category_summary = df.groupby("Κατηγορία")["Ποσό"].sum()
        st.pyplot(category_summary.plot.pie(autopct="%1.1f%%").figure)

    except FileNotFoundError:
        st.write(
            "Δεν υπάρχουν έξοδα ακόμα. Προσθέστε κάποια στη σελίδα 'Προσθήκη Εξόδου'!")

