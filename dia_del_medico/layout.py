"""What is what in the PDF: paint-operator indices of every element, per page,
and the hand-measured geometry (in PDF points, origin top-left) that the
animation follows: wave centre lines, frame paths, shield and cross."""

PAGES = {
    "s1": dict(page=1, groups={
        "bg": "0",
        "panel": "1",
        "frame": "2",
        "q1c": "3", "q1g": "4-7",          # opening quote: circle, glyphs
        "q2c": "8", "q2g": "9-12",         # closing quote
        # each line: its two soft shadows (Multiply) + the text itself
        "l1": "13,18,19", "l2": "14,20,21", "l3": "15,22,23",
        "l4": "16,24,25", "l5": "17,26,27",
        "chinoin": "28-39",
    }),
    "s2": dict(page=2, groups={
        "bg": "0",
        "panel": "1",
        "octubre": "2,3",
        "dia": "4,5",
        "chinoin": "6-17",
        "q2": "18,19",                     # closing quote (bottom right)
        "q1": "20,21",                     # opening quote (top left)
        "stroke_top": "22",
        "stroke_bot": "23",
        "n23": "24,25",
    }),
    "s3": dict(page=3, groups={
        "bg": "0",
        "zymir": "1-30",
        "chinoin": "31-42",
        "gabirol": "43-50",
        "legend": "51",
        "gracias": "52",
        "sunderin": "53-237",
        "proposito": "238",
        "salud": "239",
        "benel": "240-250",
    }),
}

# Centre lines of the turquoise dot waves, start -> end (direction of flow).
WAVES = {
    "s1": [(1530, -40), (1490, 150), (1440, 330), (1395, 520), (1340, 700),
           (1240, 870), (1100, 990), (950, 1120)],
    "s2": [(-40, 50), (110, 85), (230, 160), (320, 280), (400, 410), (500, 510),
           (640, 585), (800, 640), (980, 690), (1150, 730)],
    "s3": [(-40, 50), (90, 120), (210, 220), (330, 340), (460, 460), (590, 590),
           (720, 720), (880, 800), (1080, 850), (1350, 890), (1600, 950), (1800, 1010)],
}
# half width (pt) of the dot sheet around each centre line
WAVE_WIDTH = {"s1": 230, "s2": 150, "s3": 140}

# Page 1 white frame: centre line of the ring and where the stroke starts
# (under the opening quote) - half the perimeter later it is under the closing one.
FRAME1 = dict(rect=(883.9, 215.2, 1801.7, 863.8), start=(1046.0, 215.2))
# Page 2 frame strokes as drawn in the PDF (start -> end)
STROKE_TOP = [(168.6, 329.2), (1089.0, 329.2), (1089.0, 512.1)]
STROKE_BOT = [(778.2, 817.9), (124.5, 817.9), (124.5, 635.0)]

# Page 3 shield (flattened in the photo): soft region, cross arms, and the
# point where the incoming wave meets the shield network.
SHIELD = dict(center=(470, 540), radii=(400, 430), contact=(250, 290),
              outline=[(118, 250), (200, 226), (300, 200), (400, 176), (470, 166), (545, 176),
                       (640, 200), (740, 226), (835, 258), (838, 330), (828, 430), (808, 530),
                       (775, 630), (728, 725), (660, 810), (585, 880), (512, 935), (440, 885),
                       (350, 815), (268, 725), (205, 615), (160, 495), (132, 375)])
CROSS = dict(center=(477, 442), v=(437, 305, 519, 578), h=(335, 403, 613, 482))
