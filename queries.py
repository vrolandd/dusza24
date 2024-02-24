import db
import models

def printGame(): # Test
    for game in db.jatekok():
        print(f'ID: {game.id}\n\tSzervező: {game.szervezo}\n\tNév: {game.nev}\n\tAlanyok: {game.alanyok}\n\tEsemények: {game.esemenyek}')
    print('\n' + '---' * 10 + '\n')

def printBet(): # Test
    for bet in db.fogadasok():
        print(f'ID: {bet.id}\n\tFogadó: {bet.fogado}\n\tJáték: {bet.jatek.nev}\n\tÖsszeg: {bet.osszeg}\n\tAlany: {bet.alany}\n\tEsemény: {bet.esemeny}\n\tJáték: {bet.jatek}\n\tÉrték: {bet.ertek}')
    print('\n' + '---' * 10 + '\n')

def printResult(): # Test
    for result in db.eredmenyek():
        print(f'ID: {result.id}\n\tJáték: {result.jatek.nev}\n\tAlany: {result.alany}\n\tEsemény: {result.esemeny}\n\tÉrték: {result.ertek}\n\tSzorzó: {result.szorzo}')
    print('\n' + '---' * 10 + '\n')

def printUser(): # Test
    for user in db.felhasznalok():
        print(f'ID: {user.id}\n\tNév: {user.nev}\n\tPontok: {user.pontok}')
    print('\n' + '---' * 10 + '\n')


def gameStats(): # Get all games' statistics.
    gameStats = {}
    for game in db.jatekok():
        gameStats[game.id] = {}
        gameStats[game.id]['NumOfBets'] = 0
        gameStats[game.id]['BetAmount'] = 0
        gameStats[game.id]['WinAmount'] = 0
        for bet in db.fogadasok():
            if bet.jatek.id == game.id:
                gameStats[game.id]['NumOfBets'] += 1
                gameStats[game.id]['BetAmount'] += bet.osszeg
        for result in db.eredmenyek():
            if result.jatek.id == game.id and result.alany in game.alanyok and result.esemeny in game.esemenyek:
                for bet in db.fogadasok():
                    if result.alany == bet.alany and result.esemeny == bet.esemeny and result.ertek == bet.ertek: gameStats[game.id]['WinAmount'] += bet.osszeg * result.szorzo
        
    return gameStats # Return them in a dictionary based on the game ids.

def betStats(game:models.Jatek): # Get bet statistics by Game object.
    betStats = {}
    for subject in game.alanyok:
        for event in game.esemenyek:
            betStats[f'{event};{subject}'] = {}
            betStats[f'{event};{subject}']['NumOfBets'] = 0
            betStats[f'{event};{subject}']['BetAmount'] = 0
            betStats[f'{event};{subject}']['WinAmount'] = 0
            for bet in db.fogadasok():
                if bet.alany == subject and bet.esemeny == event and bet.jatek.id == game.id:
                    betStats[f'{event};{subject}']['NumOfBets'] += 1
                    betStats[f'{event};{subject}']['BetAmount'] += bet.osszeg
            for result in db.eredmenyek():
                if result.jatek.id == game.id and result.alany == subject and result.esemeny == event:
                    for bet in db.fogadasok():
                        if bet.alany == subject and bet.esemeny == event and bet.jatek.id == game.id and bet.ertek == result.ertek: betStats[f'{event};{subject}']['WinAmount'] += bet.osszeg * result.szorzo
    
    return betStats # Return them in a dictionary based on 'event;subject' combined String.

def calcPoints(game:models.Jatek, results:dict, multipliers:dict): # Calculate the users' points based on the ended bets' results.
    """Call this after ending a bet 'event' AND calling 'calcMultiplier' [and doing its' instructions before this]!"""
    users = db.felhasznalok()

    for subject in results:
        for event in results[subject]:
            for bet in db.fogadasok():
                if bet.jatek.id == game.id and bet.alany in game.alanyok and bet.esemeny in game.esemenyek and bet.alany == subject and bet.esemeny == event and bet.ertek == results[subject][event].get():
                    next(filter(lambda user: user.nev == bet.fogado.nev, users), None).pontok += round(bet.osszeg * multipliers[f'{subject};{event};{results[subject][event].get()}'])

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
        if not subjectCheck is None and not eventCheck is None and not valueCheck is None: return multiplierDict[f'{subjectCheck};{eventCheck};{valueCheck}'] # If there is a provided bet return only it's multiplier.
        else: return multiplierDict # Return all multipliers based on Game object.
    except(KeyError): # If the provided bet does not exists make the multiplier 0.
        return 0

# gameStats() # gameStats test
# printUser() # print all users
# printGame() # print all games
# printBet() # print all bets
# printResult() # print all results