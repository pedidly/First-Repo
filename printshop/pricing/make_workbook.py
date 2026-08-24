#!/usr/bin/env python3
"""Generate printshop.xlsx -- the costing sheet, order book, and month tally.

    python3 make_workbook.py

Regenerating overwrites the file, so keep your live orders in a copy, or edit
this script and rebuild. Every number in the workbook is a formula off the
Settings sheet: change the filament price there and the whole catalogue reprices.
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
import os

INK = "FF15191E"
ACCENT = "FFA65C08"
HEAD_FILL = PatternFill("solid", fgColor="FFE3E7EC")
ACCENT_FILL = PatternFill("solid", fgColor="FFF3E6D2")
THIN = Side(style="thin", color="FFC6CDD5")
BOX = Border(bottom=THIN)
H1 = Font(name="Calibri", size=13, bold=True, color=INK)
HEAD = Font(name="Calibri", size=9, bold=True, color="FF6E7883")
BODY = Font(name="Calibri", size=11)
NOTE = Font(name="Calibri", size=9, italic=True, color="FF6E7883")
EUR = '#,##0.00" EUR"'
PCT = '0%'

CATALOGUE = [
    ("Replacement part, custom", 40, 2.0, 25, 35.00, "Quote per job, 30 EUR minimum"),
    ("Pet tags x10", 22, 1.1, 10, 12.00, "PETG if it lives outdoors"),
    ("Keychains x5", 28, 1.4, 10, 14.00, "Silk gold letters on matte black"),
    ("Table numbers x10, logo", 130, 5.5, 25, 55.00, "Venues, weddings, cafes"),
    ("Two-tone name sign", 45, 2.3, 12, 22.00, "The flagship. One pause."),
    ("Ornament set x8", 70, 3.4, 15, 28.00, "Q4 workhorse, batch the plate"),
    ("Wall mount", 55, 2.6, 8, 16.00, "Headset, controller, tool"),
    ("Gridfinity drawer kit x16", 240, 9.5, 15, 42.00, "Check the licence first"),
]

STATUSES = "Quoted,Confirmed,Printing,Ready,Delivered,Paid,Cancelled"
CHANNELS = "Local classifieds,Facebook,Market stall,Repeat customer,Business order,Etsy,Word of mouth"


def style_header(ws, row, last_col):
    for c in range(1, last_col + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = HEAD
        cell.fill = HEAD_FILL
        cell.border = BOX
        cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = 26


def widths(ws, spec):
    for col, w in spec.items():
        ws.column_dimensions[col].width = w


def build_settings(ws):
    ws["A1"] = "Settings"
    ws["A1"].font = H1
    ws["A2"] = "Change a number here and the whole workbook reprices."
    ws["A2"].font = NOTE
    rows = [
        ("Filament price per kg", 22.00, EUR, "What you actually pay, delivered"),
        ("Waste factor", 1.08, "0.00", "Purge on colour change, skirts, reprints"),
        ("Machine rate per hour", 2.00, EUR, "Power, wear, nozzles, plates, failures"),
        ("Labour rate per hour", 30.00, EUR, "What your evening is worth"),
        ("Packaging per order", 1.00, EUR, "Box, bag, label"),
        ("Personalisation multiplier", 1.7, "0.00", "What the name on it is worth"),
        ("Minimum shipped price", 8.00, EUR, "Below this, postage eats it"),
        ("Custom job minimum", 30.00, EUR, "No exceptions, ever"),
    ]
    ws["A4"], ws["B4"], ws["C4"] = "Setting", "Value", "Why"
    style_header(ws, 4, 3)
    for i, (label, val, fmt, why) in enumerate(rows, start=5):
        ws.cell(row=i, column=1, value=label).font = BODY
        v = ws.cell(row=i, column=2, value=val)
        v.number_format = fmt
        v.font = Font(name="Calibri", size=11, bold=True, color=ACCENT)
        v.fill = ACCENT_FILL
        ws.cell(row=i, column=3, value=why).font = NOTE
    widths(ws, {"A": 30, "B": 16, "C": 44})
    return {label: f"Settings!$B${i}" for i, (label, *_ ) in enumerate(rows, start=5)}


def build_catalogue(ws, s):
    ws["A1"] = "Catalogue"
    ws["A1"].font = H1
    ws["A2"] = "Sort by return per print-hour. Kill anything that has not sold twice."
    ws["A2"].font = NOTE
    heads = ["Product", "Grams", "Print hrs", "Hands-on min", "Material", "Cost floor",
             "Suggested", "List price", "Per print-hr", "Margin", "Notes"]
    for c, h in enumerate(heads, start=1):
        ws.cell(row=4, column=c, value=h)
    style_header(ws, 4, len(heads))

    for i, (name, g, hrs, mins, price, note) in enumerate(CATALOGUE, start=5):
        ws.cell(row=i, column=1, value=name).font = BODY
        ws.cell(row=i, column=2, value=g)
        ws.cell(row=i, column=3, value=hrs)
        ws.cell(row=i, column=4, value=mins)
        ws.cell(row=i, column=5, value=f"=B{i}*{s['Filament price per kg']}/1000*{s['Waste factor']}")
        ws.cell(row=i, column=6,
                value=f"=E{i}+C{i}*{s['Machine rate per hour']}+D{i}/60*{s['Labour rate per hour']}+{s['Packaging per order']}")
        ws.cell(row=i, column=7,
                value=f"=MAX({s['Minimum shipped price']},CEILING(F{i}*{s['Personalisation multiplier']},0.5))")
        ws.cell(row=i, column=8, value=price)
        ws.cell(row=i, column=9, value=f"=IF(C{i}=0,0,(H{i}-E{i}-{s['Packaging per order']})/C{i})")
        ws.cell(row=i, column=10, value=f"=IF(H{i}=0,0,(H{i}-E{i}-{s['Packaging per order']})/H{i})")
        ws.cell(row=i, column=11, value=note).font = NOTE
        for col in (5, 6, 7, 8, 9):
            ws.cell(row=i, column=col).number_format = EUR
        ws.cell(row=i, column=10).number_format = PCT
        ws.cell(row=i, column=8).font = Font(name="Calibri", size=11, bold=True)

    last = 4 + len(CATALOGUE)
    ws.cell(row=last + 1, column=1, value="One of each").font = Font(size=10, bold=True)
    ws.cell(row=last + 1, column=2, value=f"=SUM(B5:B{last})")
    ws.cell(row=last + 1, column=3, value=f"=SUM(C5:C{last})")
    ws.cell(row=last + 1, column=8, value=f"=SUM(H5:H{last})").number_format = EUR
    widths(ws, {"A": 28, "B": 8, "C": 10, "D": 13, "E": 12, "F": 12, "G": 12,
                "H": 12, "I": 12, "J": 9, "K": 34})
    ws.freeze_panes = "A5"


def build_orders(ws, s):
    ws["A1"] = "Orders"
    ws["A1"].font = H1
    ws["A2"] = "One row per order. Fill columns A-I and the rest calculates."
    ws["A2"].font = NOTE
    heads = ["Date", "Order", "Customer", "Channel", "Product", "Qty", "Grams total",
             "Print hrs", "Price each", "Revenue", "Material", "Fee %", "Fee",
             "Profit", "Per print-hr", "Status", "Due", "Notes"]
    for c, h in enumerate(heads, start=1):
        ws.cell(row=4, column=c, value=h)
    style_header(ws, 4, len(heads))

    ROWS = 300
    for i in range(5, 5 + ROWS):
        ws.cell(row=i, column=10, value=f"=IF(F{i}=\"\",\"\",F{i}*I{i})")
        ws.cell(row=i, column=11,
                value=f"=IF(G{i}=\"\",\"\",G{i}*{s['Filament price per kg']}/1000*{s['Waste factor']})")
        ws.cell(row=i, column=13, value=f"=IF(J{i}=\"\",\"\",J{i}*L{i})")
        ws.cell(row=i, column=14,
                value=f"=IF(J{i}=\"\",\"\",J{i}-K{i}-M{i}-{s['Packaging per order']})")
        ws.cell(row=i, column=15, value=f"=IF(OR(H{i}=\"\",H{i}=0),\"\",N{i}/H{i})")
        for col in (9, 10, 11, 13, 14, 15):
            ws.cell(row=i, column=col).number_format = EUR
        ws.cell(row=i, column=12).number_format = PCT
        ws.cell(row=i, column=1).number_format = "yyyy-mm-dd"
        ws.cell(row=i, column=17).number_format = "yyyy-mm-dd"

    dv_status = DataValidation(type="list", formula1=f'"{STATUSES}"', allow_blank=True)
    dv_channel = DataValidation(type="list", formula1=f'"{CHANNELS}"', allow_blank=True)
    ws.add_data_validation(dv_status)
    ws.add_data_validation(dv_channel)
    dv_status.add(f"P5:P{4 + ROWS}")
    dv_channel.add(f"D5:D{4 + ROWS}")

    widths(ws, {"A": 12, "B": 8, "C": 20, "D": 18, "E": 26, "F": 6, "G": 12, "H": 10,
                "I": 11, "J": 12, "K": 11, "L": 7, "M": 10, "N": 11, "O": 12,
                "P": 13, "Q": 12, "R": 30})
    ws.freeze_panes = "C5"


def build_month(ws):
    ws["A1"] = "The month"
    ws["A1"].font = H1
    ws["A2"] = "Counts orders by their date. Paid and unpaid alike -- chase the gap."
    ws["A2"].font = NOTE
    heads = ["Month", "Orders", "Revenue", "Material", "Fees", "Profit", "Print hrs",
             "Per print-hr", "Target"]
    for c, h in enumerate(heads, start=1):
        ws.cell(row=4, column=c, value=h)
    style_header(ws, 4, len(heads))

    months = [("2026-09", "2026-09-01", "2026-10-01", 200),
              ("2026-10", "2026-10-01", "2026-11-01", 400),
              ("2026-11", "2026-11-01", "2026-12-01", 700),
              ("2026-12", "2026-12-01", "2027-01-01", 1200),
              ("2027-01", "2027-01-01", "2027-02-01", 350),
              ("2027-02", "2027-02-01", "2027-03-01", 350)]
    O = "Orders!"
    for i, (label, start, end, target) in enumerate(months, start=5):
        rng = lambda col: f'{O}${col}$5:${col}$304'
        crit = (f'{O}$A$5:$A$304,">="&DATE({int(start[:4])},{int(start[5:7])},1),'
                f'{O}$A$5:$A$304,"<"&DATE({int(end[:4])},{int(end[5:7])},1)')
        ws.cell(row=i, column=1, value=label).font = Font(name="Calibri", size=11, bold=True)
        ws.cell(row=i, column=2, value=f'=COUNTIFS({crit})')
        ws.cell(row=i, column=3, value=f'=SUMIFS({rng("J")},{crit})')
        ws.cell(row=i, column=4, value=f'=SUMIFS({rng("K")},{crit})')
        ws.cell(row=i, column=5, value=f'=SUMIFS({rng("M")},{crit})')
        ws.cell(row=i, column=6, value=f'=SUMIFS({rng("N")},{crit})')
        ws.cell(row=i, column=7, value=f'=SUMIFS({rng("H")},{crit})')
        ws.cell(row=i, column=8, value=f'=IF(G{i}=0,0,F{i}/G{i})')
        ws.cell(row=i, column=9, value=target)
        for col in (3, 4, 5, 6, 8, 9):
            ws.cell(row=i, column=col).number_format = EUR
    last = 4 + len(months)
    ws.cell(row=last + 1, column=1, value="Total").font = Font(size=10, bold=True)
    for col in (2, 3, 4, 5, 6, 7):
        L = get_column_letter(col)
        c = ws.cell(row=last + 1, column=col, value=f"=SUM({L}5:{L}{last})")
        if col > 2:
            c.number_format = EUR
    ws.cell(row=last + 3, column=1,
            value="If a Q4 month lands under 200 EUR with no repeat customer, "
                  "change the niche -- not the equipment.").font = NOTE
    widths(ws, {"A": 12, "B": 9, "C": 14, "D": 12, "E": 11, "F": 12, "G": 11,
                "H": 14, "I": 12})


def main():
    wb = Workbook()
    settings = build_settings(wb.active)
    wb.active.title = "Settings"
    build_catalogue(wb.create_sheet("Catalogue"), settings)
    build_orders(wb.create_sheet("Orders"), settings)
    build_month(wb.create_sheet("Month"))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "printshop.xlsx")
    wb.save(out)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
