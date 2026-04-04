import sqlite3
import pandas
import pandas as pd
from src.categories import Category


class DatabaseManager:

    db_path : str
    conn : sqlite3.connect
    def wypisz(self):
        print("siemka")
    def __init__ (self,db_path : str ):
        self.db_path  = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute('PRAGMA foreign_keys = ON')
        self.init_db()

    def init_db (self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS categories(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_name TEXT UNIQUE
                );
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS expenses(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    expense_date TEXT,
                    amount REAL CHECK(amount > 0),
                    id_category INTEGER  NOT NULL REFERENCES categories(id),
                    description TEXT
                );
            ''')

            for kat in Category:
                self.conn.execute(
                    "INSERT OR IGNORE INTO categories (category_name) VALUES (?)",
                    (kat.value,)
                )

    def get_categories(self):
        cursor = self.conn.execute('SELECT category_name FROM categories')
        return [row[0] for row in cursor.fetchall()]

    def add_expense(self, date : str, amount: float, category : Category, description : str) -> None:
        with self.conn:
            self.conn.execute('''
                INSERT into expenses (expense_date,amount,id_category,description) VALUES 
                (?,?, (SELECT id FROM categories WHERE category_name = ?),?)
            ''',(date,amount,category.value,description))


    def get_expenses(self, start_date: str = None, end_date : str = None, category: Category = None) -> pd.DataFrame:
        query = '''
        SELECT e.id, e.expense_date, e.amount, c.category_name, e.description 
        FROM expenses e 
        JOIN categories c on e.id_category = c.id
        WHERE 1=1
        '''

        limitations = []

        if category:
            query += ' AND c.category_name = ?'
            limitations.append(category.value)
        if start_date:
            query +=  ' AND e.expense_date >= ?'
            limitations.append(start_date)
        if end_date:
            query += ' AND e.expense_date <= ?'
            limitations.append(end_date)

        query += ' ORDER BY e.expense_date DESC'
        return pd.read_sql_query(sql = query, con = self.conn ,params = limitations)

    def delete_expense (self, id_expense : int) -> None:
        with self.conn:
            self.conn.execute('''DELETE from expenses WHERE id = ?''', (int(id_expense),))











