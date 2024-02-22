import os, shutil
from time import sleep
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
	_cursor.execute("SELECT rowid, Nev, Pontok FROM Felhasznalok WHERE Nev = ? AND Jelszo = ?;", (nev, jelszo))
	felh = _cursor.fetchone()
	return models.Felhasznalo(*felh) if felh else None

def jatekok() -> list[models.Jatek]:
	_cursor.execute("""
		SELECT Jatekok.rowid, Jatekok.Nev, Jatekok.Alanyok, Jatekok.Esemenyek, 
					Felhasznalok.rowid, Felhasznalok.Nev, Felhasznalok.Pontok 
		FROM Jatekok 
		INNER JOIN Felhasznalok ON Felhasznalok.rowid = Jatekok.SzervezoId;""")
	return [models.Jatek(*row[:4], models.Felhasznalo(*row[4:])) for row in _cursor.fetchall()]

def fogadasok() -> list[models.Fogadas]:
	_cursor.execute("""
		SELECT Fogadasok.rowid, Fogadasok.Osszeg, Fogadasok.Alany, Fogadasok.Esemeny, Fogadasok.Ertek, 
					Felhasznalok.rowid, Felhasznalok.Nev, Felhasznalok.Pontok, 
					Jatekok.rowid, Jatekok.Nev, Jatekok.Alanyok, Jatekok.Esemenyek, 
					Jatekok.SzervezoId, Szervezo.Nev, Szervezo.Pontok
		FROM Fogadasok 
		INNER JOIN Jatekok ON Jatekok.rowid = Fogadasok.JatekId 
		INNER JOIN Felhasznalok ON Felhasznalok.rowid = Fogadasok.FogadoId
		INNER JOIN Felhasznalok AS Szervezo ON Jatekok.SzervezoId = Szervezo.rowid;""")
	return [models.Fogadas(*row[:5], models.Felhasznalo(*row[5:8]), models.Jatek(*row[8:12], models.Felhasznalo(*row[12:]))) for row in _cursor.fetchall()]

def eredmenyek() -> list[models.Eredmeny]:
	_cursor.execute("""
		SELECT Eredmenyek.rowid, Eredmenyek.Alany, Eredmenyek.Esemeny, Eredmenyek.Ertek, Eredmenyek.Szorzo,
					Jatekok.rowid, Jatekok.Nev, Jatekok.Alanyok, Jatekok.Esemenyek, 
					Felhasznalok.rowid, Felhasznalok.Nev, Felhasznalok.Pontok
		FROM Eredmenyek 
		INNER JOIN Jatekok ON Jatekok.rowid = Esemenyek.JatekId
		INNER JOIN Felhasznalok ON Felhasznalok.rowid = Jatekok.SzervezoId;""")
	return [models.Eredmeny(*row[:5], models.Jatek(*row[5:9], models.Felhasznalo(*row[9:]))) for row in _cursor.fetchall()]