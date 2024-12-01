from functools import reduce
import re
import math

FILE_NAME = "example"
FILE_NAME = "input"

TOKEN = "([A-Za-z]+)"
NUM = "(-?\d+)"

WEIGHT = 100

class Ingredient:
    def __init__(self, nums, calories):
        self.nums = nums
        self.calories = calories
        

def find(ingr, remWeight, totCals, amounts = []):
    used = len(amounts)
    #print(f"{'  ' * used}find with remaining weight: {remWeight}, amounts = ", end="")
    if remWeight == 0:
        amounts += [0] * (len(ingr) - used - 1)
        used = len(amounts)
    
    #print(amounts)
    
    # last ingredient: use all of the remaining weight
    if used == len(ingr) - 1:
        amounts.append(remWeight)
        nums = zip(*(ing.nums for ing in ingr))
        score = reduce(lambda a,b: a*b, (max(0, sum(amounts[i] * n for i,n in enumerate(ns))) for ns in nums))
        
        calories = sum(ing.calories * amounts[i] for i,ing in enumerate(ingr))

        #print(f"{'  ' * used} <- return score = {score}, calories = {calories}")
        return score, score if calories == totCals else None
        
    maxScore = None
    maxScoreCals = None
    for n in range(0,remWeight+1):
        score, scoreCals = find(ingr, remWeight - n, totCals, [*amounts, n])
        
        if maxScore is None or score > maxScore:
            maxScore = score
        
        if scoreCals is not None and (maxScoreCals is None  or scoreCals > maxScoreCals):
            maxScoreCals = scoreCals
    
    return maxScore,maxScoreCals


with open(FILE_NAME) as file:
    
    reindeers = []
    
    reindeersRes = []
    
    names = None
    
    ingr = []
    
    for line in file:
        m = re.match(f"{TOKEN}: {TOKEN} {NUM}, {TOKEN} {NUM}, {TOKEN} {NUM}, {TOKEN} {NUM}, {TOKEN} {NUM}", line)
        
        
        tokens = list(m.group(i) for i in range(1, 12))
        name = tokens[0]
        names = tokens[1::2]
        nums = [int(n) for n in tokens[2::2]]
        
        ingr.append(Ingredient(nums[:-1], nums[-1]))
        
        #print(ingr)
        
        
    score,scoreCals = find(ingr, WEIGHT, 500)
    
    print("Part One: Given the ingredients in your kitchen and their properties, what is the total score of the highest-scoring cookie you can make?")
    print(score)
    
    print()
    print("Part Two: Given the ingredients in your kitchen and their properties, what is the total score of the highest-scoring cookie you can make with a calorie total of 500?")
    print(scoreCals)
    
