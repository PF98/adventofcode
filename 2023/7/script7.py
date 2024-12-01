FILE_NAME = "example"
FILE_NAME = "input"

with open(FILE_NAME) as file:
    lst = [line.strip().split(" ") for line in file]


from collections import Counter

CARD_VALUE = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
def mapCardValue(c):
    if "2" <= c <= "9":
        return int(c)
    
    return CARD_VALUE[c]

CARD_VALUE2 = {"T": 10, "J": 0, "Q": 12, "K": 13, "A": 14}
def mapCardValue2(c):
    if "2" <= c <= "9":
        return int(c)
    return CARD_VALUE2[c]
    
    
# VALUES:
# High Card: 1
# One Pair: 2
# Two Pairs: 3
# Three of a Kind: 4
# Full House: 5
# Four of a Kind: 6
# Five of a Kind: 7
def handValue(cards):
    cards = [mapCardValue(c) for c in cards]

    valueCounts = Counter(cards)
    revCounts = {v: k for k,v in valueCounts.items()}
    
    # FIVE OF A KIND
    if 5 in revCounts:
        return (7, *cards)
    
    # FOUR OF A KIND (POKER)
    if 4 in revCounts:
        return (6, *cards)
    
    if 3 in revCounts:
        # FULL HOUSE
        if 2 in revCounts:
            return (5, *cards)
        # THREE OF A KIND
        else:
            return (4, *cards)
    
    # PAIRS:
    if 2 in revCounts:
        # TWO PAIRS 
        if sum(1 for v in valueCounts.values() if v == 2) == 2:
            return (3, *cards)
        
        # ONE PAIR
        return (2, *cards)
    
    # HIGH CARD
    return (1, *cards)

def handValue2(cards):
    cards = [mapCardValue2(c) for c in cards]

    valueCounts = Counter(cards)
    
    if CARD_VALUE2["J"] in valueCounts:
        jacks = valueCounts[CARD_VALUE2["J"]]
        # if only jacks: keep it as is
        # if there are other cards: turn all of the jacks into one of the cards 
        # that is present the most times
        if jacks < 5:
            del valueCounts[CARD_VALUE2["J"]]
            maxv = max(valueCounts.values())
            
            for k,v in valueCounts.items():
                if v != maxv:
                    continue
                valueCounts[k] += jacks
                break
    
            
    revCounts = {v: k for k,v in valueCounts.items()}
        
    
    # FIVE OF A KIND
    if 5 in revCounts:
        return (7, *cards)
    
    # FOUR OF A KIND (POKER)
    if 4 in revCounts:
        return (6, *cards)
    
    if 3 in revCounts:
        # FULL HOUSE
        if 2 in revCounts:
            return (5, *cards)
        # THREE OF A KIND
        else:
            return (4, *cards)
    
    # PAIRS:
    if 2 in revCounts:
        # TWO PAIRS 
        if sum(1 for v in valueCounts.values() if v == 2) == 2:
            return (3, *cards)
        
        # ONE PAIR
        return (2, *cards)
    
    # HIGH CARD
    return (1, *cards)





print("Part One:")
print(sum(n*int(v) for n,(_,v) in enumerate(sorted(lst, key = lambda t: handValue(t[0])), start=1)))

print()
print("Part Two:")
print(sum(n*int(v) for n,(_,v) in enumerate(sorted(lst, key = lambda t: handValue2(t[0])), start=1)))
