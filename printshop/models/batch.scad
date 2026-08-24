// ---------------------------------------------------------------------------
// batch.scad — fill the A1's 256 mm plate with one overnight run of orders.
//
//   openscad -o plate.stl -D 'names=["ANNA","BEN","CARLA","DEV"]' batch.scad
//
// One pause serves the whole plate: every sign changes colour at the same Z.
// That is the entire no-AMS advantage, expressed as a build plate.
// ---------------------------------------------------------------------------
include <lib/plate.scad>

names       = ["ANNA", "BEN", "CARLA", "DEV", "ELENA", "FINN"];
font        = "Liberation Sans:style=Bold";
text_size   = 14;
base_h      = 3.0;
text_h      = 0.8;
pad         = 9;
corner_r    = 3;
min_width   = 60;
gap         = 6;                  // between parts
bed         = 250;                // usable square, 3 mm short of the A1's 256
layer_h     = 0.2;

cell_w = max([for (n = names) plate_width(n, text_size, pad, min_width)]) + gap;
cell_d = text_size + 2 * pad + gap;
cols   = max(1, floor(bed / cell_w));
rows   = ceil(len(names) / cols);

for (i = [0 : len(names) - 1]) {
    col = i % cols;
    row = floor(i / cols);
    translate([(col - (cols - 1) / 2) * cell_w,
               ((rows - 1) / 2 - row) * cell_d, 0])
        name_sign(names[i], text_size, base_h, text_h, pad, corner_r, min_width, font);
}

echo(str("Batch: ", len(names), " signs, ", cols, " x ", rows,
         " grid, footprint ", cols * cell_w, " x ", rows * cell_d, " mm"));
if (rows * cell_d > bed)
    echo("WARNING: taller than the usable plate — split this into two runs.");
