import db
import models
from typing import List

def printGame(): # Delete later
    for game in db.jatekok():
        print(f'ID: {game.id}\n\tSzervező: {game.szervezo}\n\tNév: {game.nev}\n\tAlanyok: {game.alanyok}\n\tEsemények: {game.esemenyek}')
    print('\n' + '---' * 10 + '\n')

def printBet(): # Delete later
    for bet in db.fogadasok():
        print(f'ID: {bet.id}\n\tFogadó: {bet.fogado}\n\tJáték: {bet.jatek.nev}\n\tÖsszeg: {bet.osszeg}\n\tAlany: {bet.alany}\n\tEsemény: {bet.esemeny}\n\tJáték: {bet.jatek}\n\tÉrték: {bet.ertek}')
    print('\n' + '---' * 10 + '\n')

def printResult(): # Delete later
    for result in db.eredmenyek():
        print(f'ID: {result.id}\n\tJáték: {result.jatek.nev}\n\tAlany: {result.alany}\n\tEsemény: {result.esemeny}\n\tÉrték: {result.ertek}\n\tSzorzó: {result.szorzo}')
    print('\n' + '---' * 10 + '\n')

def printUser(): # Delete later
    for user in db.felhasznalok():
        print(f'ID: {user.id}\n\tNév: {user.nev}\n\tPontok: {user.pontok}')
    print('\n' + '---' * 10 + '\n')


def gameStats():
    gameStats = {}
    for game in db.jatekok():
        gameStats[game.nev] = {}
        gameStats[game.nev]['NumOfBets'] = 0
        gameStats[game.nev]['BetAmount'] = 0
        gameStats[game.nev]['WinAmount'] = 0
        for bet in db.fogadasok():
            if bet.jatek.nev == game.nev:
                gameStats[game.nev]['NumOfBets'] += 1
                gameStats[game.nev]['BetAmount'] += bet.osszeg
        for result in db.eredmenyek():
            if result.jatek.nev == game.nev and result.alany in game.alanyok and result.esemeny in game.esemenyek:
                for bet in db.fogadasok():
                    if result.alany == bet.alany and result.esemeny == bet.esemeny and result.ertek == bet.ertek: gameStats[game.nev]['WinAmount'] += bet.osszeg * result.szorzo
        
    return gameStats

def userRanking(users:List[models.Felhasznalo]):
    sortedUsers = sorted(users, key=lambda user: round(user.pontok), reverse=True)
    rank = 1
    prevPoints = None
    id = 0 # Not using user.id because of the posibility of user deletion feature breaking everything.
    for user in sortedUsers:
        user.pontok = round(user.pontok)
        if user.pontok != prevPoints: user.rank = rank
        else: user.rank = prevRank
        prevRank = user.rank
        prevPoints = user.pontok
        rank += 1
        sortedUsers[id] = user
        id += 1

    return sortedUsers

def betStats(game:models.Jatek):
    betStats = {}
    for subject in game.alanyok:
        for event in game.esemenyek:
            betStats[f'{event};{subject}'] = {}
            betStats[f'{event};{subject}']['NumOfBets'] = 0
            betStats[f'{event};{subject}']['BetAmount'] = 0
            betStats[f'{event};{subject}']['WinAmount'] = 0
            for bet in db.fogadasok():
                if bet.alany == subject and bet.esemeny == event and bet.jatek.nev == game.nev:
                    betStats[f'{event};{subject}']['NumOfBets'] += 1
                    betStats[f'{event};{subject}']['BetAmount'] += bet.osszeg
            for result in db.eredmenyek():
                if result.jatek.nev == game.nev and result.alany == subject and result.esemeny == event:
                    for bet in db.fogadasok():
                        if bet.alany == subject and bet.esemeny == event and bet.jatek.nev == game.nev and bet.ertek == result.ertek: betStats[f'{event};{subject}']['WinAmount'] += bet.osszeg * result.szorzo
    
    return betStats

# for game in db.jatekok(): # betStats test
#     print(betStats(game))

def calcPoints(game:models.Jatek, results:dict, multipliers:dict): # Calculate the users' points based on the ended bets' results.
    """Call this #statim# [immediately] after ending a bet 'event' AND calling 'calcMultiplier' [and doing its' instructions before this]!"""
    users = db.felhasznalok()


    for subject in results:
        for event in results[subject]:
            # subject[event].get()
            for bet in db.fogadasok():
                if bet.jatek.nev == game.nev and bet.alany in game.alanyok and bet.esemeny in game.esemenyek and bet.alany == subject and bet.esemeny == event and bet.ertek == results[subject][event].get():
                    next(filter(lambda user: user.nev == bet.fogado.nev, users), None).pontok += round(bet.osszeg * multipliers[f'{subject};{event};{results[subject][event].get()}'])


    # for result in db.eredmenyek():
    #     if result.esemeny in game.esemenyek and result.alany in game.alanyok and result.jatek.nev == game.nev:
    #         for bet in db.fogadasok():
    #             if bet.jatek.nev == result.jatek.nev and bet.alany == result.alany and bet.esemeny == result.esemeny and bet.ertek == result.ertek:
    #                 next(filter(lambda user: user.nev == bet.fogado.nev, users), None).pontok += bet.osszeg * result.szorzo

    return users # Return a new users list with the updated points.

    


def showMultipliers(game:models.Jatek, subjectCheck:str = None, eventCheck:str = None, valueCheck:str = None):
    """Call this every time the user opens the betting page. This returns every subject - event - value pair's multiplier. If the optional variables are given, which should be at the moment when the game is closed, it returns the winning value's multiplier."""
    multiplierDict = {}

    for subject in game.alanyok:
        for event in game.esemenyek:
            for bet in db.fogadasok():
                if bet.alany == subject and bet.esemeny == event:
                    multiplierDict[f'{subject};{event};{bet.ertek}'] = multiplierDict.get(f'{subject};{event};{bet.ertek}', 0) + 1 # => bet.osszeg: Pénz alapján számítja, 1: Emberek száma alapján számítja.

    # pointSum = sum(map(lambda x: x[1], multiplierDict.items())) # Használd ezt, ha összeg alapján számítjuk.

    for key in multiplierDict:
        multiplierDict[key] = 1 + round(5 / (2 ** (multiplierDict[key] - 1)), 2) # Használd ezt, ha emberek száma alapján számítjuk.
        # multiplierDict[key] = 1 + round((1 - multiplierDict[key] / pointSum) * 5, 2) # Használd ezt, ha összeg alapján számítjuk.
    
    try:
        if not subjectCheck is None and not eventCheck is None and not valueCheck is None: return multiplierDict[f'{subjectCheck};{eventCheck};{valueCheck}']
        else: return multiplierDict
    except(KeyError):
        return 0


# for game in db.jatekok():
#     calcPoints(game)

# for result in db.eredmenyek():
#     calcPoints(result.esemeny)

# gameStats() # gameStats test
# printUser() # print all users DELETE
# printGame() # print all games DELETE
# printBet() # print all bets DELETE
# printResult() # print all results DELETE

# for game in db.jatekok():
#     print(showMultipliers(game))
#     print('\n\n\n' + '---------' * 10 + '\n\n\n')

# for bet in db.fogadasok():
#     print(bet.fogado.nev, bet.fogado.pontok)

# for user in userRanking(): # userRanking test
#     print(user.nev, user.pontok, user.rank)