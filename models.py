class Felhasznalo:
	def __init__(self, id:int, nev:str, pontok:int):
		self.id = id
		self.nev = nev
		self.pontok = pontok
	

class Jatek:
	def __init__(self, id:int, szervezo:int, nev:str, alanyok:str, esemenyek:str):
		self.id = id
		self.szervezo = szervezo
		self.nev = nev
		self.alanyok = alanyok.split(";")
		self.esemenyek = esemenyek.split(";")


class Fogadas:
	def __init__(self, id:int, fogado:int, jatek:int, osszeg:int, alany:str, esemeny:str, ertek:str):
		self.id = id
		self.fogado = fogado
		self.jatek = jatek
		self.osszeg = osszeg
		self.alany = alany
		self.esemeny = esemeny
		self.ertek = ertek


class Eredmeny:
	def __init__(self, id:int, jatek:int, alany:str, esemeny:str, ertek:str, szorzo:int):
		self.id = id
		self.jatek = jatek
		self.alany = alany
		self.esemeny = esemeny
		self.ertek = ertek
		self.szorzo = szorzo