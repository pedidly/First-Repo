// ---------------------------------------------------------------------------
// name_sign.scad — the flagship SKU. Desk or door sign, two colours, one pause.
//
//   openscad -o dennis.stl -D 'name="DENNIS"' name_sign.scad
//
// Sells for ~€22. Prints in ~2.3 h and ~45 g at the default size.
// ---------------------------------------------------------------------------
include <lib/plate.scad>

name        = "DENNIS";           // the only thing most orders change
font        = "Liberation Sans:style=Bold";
text_size   = 14;                 // mm
base_h      = 3.0;                // colour 1 thickness
text_h      = 0.8;                // colour 2 thickness — 4 layers at 0.2 mm
pad         = 9;                  // margin around the text
corner_r    = 3;
min_width   = 60;
layer_h     = 0.2;                // only used to report the pause layer
part        = "all";              // "all" | "base" | "text"

name_sign(name, text_size, base_h, text_h, pad, corner_r, min_width, font, part);

report("Name sign", plate_width(name, text_size, pad, min_width),
       text_size + 2 * pad, base_h, text_h, layer_h);
