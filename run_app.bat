@echo off
title Expense Tracker - ML Environment
echo [1/3] Przygotowanie srodowiska...

:: 1. Ustawiamy sciezke do skryptu aktywacji Minicondy
set CONDA_ACTIVATE=C:\Users\jakub\miniconda3\Scripts\activate.bat

:: 2. Aktywujemy srodowisko 'ml' i uruchamiamy Streamlita
:: Uzywamy 'call', zeby skrypt nie zamknal sie po aktywacji condy
call %CONDA_ACTIVATE% ml

echo [2/3] Srodowisko 'ml' aktywne.
echo [3/3] Startuje Streamlit...

:: 3. Odpalenie aplikacji
streamlit run app.py

:: Jeśli coś pójdzie nie tak, okno zostanie otwarte, żebyś widział błędy
pause