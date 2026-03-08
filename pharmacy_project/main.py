import json
import os
from datetime import datetime
from collections import defaultdict
from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import TableStyle
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

DATA_FILE = "data.json"


# ===================== ФАЙЛ =====================

def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "warehouse": {},
            "departments": {},
            "invoices": [],
            "invoice_counter": 1
        }
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# ===================== СКЛАД =====================

def add_batch(data):
    name = input("Назва препарату: ")
    qty = int(input("Кількість: "))
    expiry = input("Дата придатності (рррр-мм-дд): ")

    if name not in data["warehouse"]:
        data["warehouse"][name] = []

    data["warehouse"][name].append({
        "qty": qty,
        "expiry": expiry
    })

    save_data(data)
    print("✔ Партію додано")


def show_warehouse(data):
    print("\n===== СКЛАД =====")
    today = datetime.now()

    for name, batches in data["warehouse"].items():
        total = 0
        print(f"\n{name}")
        for batch in batches:
            exp = datetime.strptime(batch["expiry"], "%Y-%m-%d")
            days = (exp - today).days
            total += batch["qty"]

            if days < 0:
                status = "❌ ПРОСТРОЧЕНО"
            elif days < 30:
                status = "🔴 Менше 30 днів"
            elif days < 90:
                status = "🟡 Менше 90 днів"
            else:
                status = "🟢 Норма"

            print(f"  {batch['qty']} | {batch['expiry']} | {status}")

        print("Всього:", total)


# ===================== ВИДАЧА + PDF =====================

def issue_to_department(data):
    dep = input("Відділення: ")
    items = []

    while True:
        name = input("Назва препарату (або stop): ")
        if name == "stop":
            break

        if name not in data["warehouse"]:
            print("❌ Немає такого препарату")
            continue

        qty = int(input("Кількість: "))

        total_available = sum(b["qty"] for b in data["warehouse"][name])
        if qty > total_available:
            print("❌ Недостатньо")
            continue

        remaining = qty
        for batch in data["warehouse"][name]:
            if remaining == 0:
                break
            if batch["qty"] <= remaining:
                remaining -= batch["qty"]
                batch["qty"] = 0
            else:
                batch["qty"] -= remaining
                remaining = 0

        data["warehouse"][name] = [b for b in data["warehouse"][name] if b["qty"] > 0]

        items.append({"name": name, "qty": qty})

    if not items:
        return

    invoice_number = f"INV-{datetime.now().year}-{data['invoice_counter']:04}"
    data["invoice_counter"] += 1

    invoice = {
        "number": invoice_number,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "department": dep,
        "items": items
    }

    data["invoices"].append(invoice)
    save_data(data)

    generate_pdf(invoice)
    print(f"✔ Видано. Накладна {invoice_number}")


def generate_pdf(invoice):
    file_name = f"{invoice['number']}.pdf"
    doc = SimpleDocTemplate(file_name)
    elements = []

    elements.append(Paragraph(f"Накладна № {invoice['number']}", ParagraphStyle('h', fontSize=16)))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(f"Дата: {invoice['date']}", ParagraphStyle('n')))
    elements.append(Paragraph(f"Відділення: {invoice['department']}", ParagraphStyle('n')))
    elements.append(Spacer(1, 0.3 * inch))

    table_data = [["Препарат", "Кількість"]]

    for item in invoice["items"]:
        table_data.append([item["name"], str(item["qty"])])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.5 * inch))

    elements.append(Paragraph("Підпис складу: ____________________", ParagraphStyle('n')))
    elements.append(Paragraph("Підпис відділення: ________________", ParagraphStyle('n')))

    doc.build(elements)


# ===================== EXCEL РЕЄСТР =====================

def export_excel(data):
    wb = Workbook()
    ws = wb.active
    ws.append(["Номер", "Дата", "Відділення", "Препарат", "Кількість"])

    for inv in data["invoices"]:
        for item in inv["items"]:
            ws.append([
                inv["number"],
                inv["date"],
                inv["department"],
                item["name"],
                item["qty"]
            ])

    file_name = "invoice_registry.xlsx"
    wb.save(file_name)
    print("✔ Excel реєстр створено:", file_name)


# ===================== МЕНЮ =====================

def main():
    data = load_data()

    while True:
        print("""
1. Додати партію
2. Показати склад
3. Видати (накладна + PDF)
4. Excel реєстр накладних
5. Вийти
""")

        choice = input("Вибір: ")

        if choice == "1":
            add_batch(data)
        elif choice == "2":
            show_warehouse(data)
        elif choice == "3":
            issue_to_department(data)
        elif choice == "4":
            export_excel(data)
        elif choice == "5":
            break


main()