import streamlit as st
from src.categories import Category
from src.database import DatabaseManager

st.title("Expenses tracker")

db = DatabaseManager("expenses.db")

st.sidebar.header("Filters")

selected_cat_name = st.sidebar.selectbox(
    "Choose category:",
    ["All"] + [kat.value for kat in Category]
)

selected_cat = None
if selected_cat_name != "All":
    selected_cat = next(k for k in Category if k.value == selected_cat_name)

st.subheader("Expenses list")


df = db.get_expenses(category=selected_cat)

if df.empty:
    st.info("Brak wydatków do wyświetlenia dla wybranych filtrów.")
else:
    # Wyświetlamy ładną tabelę
    st.dataframe(df, use_container_width=True)

    # Małe podsumowanie pod tabelą
    total = df['amount'].sum()
    st.metric(label="Suma wydatków", value=f"{total:.2f} zł")