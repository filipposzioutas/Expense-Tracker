import streamlit as st
import pandas as pd
import csv
from datetime import date

CSV_FILE = "expenses.csv"

# -----------------------------
# Sidebar for navigation
# -----------------------------
st.sidebar.title("Menu")
page = st.sidebar.radio("Choose page", ["Add Expense", "View Summary"])

# -----------------------------
# Function to save expenses
# -----------------------------


def save_expense(date, amount, category, description):
    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, amount, category, description])


# -----------------------------
# Page 1: Add Expense
# -----------------------------
if page == "Add Expense":
    st.title("💸 Expense Tracker App")
    st.write("Track your income and daily expenses")

    # Income
    income = st.number_input(
        "Enter your monthly income (€)", min_value=0, step=50)

    # Date picker
    selected_date = st.date_input("Select date", value=date.today())

    # Expense inputs
    st.subheader("Add a new expense")
    amount = st.number_input("Expense amount (€)", min_value=0, step=1)
    category = st.selectbox(
        "Category", ["Food", "Transport", "Rent", "Entertainment", "Other"])
    description = st.text_input("Description (optional)")

    # Button to save expense
    if st.button("Add expense"):
        save_expense(selected_date, amount, category, description)
        st.success("✅ Expense saved!")

# -----------------------------
# Page 2: View Summary
# -----------------------------
else:
    st.title("📊 Expense Summary")

    try:
        df = pd.read_csv(CSV_FILE, names=[
                         "Date", "Amount", "Category", "Description"])
        st.dataframe(df)

        # Total expenses & remaining budget
        total_expenses = df["Amount"].sum()
        # Ask user for monthly income to calculate remaining
        income = st.number_input(
            "Enter your monthly income (€)", min_value=0, step=50)
        remaining = income - total_expenses
        st.write(f"💰 Total expenses: €{total_expenses}")
        st.write(f"🟢 Remaining budget: €{remaining}")

        # Category pie chart
        st.subheader("🍕 Expenses by Category")
        category_summary = df.groupby("Category")["Amount"].sum()
        st.pyplot(category_summary.plot.pie(autopct="%1.1f%%").figure)

    except FileNotFoundError:
        st.write("No expenses yet. Add some in the 'Add Expense' page!")
