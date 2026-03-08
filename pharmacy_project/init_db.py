import sqlite3

conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

# USERS
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

# MEDICINES
cursor.execute("""
CREATE TABLE medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

# BATCHES
cursor.execute("""
CREATE TABLE batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_id INTEGER,
    series TEXT,
    expiry_date TEXT,
    storage_place TEXT,
    quantity INTEGER,
    FOREIGN KEY (medicine_id) REFERENCES medicines(id)
)
""")

# INVOICES
cursor.execute("""
CREATE TABLE invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT,
    department TEXT,
    date TEXT,
    status TEXT
)
""")

# INVOICE ITEMS
cursor.execute("""
CREATE TABLE invoice_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER,
    batch_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (invoice_id) REFERENCES invoices(id),
    FOREIGN KEY (batch_id) REFERENCES batches(id)
)
""")

# Річний ліміт
cursor.execute("""
CREATE TABLE department_limits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department TEXT,
    medicine_id INTEGER,
    year INTEGER,
    yearly_limit INTEGER,
    FOREIGN KEY (medicine_id) REFERENCES medicines(id)
)
""")

conn.commit()
conn.close()

print("ERP база створена ✅")