# Models

Parametric sources for the product line. Every part is a rounded plate plus
raised text, so every part is one filament change away from looking two-colour.

## Generating an order

```bash
openscad -o dennis.stl -D 'name="DENNIS"' name_sign.scad
openscad -o anna.stl   -D 'name="ANNA"'   keychain.scad
openscad -o rex.stl    -D 'name="REX"' -D 'line2="+358 40 123 4567"' pet_tag.scad
openscad -o mum.stl    -D 'name="MUM"' -D 'year="2026"' ornament.scad

# a whole plate in one run
openscad -o plate.stl -D 'names=["ANNA","BEN","CARLA","DEV","ELENA","FINN"]' batch.scad
```

Every file echoes its finished size and the layer to pause at:

```
ECHO: "Name sign: 89.736 x 32 x 3.8 mm | swap filament before layer 16 (Z = 3 mm)"
```

The round parts shrink their text to fit, so a nine-letter name still lands
inside the rim. The rectangular parts grow instead, so the text size stays
consistent across a set.

## The filament change

This is the whole no-AMS trick, and it takes thirty seconds.

1. Slice the STL in Bambu Studio with the standard A1 PLA profile.
2. Right-click the layer slider at the layer the file reported — the first
   layer of the raised text — and choose **Add filament change**.
3. Print. The A1 parks and prompts you.
4. Pull the old filament, push the new one in, purge until the colour runs
   clean, resume.
5. Watch the first swapped layer go down. If the old colour is still bleeding
   through, purge more — that is the only failure mode this workflow has.

On a batch plate every sign changes colour at the same Z, so one pause serves
twenty parts. That is the economics: an AMS farm burns 20–40% of its filament
on purge towers to do what one interruption does here.

## Print settings

| | |
|---|---|
| Nozzle / layer | 0.4 mm / 0.2 mm |
| Plate | Textured PEI — the matte finish is what makes these look bought |
| Walls / infill | 3 walls, 15% — these are flat plates, nothing structural |
| Supports | None. Nothing here overhangs. |
| Material | PLA for indoors, PETG for anything facing sun, rain or a car |
| Spacing on a batch plate | 6 mm, set by `gap` in `batch.scad` |

## Fonts

The plate sizing uses a table of measured glyph advances for **Liberation Sans
Bold**, because OpenSCAD 2021 cannot measure a rendered string. Change the font
and that table goes stale — plates come out too wide, or the text hangs off the
edge.

To re-measure for a new font, render `"HxH"` against `"HH"` at size 100 for each
character and divide the difference by 100. That is exactly how `ADV_VALS` in
`lib/plate.scad` was built.

## Licensing

Everything in this folder is original geometry, so it is yours to sell. That is
not true of most models you download: Printables and Thingiverse default to
CC-BY-**NC**, which forbids exactly what this business does. Check every model
before it goes on the stall, and never print fan art for sale.
