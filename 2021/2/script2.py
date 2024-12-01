FUNC_MAP_1 = {
    "forward": lambda pos, x : (pos[0] + x, pos[1]),
    "down": lambda pos, x : (pos[0], pos[1] + x),
    "up": lambda pos, x : (pos[0], pos[1] - x)
}
FUNC_MAP_2 = {
    "forward": lambda pos, x : {
        "h": pos["h"] + x,
        "v": pos["v"] + pos["aim"] * x,
        "aim": pos["aim"]
    },
    "down": lambda pos, x : {
        "h": pos["h"],
        "v": pos["v"],
        "aim": pos["aim"] + x
    },
    "up": lambda pos, x : {
        "h": pos["h"],
        "v": pos["v"],
        "aim": pos["aim"] - x
    },
}


FILE_NAME = "example"
FILE_NAME = "input"

with open(FILE_NAME) as file:
    course = [line.split(" ") for line in file]
    pos1 = (0,0)
    pos2 = {"h": 0, "v": 0, "aim": 0}
    for data in course:
        pos1 = FUNC_MAP_1[data[0]](pos1, int(data[1]))
        pos2 = FUNC_MAP_2[data[0]](pos2, int(data[1]))
        
    print("Part One: What do you get if you multiply your final horizontal position by your final depth?")
    print(pos1[0] * pos1[1])
    
    print()
    print("Part Two: What do you get if you multiply your final horizontal position by your final depth?")
    print(pos2["h"] * pos2["v"])
    
    
    
    
