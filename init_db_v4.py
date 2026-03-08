import sqlite3

conn = sqlite3.connect("hospital.db")
c = conn.cursor()

# USERS
c.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

# DEPARTMENTS
c.execute("""
CREATE TABLE departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    yearly_limit INTEGER DEFAULT 0
)
""")

# MEDICINES (партії)
c.execute("""
CREATE TABLE medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    series TEXT,
    expiry_date TEXT,
    location TEXT,
    quantity INTEGER,
    min_quantity INTEGER DEFAULT 0
)
""")

# RESERVATIONS (попередні резерви)
c.execute("""
CREATE TABLE reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER,
    status TEXT DEFAULT 'draft',
    created_at TEXT,
    FOREIGN KEY(department_id) REFERENCES departments(id)
)
""")

# RESERVATION ITEMS
c.execute("""
CREATE TABLE reservation_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reservation_id INTEGER,
    medicine_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY(reservation_id) REFERENCES reservations(id),
    FOREIGN KEY(medicine_id) REFERENCES medicines(id)
)
""")

# INVOICES
c.execute("""
CREATE TABLE invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT UNIQUE,
    department_id INTEGER,
    status TEXT DEFAULT 'issued',
    created_at TEXT,
    FOREIGN KEY(department_id) REFERENCES departments(id)
)
""")

# INVOICE ITEMS
c.execute("""
CREATE TABLE invoice_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER,
    medicine_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY(invoice_id) REFERENCES invoices(id),
    FOREIGN KEY(medicine_id) REFERENCES medicines(id)
)
""")

# AUDIT LOG
c.execute("""
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT,
    user TEXT,
    timestamp TEXT
)
""")

# Додаємо відділення
departments = [
    "Педіатрія",
    "Терапія",
    "Неврологія",
    "Хірургія",
    "Поліклініка",
    "Інфекція",
    "Приймальне"
]

for dep in departments:
    c.execute("INSERT INTO departments (name) VALUES (?)", (dep,))

# Додаємо користувачів
users = [
    ("admin", "123", "admin"),
    ("warehouse", "123", "warehouse"),
    ("pediatrics", "123", "department"),
    ("therapy", "123", "department"),
    ("neurology", "123", "department"),
    ("surgery", "123", "department"),
    ("clinic", "123", "department"),
    ("infection", "123", "department"),
    ("admission", "123", "department")
]

for user in users:
    c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", user)

conn.commit()
conn.close()

print("ERP база створена успішно.")