"""Día del Pediatra - what is what in the PDF (paint-operator indices per
element) and the geometry measured on the flattened photos (fit.py), in PDF
points with the origin top-left."""

PAGES = {
    "s1": dict(page=1, groups={
        "bg": "0",
        "chinoin": "1-12",
        "grandes": "13-30",          # teal text + white glyph outlines + text again
        "dashes": "31-33",
        "line": "34",                # blue line above the card
        "contour": "35",             # blue outline of the card
        "surface": "36",             # turquoise card
        "pequenos": "37",
    }),
    "s2": dict(page=2, groups={
        "bg": "0",
        "octubre": "1",
        "chinoin": "2-13",
        "outline": "14,16",          # black contour around the pleca
        "pleca": "15",
        "dia": "17",
    }),
    "s3": dict(page=3, groups={
        "bg": "0",
        "zymir": "1-30",
        "sunderin": "31-252",
        "chinoin": "253-264",
        "gabirol": "265-272",
        "legend": "273",
        "balloon": "274-276,278",    # turquoise speech balloon (tail, sides, body)
        "outline": "277",            # purple contour
        "r1": "279", "r2": "280", "r3": "281", "r4": "282",
        "benel": "283-293",
    }),
}

# Curved edge of each photo: circle (cx, cy, R) of its outer edge (fit residual
# < 0.5 px) and the radial extent (inner, outer offset from R) of the coloured stroke
ARC = {"s1": (411.1, 519.5, 848.0), "s2": (274.4, 564.5, 872.4)}
ARC_BAND = {"s1": (-39.5, 1.5), "s2": (-11.5, 1.5)}

# Families of concentric white rings (centre, outermost radius) outside the photos
RINGS = {
    "s1": [((1911.9, -28.5), 360.0), ((1702.7, 1324.4), 620.0)],
    "s2": [((1912.6, 259.6), 590.0)],
    "s3": [((36.5, 96.3), 320.0), ((1703.2, 1009.6), 340.0)],
}

# Start points (pt) for drawn outlines: the stroke grows from here along its own shape
DRAW_FROM = {
    ("s1", "line"): (946, 520),
    ("s1", "contour"): (975, 436),
    ("s2", "outline"): (1045, 555),
    ("s3", "outline"): (160, 700),
}
# Tip of the speech balloon (pt): it grows from here
BALLOON_TIP = (452, 744)

# Per-glyph outline operators: their boxes split a text block into letters
GLYPH_OPS = {("s1", "grandes"): "14-29"}
