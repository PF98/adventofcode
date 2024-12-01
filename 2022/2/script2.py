FILE_NAME = "example"
FILE_NAME = "input"

MAPS = [
    {
        "A": 1, # rock
        "B": 2, # paper
        "C": 3, # scissor
    },
    {
        "X": 1, # rock
        "Y": 2, # paper
        "Z": 3, # scissor
    }
]
    
CHOICE_MAP = {
    1: lambda opp: (opp + 2 - 1) % 3 + 1, # lose
    2: lambda opp: opp, # draw
    3: lambda opp: (opp + 1 - 1) % 3 + 1, # win
}


def scores(opp, you):
    if opp == you:
        return 3
    
    if (opp + 1) % 3 == you % 3:
        return 6
    
    return 0

def scores2(opp, you):
    chosen = CHOICE_MAP[you](opp)
    return scores(opp, chosen) + chosen

with open(FILE_NAME) as file:
    lst = [tuple(MAPS[i][a.strip()] for i,a in enumerate(line.split(" "))) for line in file]
    
    scrs = [scores(*t) + t[1] for t in lst]
    
    #chunks = sorted(sum(int(n) for n in g) for k,g in groupby(lst, key=lambda x: len(x) > 0) if k)
    
    print("Part One: What would your total score be if everything goes exactly according to your strategy guide?")
    print(sum(scrs))
    
    
    
    scrs2 = [scores2(*t) for t in lst]
    
    print()
    print("Following the Elf's instructions for the second column, what would your total score be if everything goes exactly according to your strategy guide?")
    print(sum(scrs2))
