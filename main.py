import streamlit as st
import pandas as pd
import numpy as np

# 1. Konfiguracja strony
st.set_page_config(page_title="Giełda Demo", layout="wide")
st.title("📈 Przykładowy Dashboard Giełdowy")

# 2. Tworzenie paska bocznego (Sidebar)
st.sidebar.header("⚙️ Ustawienia wykresu")
st.sidebar.write("Przesuń suwak, aby zmienić dane:")
# Magiczny suwak, który zwraca liczbę do zmiennej "dni"
dni = st.sidebar.slider("Liczba dni do analizy", min_value=10, max_value=365, value=100)

# 3. Generowanie sztucznych danych (symulacja cen akcji)
# Tworzymy 3 kolumny z losowymi liczbami, które sumują się w czasie
dane = pd.DataFrame(
    np.random.randn(dni, 3).cumsum(axis=0),
    columns=['Apple 🍏', 'Google 🔍', 'Microsoft 🪟']
)

# 4. Wyświetlanie na ekranie
col1, col2 = st.columns([1, 2]) # Dzielimy ekran na dwie nierówne kolumny

with col1:
    st.subheader("Surowe dane")
    st.dataframe(dane, height=400) # Streamlit sam robi przewijaną tabelę!

with col2:
    st.subheader(f"Wykres z ostatnich {dni} dni")
    st.line_chart(dane) # Streamlit sam rysuje piękny, interaktywny wykres

st.success("Wyobraź sobie, że to są Twoje wydatki z podziałem na kategorie!")