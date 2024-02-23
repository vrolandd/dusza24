import os, shutil
import models
import sqlite3

from argon2 import PasswordHasher


if not os.path.exists('./data'):
	os.mkdir('./data')
if not os.path.exists('./data/main.db'):
	if os.path.exists('./data/template.db'):
		shutil.copyfile('./data/template.db', './data/main.db')
	else:
		print("NO DATABASE FOUND!")
		exit(1)
	
_hasher = PasswordHasher()
_connection = sqlite3.connect('./data/main.db')
_cursor = _connection.cursor()

def bejelentkezes(nev:str, jelszo:str = None) -> models.Felhasznalo | str:
	_cursor.execute("SELECT rowid, Nev, Pontok, Jelszo FROM Felhasznalok WHERE Nev = ?;", (nev,))
	resp = _cursor.fetchone()
	if not resp:
		return "nincs_ilyen_felhasznalo"
	try:
		_hasher.verify(resp[3], jelszo)
		return models.Felhasznalo(*resp[:3])
	except Exception:
		return "helytelen_jelszo"

def regisztracio(nev:str, jelszo:str) -> models.Felhasznalo:
	_cursor.execute("INSERT INTO Felhasznalok (Nev, Jelszo, Pontok) VALUES (?, ?, 100);", (nev, _hasher.hash(jelszo)))
	_cursor.execute("SELECT rowid, Nev, Pontok FROM Felhasznalok WHERE Nev = ?;", (nev,))
	resp = _cursor.fetchone()
	_connection.commit()
	return models.Felhasznalo(*resp)

def jelszo_modositas(felhasznaloId:int, ujJelszo:str):
	_cursor.execute("UPDATE Felhasznalok SET Jelszo = ? WHERE rowid = ?;", (_hasher.hash(ujJelszo), felhasznaloId))
	_connection.commit()

def felhasznalok() -> list[models.Felhasznalo]:
	_cursor.execute("SELECT rowid, Nev, Pontok FROM Felhasznalok;")
	return [models.Felhasznalo(*row) for row in _cursor.fetchall()]

def jatekok(jatekId:int = None, felhasznaloId:int = None, include_lezart = True) -> list[models.Jatek]:
	_cursor.execute(f"""
		SELECT Jatekok.rowid, Jatekok.Nev, Jatekok.Alanyok, Jatekok.Esemenyek, 
					Felhasznalok.rowid, Felhasznalok.Nev, Felhasznalok.Pontok 
		FROM Jatekok 
		INNER JOIN Felhasznalok ON Felhasznalok.rowid = Jatekok.SzervezoId
		{"LEFT JOIN Eredmenyek ON Jatekok.rowid = Eredmenyek.JatekId" if not include_lezart else ""}
		WHERE {"Eredmenyek.rowid IS NULL" if not include_lezart else "1"}
		AND {"Jatekok.rowid = ?" if jatekId else "1"}
		AND {"Jatekok.SzervezoId = ?" if felhasznaloId else "1"};""",
		tuple(filter(None, (jatekId, felhasznaloId))))
	return [models.Jatek(*row[:4], models.Felhasznalo(*row[4:])) for row in _cursor.fetchall()]

def fogadasok(fogadasId:int = None, felhasznaloId:int = None) -> list[models.Fogadas]:
	_cursor.execute(f"""
		SELECT Fogadasok.rowid, Fogadasok.Osszeg, Fogadasok.Alany, Fogadasok.Esemeny, Fogadasok.Ertek, 
					Felhasznalok.rowid, Felhasznalok.Nev, Felhasznalok.Pontok, 
					Jatekok.rowid, Jatekok.Nev, Jatekok.Alanyok, Jatekok.Esemenyek, 
					Jatekok.SzervezoId, Szervezo.Nev, Szervezo.Pontok
		FROM Fogadasok 
		INNER JOIN Jatekok ON Jatekok.rowid = Fogadasok.JatekId 
		INNER JOIN Felhasznalok ON Felhasznalok.rowid = Fogadasok.FogadoId
		INNER JOIN Felhasznalok AS Szervezo ON Jatekok.SzervezoId = Szervezo.rowid
		WHERE {"Fogadasok.FogadoId = ?" if felhasznaloId else "1"}
		AND {"Fogadasok.rowid = ?" if fogadasId else "1"};""", 
		tuple(filter(None, (felhasznaloId, fogadasId))))
	return [models.Fogadas(*row[:5], models.Felhasznalo(*row[5:8]), models.Jatek(*row[8:12], models.Felhasznalo(*row[12:]))) for row in _cursor.fetchall()]

def eredmenyek() -> list[models.Eredmeny]:
	_cursor.execute("""
		SELECT Eredmenyek.rowid, Eredmenyek.Alany, Eredmenyek.Esemeny, Eredmenyek.Ertek, Eredmenyek.Szorzo,
				Jatekok.rowid, Jatekok.Nev, Jatekok.Alanyok, Jatekok.Esemenyek, 
				Felhasznalok.rowid, Felhasznalok.Nev, Felhasznalok.Pontok
		FROM Eredmenyek 
		INNER JOIN Jatekok ON Jatekok.rowid = Eredmenyek.JatekId
		INNER JOIN Felhasznalok ON Felhasznalok.rowid = Jatekok.SzervezoId;""")
	return [models.Eredmeny(*row[:5], models.Jatek(*row[5:9], models.Felhasznalo(*row[9:]))) for row in _cursor.fetchall()]

def uj_jatek(szervezoId:int, nev:str, alanyok:list[str], esemenyek:list[str]):
	_cursor.execute("""
		INSERT INTO Jatekok (SzervezoId, Nev, Alanyok, Esemenyek) VALUES (?, ?, ?, ?);
		""", (szervezoId, nev, ";".join(alanyok), ";".join(esemenyek)))
	_connection.commit()

def uj_fogadas(fogadoId:int, jatekId:int, osszeg:int, alany:str, esemeny:str, ertek:str):
	try:
		_cursor.execute("BEGIN TRANSACTION;")
		_cursor.execute("UPDATE Felhasznalok SET Pontok = Pontok - ? WHERE rowid = ?;",
			(osszeg, fogadoId))
		_cursor.execute("INSERT INTO Fogadasok (FogadoId, JatekId, Osszeg, Alany, Esemeny, Ertek) VALUES (?, ?, ?, ?, ?, ?);",
			(fogadoId, jatekId, osszeg, alany, esemeny, ertek))
		_cursor.execute("COMMIT;")
		_connection.commit()
	except Exception as e:
		_cursor.execute("ROLLBACK;")
		raise e

def closeGame(gameId:int, results:dict, users:list[models.Felhasznalo], multiplier:int):
	try:
		_cursor.execute('BEGIN TRANSACTION;')
		for subject in results:
			for event in subject:
				_cursor.execute('INSERT INTO Eredmenyek (JatekId, Alany, Esemeny, Ertek, Szorzo) VALUES (?, ?, ?, ?, ?);', (gameId, subject, event, subject[event], multiplier))
		for user in users: _cursor.execute('UPDATE Felhasznalok SET Pontok = ? WHERE rowid = ?;', (user.pontok, user.id))
		_cursor.execute('COMMIT;')
		_connection.commit()
	except Exception as e:
		print(e)
		_cursor.execute('ROLLBACK;')