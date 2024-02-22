class Felhasznalo:
	def __init__(self, id:int, nev:str, pontok:int):
		self.id = int(id)
		self.nev = str(nev)
		self.pontok = int(pontok)
	

class Jatek:
	def __init__(self, id:int, nev:str, alanyok:str, esemenyek:str, szervezo:Felhasznalo):
		self.id = int(id)
		self.szervezo = szervezo
		self.nev = str(nev)
		self.alanyok = alanyok.split(";")
		self.esemenyek = esemenyek.split(";")


class Fogadas:
	def __init__(self, id:int, osszeg:int, alany:str, esemeny:str, ertek:str, fogado:Felhasznalo, jatek:Jatek):
		self.id = int(id)
		self.fogado = fogado
		self.jatek = jatek
		self.osszeg = int(osszeg)
		self.alany = str(alany)
		self.esemeny = str(esemeny)
		self.ertek = str(ertek)


class Eredmeny:
	def __init__(self, id:int, alany:str, esemeny:str, ertek:str, szorzo:int, jatek:Jatek):
		self.id = int(id)
		self.jatek = jatek
		self.alany = str(alany)
		self.esemeny = str(esemeny)
		self.ertek = str(ertek)
		self.szorzo = int(szorzo)