import sqlite3
from datetime import datetime

# Connect to SQLite database (or create it if it doesn't exist)
def connect_db():
    conn = sqlite3.connect("invoices.db")
    return conn

# Create invoices table if not exists
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT UNIQUE,
            date TEXT,
            vendor TEXT,
            total_amount REAL
        )
    """)
    conn.commit()
    conn.close()

# Insert validated invoice record
def insert_invoice(invoice_number, date, vendor, total_amount):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO invoices (invoice_number, date, vendor, total_amount)
            VALUES (?, ?, ?, ?)
        """, (invoice_number, date, vendor, total_amount))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Duplicate Invoice Number!"
    finally:
        conn.close()
    return "Inserted Successfully!"

# Fetch all records
def fetch_invoices():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM invoices")
    records = cursor.fetchall()
    conn.close()
    return records


def get_invoice_count():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM invoices")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_total_sales():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(total_amount) FROM invoices")
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0

def get_recent_invoices(limit=5):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM invoices ORDER BY id DESC LIMIT ?", (limit,))
    records = cursor.fetchall()
    conn.close()
    return records

