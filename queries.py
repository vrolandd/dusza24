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
        
    print(gameStats)

def userRanking(users:List[models.Felhasznalo]):
    sortedUsers = sorted(users, key=lambda user: round(user.pontok), reverse=True)
    rank = 1
    prevPoints = None
    id = 0 # Not using user.id 'cus of the posibility of user deletion feature breaking the WHOLE FUCKING METHOD, AND MIGHT CAUSE THE EFFECT OF ME BREAKING YOUR NECK
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
                        if bet.alany == subject and bet.esemeny == event and bet.jatek.nev == game.nev and bet.ertek == result.ertek: betStats[f'{event}-{subject}']['WinAmount'] += bet.osszeg * result.szorzo
    
    print(betStats, end='\n\n' + '-----' * 10 + '\n\n')

# for game in db.jatekok(): # betStats test
#     betStats(game)

def calcPoints(game:models.Jatek): # Calculate the users' points based on the ended bets' results.
    """Call this #statim# [immediately] after ending a bet 'event' AND calling 'calcMultiplier' [and doing its' instructions before this]!"""
    users = db.felhasznalok()
    for result in db.eredmenyek():
        if result.esemeny in game.esemenyek and result.alany in game.alanyok and result.jatek.nev == game.nev:
            for bet in db.fogadasok():
                if bet.jatek.nev == result.jatek.nev and bet.alany == result.alany and bet.esemeny == result.esemeny and bet.ertek == result.ertek:
                    next(filter(lambda user: user.nev == bet.fogado.nev, users), None).pontok += bet.osszeg * result.szorzo

    return users # Return a new users list with the updated points. USE THIS IN THE DATABASE UPDATE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# for result in db.eredmenyek():
#     calcPoints(result.esemeny)


# gameStats() # gameStats test
# printUser() # print all users
# printGame() # print all games
# printBet() # print all bets
# printResult() # print all results

# TODO: History / Logs in SQLite [For point calculation] (?)
# TODO: Rename file (Low priority)
# TODO: Remake methods to return values (Low priority)
# TODO: Points calculation method (DONE)
# TODO: Multiplier calculation method (DONE)



# def calcMultiplier(game:models.Jatek):
#     """Call this every time AFTER someone makes a bet. If you end a game, call this immediately, and THEN update the completed events in the database."""

def showMultipliers(game:models.Jatek, subjectCheck:str = None, eventCheck:str = None, valueCheck:str = None): # Kiszámítja, hogy mi LESZ a szorzó, ha 
    # if not any(checkGame.jatek.nev == game.name for checkGame in db.fogadasok()): return None
    # if any(checkGame.jatek.nev == game.nev for checkGame in db.eredmenyek()): return 'Egy kibaszott gyökér vagy'

    multiplierDict = {}

    for subject in game.alanyok:
        for event in game.esemenyek:
            for bet in db.fogadasok():
                if bet.alany == subject and bet.esemeny == event:
                    multiplierDict[f'{subject};{event};{bet.ertek}'] = multiplierDict.get(f'{subject};{event};{bet.ertek}', 0) + bet.osszeg


    pointSum = sum(map(lambda x: x[1], multiplierDict.items()))

    for key in multiplierDict:
        multiplierDict[key] = round(multiplierDict[key] / pointSum * 5, 2)
    
    try:
        if not subjectCheck is None and not eventCheck is None and not valueCheck is None: return multiplierDict[f'{subjectCheck};{eventCheck};{valueCheck}']
        else: return multiplierDict
    except(KeyError):
        return 6


# for game in db.jatekok():
#     print(showMultipliers(game, 'qweqwe', 'fgddfg', 'igen'))
#     print('\n\n\n' + '---------' * 10 + '\n\n\n')







    # for bet in calcPoints(result.esemeny):
    #     print(bet.esemeny, bet.id)
    #     print(bet.fogado.nev, bet.fogado.pontok)

# for bet in db.fogadasok():
#     print(bet.fogado.nev, bet.fogado.pontok)

# for user in userRanking(): # userRanking test
#     print(user.nev, user.pontok, user.rank)