import streamlit as st
import pandas as pd

st.set_page_config(page_title="Smart Budgeting App", layout="centered")

st.title("📊 Smart Budgeting App")
st.write("Track your income, expenses, and savings goals with ease.")

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Date", "Category", "Description", "Planned Amount", "Actual Amount", "Current Balance"])

# Section: Add a new transaction
st.header("➕ Add New Entry")
with st.form("entry_form"):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date")
        category = st.selectbox("Category", ["Income", "Bills", "Food", "Transport", "Entertainment", "Shopping", "Health", "Savings", "Other"])
    with col2:
        description = st.text_input("Description")
        planned = st.number_input("Planned Amount ($)", min_value=0.0, step=0.01)
        actual = st.number_input("Actual Amount ($)", min_value=0.0, step=0.01)

    submitted = st.form_submit_button("Add Entry")
    if submitted:
        new_row = pd.DataFrame([[date, category, description, planned, actual]],
                               columns=st.session_state.data.columns)
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
        st.success("Entry added!")

# Section: View Transactions
df = st.session_state.data
if not df.empty:
    st.header("📅 Transaction History")
    st.dataframe(df)

    # Save/Export
    st.download_button("⬇️ Download CSV", df.to_csv(index=False), file_name="budget_data.csv", mime="text/csv")

    # Category Filter
    st.subheader("📂 Filter by Category")
    category_filter = st.selectbox("Select Category", ["All"] + df["Category"].unique().tolist())
    if category_filter != "All":
        df = df[df["Category"] == category_filter]

    # Budget Summary
    st.subheader("📈 Summary")
    grouped = df.groupby("Category")[["Planned Amount", "Actual Amount"]].sum()
    grouped["Difference"] = grouped["Planned Amount"] - grouped["Actual Amount"]
    st.dataframe(grouped)

    # Overspending Alerts
    st.subheader("🚨 Overspending Alerts")
    overspent = grouped[grouped["Difference"] < 0]
    if not overspent.empty:
        st.warning("You have overspent in the following categories:")
        st.dataframe(overspent)
    else:
        st.success("You're within your planned budget for all categories!")
else:
    st.info("No entries yet. Add your first income or expense above.")
