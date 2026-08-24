// ---------------------------------------------------------------------------
// ornament.scad — personalised flat ornament. The Q4 workhorse.
//
//   openscad -o mum.stl -D 'name="MUM"' -D 'year="2026"' ornament.scad
//
// Set of 8 sells for ~€28 at ~70 g and ~3.4 h.
// Flat means no supports and a full plate of them overnight.
// ---------------------------------------------------------------------------
include <lib/plate.scad>

name        = "MUM";
year        = "2026";             // set to "" to drop the year
font        = "Liberation Sans:style=Bold";
text_size   = 11;
year_size   = 5;
base_h      = 2.6;
text_h      = 0.8;
dia         = 70;
rim_w       = 3;                  // raised border, printed in the accent colour
hole_d      = 4;
hole_inset  = 6;
layer_h     = 0.2;
part        = "all";

module body() {
    difference() {
        cylinder(h = base_h, d = dia);
        hang_hole(0, dia / 2 - hole_inset, 0, hole_d, base_h);
    }
}

module rim() {
    translate([0, 0, base_h])
        linear_extrude(height = text_h)
            difference() {
                circle(d = dia - 4);
                circle(d = dia - 4 - 2 * rim_w);
            }
}

y_main = (year == "") ? -2 : 1;

// Keep both lines clear of the raised rim, however long the name is.
inner      = dia - 4 - 2 * rim_w - 6;
main_size  = fit_size(name, text_size, inner);
year_fit   = fit_size(year, year_size, inner);

if (part == "all" || part == "base") body();
if (part == "all" || part == "text") {
    rim();
    translate([0, y_main, 0]) raised_text(name, main_size, text_h, base_h, font);
    if (year != "")
        translate([0, -11, 0]) raised_text(year, year_fit, text_h, base_h, font);
}

report("Ornament", dia, dia, base_h, text_h, layer_h);
