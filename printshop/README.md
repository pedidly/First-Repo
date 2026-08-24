# Printshop

The working parts of the 3D printing side business: the models that make the
products, the tool that prices them, and the copy that sells them.

One Bambu A1, no AMS. The strategy that follows from that hardware is in the
[plan](https://claude.ai/code/artifact/ccab974e-fec8-4077-80d5-b5db2047b810);
this folder is what turns it into orders.

```
models/     parametric sources — a name and a colour pair is a whole product
pricing/    the costing tool and the workbook that tracks orders and months
sales/      listing copy, outreach scripts, and how to take an order safely
```

## The loop

1. **Order arrives.** Capture it with the questions in
   [`sales/order-form.md`](sales/order-form.md) — the exact text, pasted, and a
   real date.
2. **Price it.** `python3 pricing/price.py 45 2.3 --minutes 12` gives the cost
   floor and the price to ask. Custom jobs start at €30, always.
3. **Generate it.** `openscad -o anna.stl -D 'name="ANNA"' models/name_sign.scad`
4. **Batch it.** Hold orders until you can fill a plate, then run
   `models/batch.scad` overnight. One pause colours the whole plate.
5. **Log it.** A row in the Orders sheet of `pricing/printshop.xlsx`. The Month
   sheet adds it up and compares against the target.

## Setup

```bash
sudo apt install openscad          # or brew install --cask openscad
pip3 install openpyxl              # only to regenerate the workbook
python3 pricing/make_workbook.py   # rebuilds printshop.xlsx from scratch
python3 pricing/price.py --catalogue
```

Regenerating the workbook overwrites it, so keep live orders in a copy.

## The numbers

Set once, in the Settings sheet of the workbook and at the top of `price.py`:

| | |
|---|---|
| Filament | €22/kg, +8% for purge and reprints |
| Machine time | €2.00/hr — power, wear, nozzles, plates, failed prints |
| Your time | €30/hr |
| Ask | cost floor × 1.7 — the customer is buying their name, not the plastic |
| Floors | €8 shipped, €30 for a custom job |

Change the filament price in the Settings sheet and the whole catalogue
reprices. Change it in `price.py` and the CLI follows.

## What matters

The catalogue is not the asset and neither is the printer. One customer who
needs parts every month — a workshop, a clinic, a club — is worth more than
every listing in `sales/`. The service listing and the walk-in script in
[`sales/outreach.md`](sales/outreach.md) are the two things in this folder that
find that customer. Everything else pays for filament while you look.
