import os
from . import models


if not os.path.exists('./data'):
	os.mkdir('./data')
if not os.path.exists('./data/jatekok.txt'):
	open('./data/jatekok.txt', "w", encoding="utf-8").close()
if not os.path.exists('./data/fogadasok.txt'):
	open('./data/fogadasok.txt', "w", encoding="utf-8").close()
if not os.path.exists('./data/eredmenyek.txt'):
	open('./data/eredmenyek.txt', "w", encoding="utf-8").close()

#
def getJatekok():
	jatekok = []
	with open('./data/jatekok.txt', 'r', encoding='utf-8') as f:
		lines = f.readlines()
		text = lines[0]
		for line in lines[1:]:
			if not line.strip():
				continue
			if ";" in line:
				jatekok.append(models.Jatek(text))
				text = ""
			text += line 
		jatekok.append(models.Jatek(text))
	return jatekok


def getFogadasok():
	fogadasok = []
	with open('./data/fogadasok.txt', 'r', encoding='utf-8') as f:
		for line in f.readlines():
			fogadasok.append(models.Fogadas(line.strip()))
	return fogadasok


def getEredmenyek():
	eredmenyek = []
	with open('./data/eredmenyek.txt', 'r', encoding='utf-8') as f:
		lines = f.readlines()
		text = lines[0]
		for line in lines[1:]:
			if not line.strip():
				continue
			if not ";" in line:
				eredmenyek.append(models.Jatek(text))
				text = ""
			text += line
		eredmenyek.append(models.Jatek(text))
	return eredmenyek