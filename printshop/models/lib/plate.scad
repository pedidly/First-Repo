// ---------------------------------------------------------------------------
// plate.scad — shared geometry for the two-tone product line.
// Every part in this folder is a rounded plate plus raised text, so the whole
// catalogue is one filament change away from looking multi-colour.
// ---------------------------------------------------------------------------

$fn = 64;

// Glyph advances for Liberation Sans Bold, in multiples of the text size.
// Measured by rendering "HxH" against "HH" at size 100, because OpenSCAD 2021
// cannot measure a string at runtime. Swap the font and these go stale — the
// plate grows or the text hangs off the edge, so re-measure if you change it.
ADV_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 -.,'&/#+";
ADV_VALS = [
    0.979, 0.979, 0.979, 0.979, 0.905, 0.828, 1.055, 0.979, 0.377, 0.754,
    0.979, 0.828, 1.130, 0.979, 1.055, 0.905, 1.055, 0.979, 0.905, 0.828,
    0.979, 0.905, 1.280, 0.905, 0.905, 0.828,
    0.754, 0.828, 0.754, 0.828, 0.754, 0.452, 0.828, 0.828, 0.377, 0.377,
    0.754, 0.377, 1.206, 0.828, 0.828, 0.828, 0.828, 0.528, 0.754, 0.452,
    0.828, 0.754, 1.055, 0.754, 0.754, 0.678,
    0.754, 0.754, 0.754, 0.754, 0.754, 0.754, 0.754, 0.754, 0.754, 0.754,
    0.377, 0.452, 0.377, 0.377, 0.323, 0.979, 0.377, 0.754, 0.792
];

// Unknown glyphs fall back to the widest measured advance, so an accent or a
// symbol makes the plate too big rather than too small.
function char_adv(c) = let (i = search(c, ADV_CHARS)) (i == [] ? 1.28 : ADV_VALS[i[0]]);

function text_width(txt, size, i = 0) =
    i >= len(txt) ? 0 : char_adv(txt[i]) * size + text_width(txt, size, i + 1);

function plate_width(txt, size, pad, min_w) =
    max(min_w, text_width(txt, size) + 2 * pad);

// Largest text size that fits a fixed-width space — used by the round parts,
// whose plate cannot simply grow to fit a long name.
function fit_size(txt, max_size, avail_w) =
    min(max_size, avail_w / max(text_width(txt, 1), 0.001));

// Layer the slicer must pause before, 1-indexed, for a given base height.
function pause_layer(base_h, layer_h) = floor(base_h / layer_h + 0.5) + 1;

module rounded_plate(w, d, r, h) {
    linear_extrude(height = h)
        offset(r = r)
            square([max(w - 2 * r, 0.01), max(d - 2 * r, 0.01)], center = true);
}

module raised_text(txt, size, h, z, font, spacing = 1.0) {
    translate([0, 0, z])
        linear_extrude(height = h)
            text(txt, size = size, font = font, spacing = spacing,
                 halign = "center", valign = "center");
}

module hang_hole(x, y, z, dia, h) {
    translate([x, y, z - 1])
        cylinder(h = h + 2, d = dia);
}

module report(label, w, d, base_h, text_h, layer_h) {
    echo(str(label, ": ", w, " x ", d, " x ", base_h + text_h,
             " mm  |  swap filament before layer ", pause_layer(base_h, layer_h),
             " (Z = ", base_h, " mm)"));
}

// The name sign lives here so that name_sign.scad and batch.scad build the
// identical part from one definition.
module name_sign(name, text_size = 14, base_h = 3.0, text_h = 0.8, pad = 9,
                 corner_r = 3, min_width = 60,
                 font = "Liberation Sans:style=Bold", part = "all") {
    w = plate_width(name, text_size, pad, min_width);
    d = text_size + 2 * pad;
    if (part == "all" || part == "base") rounded_plate(w, d, corner_r, base_h);
    if (part == "all" || part == "text") raised_text(name, text_size, text_h, base_h, font);
}
