# -*- coding: utf-8 -*-
import matplotlib.colors as clrs

colors_blacklist = [
    "whitesmoke",
    "white",
    "snow",
    "mistyrose",
    "seashell",
    "linen",
    "bisque",
    "antiquewhite",
    "blanchedalmond",
    "papayawhip",
    "wheat",
    "oldlace",
    "floralwhite",
    "cornsilk",
    "lemonchiffon",
    "aliceblue",
    "ivory",
    "beige",
    "lightyellow",
    "lightgoldenrodyellow",
    "honeydew",
    "mintcream",
    "azure",
    "lightcyan",
    "aliceblue",
    "ghostwhite",
    "lavender",
    "lavenderblush",
]

color_list = []
for name, hex in clrs.cnames.items():
    if name not in colors_blacklist:
        color_list.append(name)
