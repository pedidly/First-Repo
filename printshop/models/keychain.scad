// ---------------------------------------------------------------------------
// keychain.scad — personalised keychain, sold in sets of five.
//
//   openscad -o anna.stl -D 'name="ANNA"' keychain.scad
//
// Set of 5 sells for ~€14 at ~28 g and ~1.4 h for the whole set.
// ---------------------------------------------------------------------------
include <lib/plate.scad>

name        = "ANNA";
font        = "Liberation Sans:style=Bold";
text_size   = 8;
base_h      = 2.4;
text_h      = 0.6;                // 3 layers at 0.2 mm
pad         = 4;
corner_r    = 2.5;
min_width   = 26;
hole_d      = 4;                  // fits a standard split ring
hole_wall   = 2.5;
layer_h     = 0.2;
part        = "all";

ring_zone = hole_d + 2 * hole_wall;
text_w    = plate_width(name, text_size, pad, min_width);
w         = text_w + ring_zone;
d         = max(text_size + 2 * pad, ring_zone);
hole_x    = -w / 2 + ring_zone / 2;

module body() {
    difference() {
        rounded_plate(w, d, corner_r, base_h);
        hang_hole(hole_x, 0, 0, hole_d, base_h);
    }
}

if (part == "all" || part == "base") body();
if (part == "all" || part == "text")
    translate([ring_zone / 2, 0, 0])
        raised_text(name, text_size, text_h, base_h, font);

report("Keychain", w, d, base_h, text_h, layer_h);
