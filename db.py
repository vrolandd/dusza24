import os, shutil
import models
import sqlite3

if not os.path.exists('./data'):
	os.mkdir('./data')
if not os.path.exists('./data/main.db'):
	if os.path.exists('./data/template.db'):
		shutil.copyfile('./data/template.db', './data/main.db')
	else:
		print("NO DATABASE FOUND!")
		exit(1)
	
_connection = sqlite3.connect('./data/main.db')
_cursor = _connection.cursor()

def bejelentkezes(nev:str, jelszo:str = None) -> models.Felhasznalo | None:
	_cursor.execute("SELECT rowid, Nev, Pontok FROM felhasznalok WHERE Nev = ? AND Jelszo = ?", (nev, jelszo))
	felh = _cursor.fetchone()
	return models.Felhasznalo(*felh) if felh else None

def jatekok() -> list[models.Jatek]:
	_cursor.execute("SELECT rowid, * FROM Jatekok")
	return [models.Jatek(*row) for row in _cursor.fetchall()]

print(jatekok()[0].szervezo)