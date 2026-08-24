// ---------------------------------------------------------------------------
// pet_tag.scad — pet tag or plant marker, sold ten to a batch.
//
//   openscad -o rex.stl -D 'name="REX"' -D 'line2="+358 40 123 4567"' pet_tag.scad
//
// Batch of 10 sells for ~€12 at ~22 g and ~1.1 h.
// Print in PETG if it lives outdoors — PLA goes brittle in UV.
// ---------------------------------------------------------------------------
include <lib/plate.scad>

name        = "REX";
line2       = "";                 // optional second line: a phone number, a species
font        = "Liberation Sans:style=Bold";
text_size   = 7;
line2_size  = 4;
base_h      = 2.2;
text_h      = 0.6;
dia         = 32;
hole_d      = 3.5;
hole_inset  = 4;                  // from the rim to the hole centre
layer_h     = 0.2;
part        = "all";

module body() {
    difference() {
        cylinder(h = base_h, d = dia);
        hang_hole(0, dia / 2 - hole_inset, 0, hole_d, base_h);
    }
}

y_main  = (line2 == "") ? -1 : 2.5;
y_line2 = -5.5;

// A disc narrows away from its centre, so fit each line to its own chord.
function chord(y) = 2 * sqrt(max(pow(dia / 2, 2) - pow(abs(y) + 4, 2), 1)) - 3;
main_size  = fit_size(name,  text_size,  chord(y_main));
line2_fit  = fit_size(line2, line2_size, chord(y_line2));

if (part == "all" || part == "base") body();
if (part == "all" || part == "text") {
    translate([0, y_main, 0]) raised_text(name, main_size, text_h, base_h, font);
    if (line2 != "")
        translate([0, y_line2, 0]) raised_text(line2, line2_fit, text_h, base_h, font);
}

report("Pet tag", dia, dia, base_h, text_h, layer_h);
