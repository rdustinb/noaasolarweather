# All of the other colors available that can be used in go.Scatter(line=dict(color=***))
# "aliceblue", "antiquewhite", "azure",
# "black", "blanchedalmond", 
# "burlywood", "cadetblue",
# "chartreuse", "chocolate",
# "cornsilk", "crimson", "cyan", "darkcyan",
# "darkgrey",
# "darkmagenta", "darkolivegreen", 
# "darkslateblue", "darkslategrey",
# "deeppink",
# "dimgray", "dimgrey", "firebrick",
# "floralwhite", "forestgreen", "gainsboro",
# "ghostwhite", "gold", "grey", "hotpink", "indigo",
# "ivory", 
# "lightcyan",
# "lightgrey",
# "lightpink",
# "lightslategrey",
# "lightsteelblue", "lime",
# "linen", "mediumaquamarine",
# "mediumslateblue",
# "midnightblue",
# "mintcream", "moccasin", "navajowhite", "navy",
# "oldlace", "olive", "palegreen", 
# "pink",
# "sienna", "silver",
# "slategrey", "snow",
# "tan", "thistle", "tomato",
# "wheat", "white", "whitesmoke",

# A dictionary of lists whose base color is used as the key
allColors = {
    "brown": ["brown", "rosybrown", "saddlebrown", "sandybrown", "bisque", "khaki", "darkkhaki"],
    "orange": ["orange", "darkorange", "peachpuff", "salmon", "darksalmon", "lightsalmon", "coral", "lightcoral"],
    "blue": ["blue", "darkblue", "lightblue", "mediumblue", "deepskyblue","lightskyblue", "skyblue", "powderblue", "dodgerblue", "royalblue", "steelblue", "slateblue", "cornflowerblue"],
    "green": ["green", "darkgreen", "lightgreen", "lawngreen", "olivedrab", "yellowgreen", "limegreen", "mediumspringgreen", "springgreen", "lightseagreen", "seagreen", "mediumseagreen", "darkseagreen"],
    "purple": ["purple", "mediumpurple", "rebeccapurple", "plum", "magenta", "maroon", "fuchsia", "lavender", "lavenderblush"],
    "turquoise": ["turquoise", "darkturquoise", "paleturquoise", "mediumturquoise", "aqua", "aquamarine", "teal"],
    "violet": ["violet", "darkviolet", "blueviolet", "mediumvioletred", "palevioletred", "orchid", "mediumorchid", "darkorchid"],
    "red": ["red", "darkred", "indianred", "orangered", "mistyrose"],
    "yellow": ["yellow", "lightyellow", "greenyellow", "goldenrod", "darkgoldenrod", "lightgoldenrodyellow", "palegoldenrod", "lemonchiffon"],
    "gray": ["gray", "darkgray", "lightgray", "slategray", "darkslategray", "lightslategray"]
};

colorsUsed = list()

DEBUG = False

def initColors():
    colorsUsed = list()

def getColorSet(setSize):
    if DEBUG:
        print("\nRequested set size is: %d"%(setSize))
        for thisColorKey in sorted(allColors, key=lambda thisKey: len(allColors[thisKey])):
            if thisColorKey not in colorsUsed:
                print("Key: %s, Number of Elements: %d"%(thisColorKey, len(allColors[thisColorKey])))
    #for thisColorKey in allColors:
    for thisColorKey in sorted(allColors, key=lambda thisKey: len(allColors[thisKey])):
        if thisColorKey in colorsUsed:
            next
        else:
            # If the number of colors available is the same or greater than those needed, return this color list
            if len(allColors[thisColorKey]) >= setSize:
                colorsUsed.append(thisColorKey)
                return allColors[thisColorKey]

