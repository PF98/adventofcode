from functools import reduce
import re
import math

FILE_NAME = "example"
FILE_NAME = "input"

HP = 50
MANA = 500

#HP = 10
#MANA = 250
        

class Effect:
    lst = []
    cnt = 0
    def __init__(self, name, mana, dur):
        self.name = name
        self.mana = mana
        self.duration = dur
        self.num = Effect.cnt
        
        Effect.cnt += 1
        self.lst.append(self)
    
    def isUsable(self, game):
        return (not game.hasEffect(self.num)) and game.player.hasMana(self.mana)
    
    def spendMana(self, game):
        game.spendMana(self.mana)
    
    def apply(self, game):
        pass
    
    def startTurn(self, game):
        pass
    
    def end(self, game):
        pass
    
    def applyStr(self, game):
        pass
    def startTurnStr(self, game):
        pass
    def endStr(self, game):
        pass
    

class MagicMissile(Effect):
    MANA = 53
    TURNS = 0
    DAMAGE = 4
    
    def __init__(self):
        super().__init__("Magic Missile", self.MANA, self.TURNS)
        
        
    def apply(self, game):
        game.boss.changeHP(-self.DAMAGE)
    
    def applyStr(self, game):
        return f", dealing {self.DAMAGE} damage"


class Drain(Effect):
    MANA = 73
    TURNS = 0
    DAMAGE = 2
    HEAL = 2
    
    def __init__(self):
        super().__init__("Drain", self.MANA, self.TURNS)
        
        
    def apply(self, game):
        game.boss.changeHP(-self.DAMAGE)
        game.player.changeHP(self.HEAL)
    
    def applyStr(self, game):
        return f", dealing {self.DAMAGE} damage, and healing {self.HEAL} hit points"


class Shield(Effect):
    MANA = 113
    TURNS = 6
    ARMOR = 7
    
    def __init__(self):
        super().__init__("Shield", self.MANA, self.TURNS)
        
        
    def apply(self, game):
        game.player.changeArmor(self.ARMOR)

    
    def end(self, game):
        game.player.changeArmor(-self.ARMOR)
    
    
    def applyStr(self, game):
        return f", increasing armor by {self.ARMOR}"
    
    def endStr(self, game):
        return f", decreasing armor by {self.ARMOR}"
    
class Poison(Effect):
    MANA = 173
    TURNS = 6
    DAMAGE = 3
    
    def __init__(self):
        super().__init__("Poison", self.MANA, self.TURNS)
    
    
    def startTurn(self, game):
        game.boss.changeHP(-self.DAMAGE)
    
    def startTurnStr(self, game):
        return f" and it deals {self.DAMAGE} damage"


class Recharge(Effect):
    MANA = 229
    TURNS = 5
    NEWMANA = 101
    
    def __init__(self):
        super().__init__("Recharge", self.MANA, self.TURNS)
    
    
    def startTurn(self, game):
        game.player.changeMana(self.NEWMANA)
    
    def startTurnStr(self, game):
        return f" and it provides {self.NEWMANA} mana"
    


