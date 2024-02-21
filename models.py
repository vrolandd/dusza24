class Jatek:
	def __init__(self, data: list[str]):
		firstline = data[0].split(";")
		self.szervezo = firstline[0]
		self.nev = firstline[1]
		self.alanyok = [x for x in data[1:int(firstline[2])+1]]
		self.esemenyek = [x for x in data[int(firstline[2])+1:]]

	def __str__(self):
		out = f"{self.szervezo};{self.nev};{len(self.alanyok)};{len(self.esemenyek)}\n"
		out += "\n".join(self.alanyok + self.esemenyek)
		return out


class Fogadas:
	def __init__(self, data: str):
		data = data.split(";")
		self.fogado = data[0]
		self.jatek = data[1]
		self.osszeg = int(data[2])
		self.alany = data[3]
		self.esemeny = data[4]
		self.ertek = data[5]

	def __str__(self):
		return f"{self.fogado};{self.jatek};{self.osszeg};{self.alany};{self.esemeny};{self.ertek}"


class Eredmeny:
	def __init__(self, data: str):
		self.alany = data.split(";")[0]
		self.esemeny = data.split(";")[1]
		self.ertek = data.split(";")[2]
		self.szorzo = int(data.split(";")[3])
	
	def __str__(self):
		return f"{self.alany};{self.esemeny};{self.ertek};{self.szorzo}"


class JatekEredmeny:
	def __init__(self, data: list[str]):
		self.jatek = data[0]
		self.eredmenyek = [Eredmeny(x) for x in data[1:]]

	def __str__(self):
		out = self.jatek + "\n"
		out += "\n".join(self.eredmenyek)
		return out