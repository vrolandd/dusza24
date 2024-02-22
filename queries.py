import db
import models

def printGame():
    for game in db.jatekok():
        print(f'ID: {game.id}\n\tSzervező: {game.szervezo}\n\tNév: {game.nev}\n\tAlanyok: {game.alanyok}\n\tEsemények: {game.esemenyek}')
    print('\n' + '---' * 10 + '\n')

def printBet():
    for bet in db.fogadasok():
        print(f'ID: {bet.id}\n\tFogadó: {bet.fogado}\n\tJáték: {bet.jatek.nev}\n\tÖsszeg: {bet.osszeg}\n\tAlany: {bet.alany}\n\tEsemény: {bet.esemeny}\n\tJáték: {bet.jatek}\n\tÉrték: {bet.ertek}')
    print('\n' + '---' * 10 + '\n')

def printResult():
    for result in db.eredmenyek():
        print(f'ID: {result.id}\n\tJáték: {result.jatek.nev}\n\tAlany: {result.alany}\n\tEsemény: {result.esemeny}\n\Érték: {result.ertek}\n\tSzorzó: {result.szorzo}')
    print('\n' + '---' * 10 + '\n')

def printUser():
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

def userRanking():
    sortedUsers = sorted(db.felhasznalok(), key=lambda user: user.pontok, reverse=True)
    rank = 1
    prevPoints = None
    for user in sortedUsers:
        if user.pontok != prevPoints: user.rank = rank
        else: user.rank = prevRank
        prevRank = user.rank
        prevPoints = user.pontok
        rank += 1
        sortedUsers[user.id-1] = user

    return sortedUsers


    




# NumOfBets, BetAmount, WinAmount




# for user in userRanking():
#     print(user.nev, user.pontok, user.rank)


# gameStats()

# printUser()
printGame()
printBet()
printResult()