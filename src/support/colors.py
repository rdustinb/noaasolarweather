# All of the other colors available that can be used in go.Scatter(line=dict(color=***))
# "aliceblue", "antiquewhite", "azure",
# "black", "blanchedalmond", 
# "burlywood", "cadetblue",
# "chartreuse", "chocolate",
# "cornsilk", "cyan", "darkcyan",
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
# "lime",
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
    "blue": ["blue", "darkblue", "lightblue", "mediumblue", "deepskyblue", "lightskyblue", "skyblue", "powderblue", "dodgerblue", "royalblue", "steelblue", "lightsteelblue", "slateblue", "cornflowerblue"],
    "green": ["green", "darkgreen", "lightgreen", "lawngreen", "olivedrab", "yellowgreen", "limegreen", "mediumspringgreen", "springgreen", "lightseagreen", "seagreen", "mediumseagreen", "darkseagreen"],
    "purple": ["purple", "mediumpurple", "rebeccapurple", "plum", "magenta", "maroon", "fuchsia", "lavender", "lavenderblush"],
    "turquoise": ["turquoise", "darkturquoise", "paleturquoise", "mediumturquoise", "aqua", "aquamarine", "teal"],
    "violet": ["violet", "darkviolet", "blueviolet", "mediumvioletred", "palevioletred", "orchid", "mediumorchid", "darkorchid"],
    "red": ["red", "darkred", "indianred", "crimson", "orangered", "mistyrose"],
    "yellow": ["yellow", "lightyellow", "greenyellow", "goldenrod", "darkgoldenrod", "lightgoldenrodyellow", "palegoldenrod", "lemonchiffon"],
    "gray": ["gray", "darkgray", "lightgray", "slategray", "darkslategray", "lightslategray"]
};

colorsUsed = list()

DEBUG = False

def initColors():
    colorsUsed = list()

def getColorSet(setSize: int):
    if DEBUG:
        print("\nColors used list is: %s"%(colorsUsed))
        print("Requested set size is: %d"%(setSize))
        print("Type of setSize is %s"%(type(setSize)))
        print("Type of len(allColors[thisColorKey]) is %s"%(type(len(allColors["red"]))))
        for thisColorKey in sorted(allColors, key=lambda thisKey: len(allColors[thisKey])):
            if thisColorKey not in colorsUsed:
                print("Key: %s, Number of Elements: %d"%(thisColorKey, len(allColors[thisColorKey])))
    #for thisColorKey in allColors:
    for thisColorKey in sorted(allColors, key=lambda thisKey: len(allColors[thisKey])):
        if thisColorKey in colorsUsed:
            if DEBUG:
                print("Color key is contained in the colorsUsed list, skipping...")
            next
        else:
            thisColorcount = len(allColors[thisColorKey])
            # If the number of colors available is the same or greater than those needed, return this color list
            if thisColorcount >= setSize:
                colorsUsed.append(thisColorKey)
                if DEBUG:
                    print("Returning the color list %s"%(thisColorKey))
                    print("Color list has an element count of %d"%(len(allColors[thisColorKey])))
                return allColors[thisColorKey]