class Game:
    class Fighter:
        def __init__(self, hp, atk, arm, mana):
            self.hp = hp
            self.atk = atk
            self.arm = arm
            self.mana = mana
        
        def attacked(self, ext_atk):
            damage = max(ext_atk - self.arm, 1)
            self.changeHP(-damage)
        
        def changeHP(self, d):
            self.hp += d
        def changeAttack(self, d):
            self.atk += d
        def changeArmor(self, d):
            self.arm += d
        def changeMana(self, d):
            self.mana += d
            
        def isAlive(self):
            return self.hp > 0
        def hasMana(self, v):
            return self.mana >= v
        
        def clone(self):
            return Game.Fighter(self.hp, self.atk, self.arm, self.mana)
            
    # player: (hp, mana)
    def __init__(self):
        self.player = None
        self.boss = None
        self.totalMana = 0
        
        # will contain (Effect object, remaining turns)
        self.effects = [None] * len(Effect.lst)
    
    def hasEffect(self, effNum):
        if self.effects[effNum] is None:
            return False
        effObj, time = self.effects[effNum]
        return time > 0
    
    def putEffect(self, effObj):
        if self.effects[effObj.num] is not None:
            oldEffObj, oldTime = self.effects[effObj.num]
            if oldTime > 0:
                raise Exception(f"put effect {effObj.num} with oldTime > 0 (oldTime = {oldTime})")
            
            oldEffObj.end(self)
            
        
        self.spendMana(effObj.mana)
        effObj.apply(self)
        
        self.effects[effObj.num] = (effObj, effObj.duration)
    
    def startTurn(self):
        for i, obj in enumerate(self.effects):
            if obj is None:
                continue
            
            effObj, time = obj
            self.effects[i] = (effObj, time - 1)
            
            effObj.startTurn(self)
            
    
    def finishTurn(self):        
        for i, obj in enumerate(self.effects):
            if obj is None:
                continue
            
            effObj, time = obj
            
            if time == 0:
                effObj.end(self)
                self.effects[i] = None
    
    def spendMana(self, mana):
        self.totalMana += mana
        self.player.changeMana(-mana)
    
    def setPlayer(self, player):
        p_hp, p_mana = player
        self.player = self.Fighter(p_hp, 0, 0, p_mana)
        
    def setBoss(self, boss):
        b_hp, b_atk = boss
        self.boss = self.Fighter(b_hp, b_atk, 0, 0)
        
    def clone(self):
        out = Game()
        out.player = self.player.clone()
        out.boss = self.boss.clone()
        out.effects = [*self.effects]
        out.totalMana = self.totalMana
        return out
    
    def printData(self, turnName, depth):
        print(f"{'|   '*(depth-1)}--------")
        print(f"{'|   '*depth}-- {turnName} turn --")
        print(f"{'|   '*depth}- Player has {self.player.hp} hit points, {self.player.arm} armor, {self.player.mana} mana")
        print(f"{'|   '*depth}- Boss has {self.boss.hp} hit points, {self.boss.atk} attack")
    
    def printStartTurnEffects(self, depth):
        for i, obj in enumerate(self.effects):
            if obj is None:
                continue
            
            effObj, time = obj
            
            print(f"{'|   '*depth}{effObj.name}'s timer is now {time - 1}", end = "")
            eStr = effObj.startTurnStr(self)
            if eStr is not None:
                print(eStr, end = "")
            print(".")
            
    def printFinishTurnEffects(self, depth):        
        for i, obj in enumerate(self.effects):
            if obj is None:
                continue
            
            effObj, time = obj
            
            if time == 0 and effObj.duration > 0:
                print(f"{'|   '*depth}{effObj.name} wears off", end = "")
                eStr = effObj.endStr(self)
                if eStr is not None:
                    print(eStr, end = "")
                print(".")
                
 



def sumStats(*args):
    return tuple(sum(stats) for stats in zip(*args))


    
    
    
lowestMana = None
    
def battle(game, hard, startEstimate, playerTurn = True, depth = 1):
    global lowestMana
    
    # starting with the turn of the boss, since in it the player has no free choice
    if playerTurn:
        lowestMana = startEstimate
    else:
        # start of the turn: apply startTurn() effects
        game.startTurn()
        
        # the boss is dead
        if not game.boss.isAlive():
            return game.totalMana
        
        # the boss attacks
        game.player.attacked(game.boss.atk)
        
        # check if the player died => if they did, None indicates that no mana minimum for a win was reached
        if not game.player.isAlive():
            return None
        
        # apply end() effects
        game.finishTurn()
        
        # the boss is dead
        if not game.boss.isAlive():
            return game.totalMana
        
        if not game.player.isAlive():
            return None
        
    if hard:
        game.player.changeHP(-1)
        if not game.player.isAlive():
            return None
    
    
    # starting with the turn of the player: apply startTurn() effects
    game.startTurn()
    
    # the boss is dead
    if not game.boss.isAlive():
        return game.totalMana

    # choices for the player
    for effObj in Effect.lst:
        # not enough mana or too much
        if not effObj.isUsable(game):
            continue
        
        if lowestMana is not None and game.totalMana + effObj.mana >= lowestMana:
            continue
            pass
        recgame = game.clone()
        
        recgame.putEffect(effObj)
        
        if not recgame.boss.isAlive():
            if lowestMana is None or recgame.totalMana < lowestMana:
                lowestMana = recgame.totalMana
            continue
        
        recgame.finishTurn()
        
        if not recgame.boss.isAlive():
            if lowestMana is None or recgame.totalMana < lowestMana:
                lowestMana = recgame.totalMana
            continue

        
        nextLowest = battle(recgame, hard, startEstimate, False, depth + 1)
        if lowestMana is None or (nextLowest is not None and nextLowest < lowestMana):
            lowestMana = nextLowest
            
    return lowestMana


