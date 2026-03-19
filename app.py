import streamlit as st
import sqlite3
import pandas
from datetime import date

st.title("💸 Mój Tracker Wydatków")
try:
    connection = sqlite3.connect('expenses.db')
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute('''
        CREATE table if not exists kategorie(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nazwa TEXT unique
        );
    ''')
    cursor.execute('''
            CREATE table if not exists wydatki(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_wydatku TEXT,
            kwota REAL check(kwota>0),
            kategoria_id INTEGER references kategorie(id),
            opis TEXT
            );
        ''')

    domyslne_kategorie = ['Jedzenie', 'Transport', 'Rozrywka', 'Rachunki', 'Inne']
    for kat in domyslne_kategorie:
        cursor.execute("INSERT OR IGNORE INTO kategorie (nazwa) VALUES (?)", (kat,))

    connection.commit()
except sqlite3.Error as error:
    st.error(f'Błąd bazy danych: {error}')
