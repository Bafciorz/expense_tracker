import streamlit as st
import pandas as pd
from datetime import datetime, date
from src.database import DatabaseManager
from src.categories import Category
import plotly.express as px


# --- initialization ---
db = DatabaseManager("expenses.db")

st.set_page_config(
    page_title=" Expense Tracker",
    layout="centered"
)

# --- sidebar ---
st.sidebar.title("Main menu")
choice = st.sidebar.radio(
    "Choose interaction",
    ["Browse your expense", "Add new expense", "Pie chart by category"]
)

# --- adding expense---
if choice == "Add new expense":
    st.header("Add new expense")

    with st.form("add_expense_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            expense_date = st.date_input("Expense date", value=date.today())
            amount = st.number_input("Amount (zł)", min_value=0.01, step=0.01, format="%.2f")

        with col2:
            cat_list = [c.value for c in Category]
            category_name = st.selectbox("Category", options=cat_list)
            description = st.text_input("Description")

        submitted = st.form_submit_button("Save expense")

        if submitted:
            selected_enum = next(c for c in Category if c.value == category_name)
            db.add_expense(
                date=str(expense_date),
                amount=amount,
                category=selected_enum,
                description=description
            )
            st.success(f"Succesfully added: {amount} zł to category{category_name}")

elif choice == "Pie chart by category":
    st.header("Pie chart by category")

    st.sidebar.markdown("---")
    st.sidebar.subheader("Filtr")

    f_category_name = st.sidebar.selectbox(
        "Category",
        ["All"] + [c.value for c in Category]
    )

    f_start_date = st.sidebar.date_input("From", value=datetime(2024, 1, 1))
    f_end_date = st.sidebar.date_input("To", value=date.today())

    selected_cat = None
    if f_category_name != "All":
        selected_cat = next(c for c in Category if c.value == f_category_name)

    df = db.get_expenses(
        start_date=f_start_date,
        end_date=f_end_date,
        category=selected_cat
    )

    if not df.empty:
        col1_chart, col2 = st.columns([1,1])

        with col1_chart:
            category_sum = df.groupby('category_name')['amount'].sum().reset_index()
            fig = px.pie(category_sum,values='amount', names='category_name', title="expenses structure")
            st.plotly_chart(fig,use_container_width=True)

# --- history ---
else:
    st.header("History of your expenses")

    st.sidebar.markdown("---")
    st.sidebar.subheader("Filtr")

    f_category_name = st.sidebar.selectbox(
        "Category",
        ["All"] + [c.value for c in Category]
    )

    f_start_date = st.sidebar.date_input("From", value=datetime(2024, 1, 1))
    f_end_date = st.sidebar.date_input("To", value=date.today())

    selected_cat = None
    if f_category_name != "All":
        selected_cat = next(c for c in Category if c.value == f_category_name)

    df = db.get_expenses(
        start_date=f_start_date,
        end_date=f_end_date,
        category=selected_cat
    )

    if not df.empty:
        total_sum = df['amount'].sum()
        st.metric("sum of your espenses", f"{total_sum:,.2f} zł".replace(",", " "))
        df_display = df.copy()
        df_display.insert(0, 'No.', range(1, len(df) + 1))

        selection = st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            column_config={"id": None},
            on_select="rerun",
            selection_mode="multi-row"
        )

        selected_rows = selection.selection.rows

        if selected_rows:
            if st.button(f"Delete selected ({len(selected_rows)})", type="primary"):
                for row_idx in selected_rows:
                    id_to_del = int(df.iloc[row_idx]['id'])
                    db.delete_expense(id_to_del)

                st.success("Successfully deleted!")
                st.rerun()



        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download as csv",
            data=csv,
            file_name='expenses.csv',
            mime='text/csv',
        )
    else:
        st.warning("There is no expenses.")

# --- ---
st.sidebar.markdown("---")
st.sidebar.info("Jakub Bafia")