def battleCommented(game, hard, startEstimate, commentToDepth, playerTurn = True, depth = 1):
    global lowestMana
    # starting with the turn of the boss, since in it the player has no free choice
    if playerTurn:
        lowestMana = startEstimate
    else:
        print(lowestMana)
        lowestMana = startEstimate
        print(lowestMana)
        game.printData("Boss", depth)
        # start of the turn: apply startTurn() effects
        game.printStartTurnEffects(depth)
        game.startTurn()
        
        # the boss is dead
        if not game.boss.isAlive():
            print(f"{'|   '*depth}Boss is now dead.")
            print(f"{'|   '*depth} <- returning {game.totalMana}")
            return game.totalMana
        
        # the boss attacks
        game.player.attacked(game.boss.atk)
        print(f"{'|   '*depth}Boss attacks for {game.boss.atk}{f' - {game.player.arm} = {max(game.boss.atk - game.player.arm, 1)}' if game.player.arm > 0 else ''} damage!")
        
        # check if the player died => if they did, None indicates that no mana minimum for a win was reached
        if not game.player.isAlive():
            print(f"{'|   '*depth}Player is now dead. RIP in peace to them")
            print(f"{'|   '*(depth-1)}")
            return None
        
        # apply end() effects
        game.printFinishTurnEffects(depth)
        game.finishTurn()
        
        # the boss is dead
        if not game.boss.isAlive():
            print(f"{'|   '*depth}Boss is now dead.")
            print(f"{'|   '*depth} <- returning {game.totalMana}")
            return game.totalMana
        
        if not game.player.isAlive():
            print(f"{'|   '*depth}Player is now dead. RIP in peace to them")
            print(f"{'|   '*(depth-1)}")
            return None
        
    if hard:
        game.player.changeHP(-1)
        if not game.player.isAlive():
            return None
    
    
    game.printData("Player", depth)
    # starting with the turn of the player: apply startTurn() effects
    game.printStartTurnEffects(depth)
    game.startTurn()
    
    # the boss is dead
    if not game.boss.isAlive():
        print(f"{'|   '*depth}Boss is now dead.")
        print(f"{'|   '*depth} <- returning {game.totalMana}")
        return game.totalMana

    #lowestMana = None

    # choices for the player
    for effObj in Effect.lst:
        # not enough mana or too much
        if not effObj.isUsable(game):
            print(f"{'|   '*depth}!!! {effObj.name} is not usable")
            print(f"{'|   '*depth}!!! mana: {game.player.mana} -> hasMana: {game.player.hasMana(effObj.mana)}")
            print(f"{'|   '*depth}!!! effects: {game.effects} -> not hasEffect({effObj.num}): {not game.hasEffect(effObj.num)}")
            continue
        
        if lowestMana is not None and game.totalMana + effObj.mana >= lowestMana:
            print(f"{'|   '*depth}~~~ Skipping {effObj.name} since it costs {effObj.mana} mana and we already have a better alternative (lowestMana = {lowestMana})")
            continue
            pass
        recgame = game.clone()
        
        print(f"{'|   '*depth}Player casts {effObj.name}", end="")
        eStr = effObj.applyStr(recgame)
        if eStr is not None:
            print(eStr, end="")
        print(".")
        
        recgame.putEffect(effObj)
        
        if not recgame.boss.isAlive():
            print(f"{'|   '*depth}Boss is now dead.")
            if lowestMana is None or recgame.totalMana < lowestMana:
                lowestMana = recgame.totalMana
            continue
        
        recgame.printFinishTurnEffects(depth)
        recgame.finishTurn()
        
        if not recgame.boss.isAlive():
            print(f"{'|   '*depth}Boss is now dead.")
            if lowestMana is None or recgame.totalMana < lowestMana:
                lowestMana = recgame.totalMana
            continue

        if depth < commentToDepth:
            nextLowest = battleCommented(recgame, hard, startEstimate, commentToDepth, False, depth + 1)
        else:
            print(f"{'|   '*depth}...")
            print(f"{'|   '*depth}Skipping depth over {commentToDepth}")
            print(f"{'|   '*depth}...")
            print(f"{'|   '*depth}")
            nextLowest = battle(recgame, hard, startEstimate, False)
            
        if lowestMana is None or (nextLowest is not None and nextLowest < lowestMana):
            lowestMana = nextLowest
            
    print(f"{'|   '*depth} <- returning {lowestMana}")
    return lowestMana

with open(FILE_NAME) as file:
    # hp, atk, arm
    boss = tuple(int(line.strip().split(": ")[1]) for line in file)
    
    MagicMissile()
    Drain()
    Shield()
    Poison()
    Recharge()
    
    game = Game()
    game.setBoss(boss)
    game.setPlayer((HP, MANA))
    
    gameOrig = game.clone()
    
    #game.printData("Before any", 0)
    
    # I knew from wrong past attempts that 1362 was too high
    lowest = battle(game, False, 1362)
    #lowest = battleCommented(game, False, 1362, 1)
    
    print("Part One: You start with 50 hit points and 500 mana points. The boss's actual stats are in your puzzle input. What is the least amount of mana you can spend and still win the fight?")
    print(lowest)
    
    
    game = gameOrig
    #game.printData("Before any", 0)
    
    # estimate of 1400
    lowest = battle(game, True, 1400)
    #lowest = battleCommented(game, True, 1400, 1)
    
    
    print()
    print("Part Two: With the same starting stats for you and the boss, what is the least amount of mana you can spend and still win the fight?")
    print(lowest)
