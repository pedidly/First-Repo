#!/usr/bin/env python3
"""Quote a print job the same way every time.

    python3 price.py 45 2.3                 # grams, print hours
    python3 price.py 45 2.3 --minutes 20 --fee 6.5
    python3 price.py --catalogue            # the standing product list

Machine time, not plastic, is what you are selling. The default rate covers
electricity, nozzle and plate wear, and the print that fails at hour seven --
because one will.
"""

import argparse

FILAMENT_EUR_PER_KG = 22.00
MACHINE_EUR_PER_HR = 2.00
LABOUR_EUR_PER_HR = 30.00
PACKAGING_EUR = 1.00
WASTE_FACTOR = 1.08          # purge on colour change, skirts, the odd reprint
SHIP_FLOOR_EUR = 8.00        # below this, postage and your time eat the margin
ASK_MULTIPLIER = 1.7         # what personalisation is worth on top of cost
CUSTOM_JOB_MINIMUM_EUR = 30.00

CATALOGUE = [
    # name,                        grams, hours, hands-on min, list price
    ("Replacement part, custom",      40,  2.0, 25, 35.00),
    ("Pet tags x10",                  22,  1.1, 10, 12.00),
    ("Keychains x5",                  28,  1.4, 10, 14.00),
    ("Table numbers x10, logo",      130,  5.5, 25, 55.00),
    ("Two-tone name sign",            45,  2.3, 12, 22.00),
    ("Ornament set x8",               70,  3.4, 15, 28.00),
    ("Wall mount",                    55,  2.6,  8, 16.00),
    ("Gridfinity drawer kit x16",    240,  9.5, 15, 42.00),
]


def quote(grams, hours, minutes=10.0, fee_pct=0.0,
          eur_per_kg=FILAMENT_EUR_PER_KG, multiplier=ASK_MULTIPLIER):
    """Return the cost breakdown, the cost floor, and the price to ask.

    The floor is what the job costs you. The ask is the floor times a
    personalisation multiplier, because the customer is paying for their name
    on the thing, not for 45 grams of PLA."""
    material = grams * (eur_per_kg / 1000.0) * WASTE_FACTOR
    machine = hours * MACHINE_EUR_PER_HR
    labour = minutes / 60.0 * LABOUR_EUR_PER_HR
    floor = material + machine + labour + PACKAGING_EUR

    fee_pct = min(max(fee_pct, 0.0), 59.0)
    price = floor * multiplier / (1 - fee_pct / 100.0)
    price = max(SHIP_FLOOR_EUR, round(price * 2 + 0.4999) / 2)  # up to nearest 50c

    fee = price * fee_pct / 100.0
    kept = price - fee - material - PACKAGING_EUR
    return {
        "material": material,
        "machine": machine,
        "labour": labour,
        "packaging": PACKAGING_EUR,
        "floor": floor,
        "fee": fee,
        "price": price,
        "per_print_hour": kept / hours if hours else 0.0,
        "margin_pct": (price - fee - material - PACKAGING_EUR) / price * 100 if price else 0.0,
    }


def print_quote(grams, hours, minutes, fee_pct, eur_per_kg, multiplier):
    q = quote(grams, hours, minutes, fee_pct, eur_per_kg, multiplier)
    print(f"\n  {grams:g} g / {hours:g} print hours / {minutes:g} min hands-on\n")
    for label, key in (("Material +8% waste", "material"), ("Machine time", "machine"),
                       ("Your time", "labour"), ("Packaging", "packaging")):
        print(f"    {label:<22} {q[key]:>8.2f}")
    print(f"    {'-' * 30}")
    print(f"    {'Cost floor':<22} {q['floor']:>8.2f}")
    if q["fee"]:
        print(f"    {'Marketplace fee':<22} {q['fee']:>8.2f}")
    print(f"\n    ASK (floor x {multiplier:g})       {q['price']:>8.2f}")
    print(f"    Return per print-hour  {q['per_print_hour']:>8.2f}")
    print(f"    Margin                 {q['margin_pct']:>7.1f}%\n")
    if hours and q["per_print_hour"] < 5:
        print("    Under EUR 5 per print-hour. The plate is worth more than this job.\n")


def print_catalogue(fee_pct, eur_per_kg):
    print(f"\n  {'Product':<28}{'g':>5}{'hrs':>6}{'cost':>8}{'list':>8}{'/hr':>8}{'margin':>8}")
    print("  " + "-" * 71)
    rows = []
    for name, grams, hours, minutes, list_price in CATALOGUE:
        q = quote(grams, hours, minutes, fee_pct, eur_per_kg)
        cost = q["material"] + q["packaging"]
        fee = list_price * fee_pct / 100.0
        kept = list_price - fee - cost
        rows.append((name, grams, hours, cost, list_price, kept / hours, kept / list_price * 100))
    for r in sorted(rows, key=lambda r: -r[5]):
        print(f"  {r[0]:<28}{r[1]:>5}{r[2]:>6.1f}{r[3]:>8.2f}{r[4]:>8.2f}{r[5]:>8.2f}{r[6]:>7.0f}%")
    plate_hours = sum(r[2] for r in rows)
    print("  " + "-" * 71)
    print(f"  {len(rows)} products, {plate_hours:.1f} print hours to make one of each\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("grams", nargs="?", type=float, help="part weight in grams")
    ap.add_argument("hours", nargs="?", type=float, help="print time in hours")
    ap.add_argument("--minutes", type=float, default=10.0, help="hands-on minutes (default 10)")
    ap.add_argument("--fee", type=float, default=0.0, help="marketplace fee %% (default 0)")
    ap.add_argument("--filament", type=float, default=FILAMENT_EUR_PER_KG,
                    help=f"filament price per kg (default {FILAMENT_EUR_PER_KG:.2f})")
    ap.add_argument("--multiplier", type=float, default=ASK_MULTIPLIER,
                    help=f"personalisation multiplier on the cost floor (default {ASK_MULTIPLIER})")
    ap.add_argument("--catalogue", action="store_true", help="show the standing product list")
    args = ap.parse_args()

    if args.catalogue:
        print_catalogue(args.fee, args.filament)
    elif args.grams is not None and args.hours is not None:
        print_quote(args.grams, args.hours, args.minutes, args.fee, args.filament,
                    args.multiplier)
    else:
        ap.print_help()
        print(f"\n  Reminder: custom jobs start at EUR {CUSTOM_JOB_MINIMUM_EUR:.0f}. No exceptions.\n")


if __name__ == "__main__":
    main()
