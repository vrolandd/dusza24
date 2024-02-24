from tkinter import IntVar, filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs.dialogs import Messagebox
import queries
import db


app = ttk.Window(title="KandOS", themename='litera')
mainframe = ttk.Frame(app)
mainframe.pack(fill=BOTH, expand=True, padx=10, pady=10)

currentUser: db.models.Felhasznalo | str = "kijelentkezve"

updaters = []
def updateAll():
	remove = []
	for u in updaters:
		try: u()
		except Exception: 
			remove.append(u)
	for r in remove:
		updaters.remove(r)

def uj_jatek(base):
	box = ttk.Toplevel(base)
	box.title("KandOS - Új Játék")
	box.geometry("500x500")
	ttk.Label(box, text="Új Játék", font=("TkDefaultFont", 20)).pack(padx=10, pady=10)
	form_frame = ttk.Frame(box)
	form_frame.pack()
	ttk.Label(form_frame, text="Játék neve:").grid(row=1, column=0, padx=5, pady=5)
	jatekneve = ttk.Entry(form_frame)
	jatekneve.grid(row=1, column=1, padx=5, pady=5)

	alanyok = ttk.Treeview(form_frame, columns=("alanyok"), show='headings', selectmode='browse')
	alanyok.grid(row=2, column=0, padx=5, pady=5)
	alanyok.column("alanyok", anchor=W)
	alanyok.heading("alanyok", text="Alanyok", anchor=W)
	alanyok.bind('<ButtonRelease-1>', lambda _: alanyok.delete(alanyok.selection()) if alanyok.selection() else None)
	
	ujalany = ttk.Entry(form_frame)
	ujalany.bind('<Return>', lambda _: (alanyok.insert('', 'end', values=(ujalany.get().replace(";", " "),)), ujalany.delete(0, END)) if ujalany.get() else None)
	ujalany.grid(row=3, column=0, padx=5, pady=5)

	esemenyek = ttk.Treeview(form_frame, columns=("esemenyek"), show='headings', selectmode='browse')
	esemenyek.grid(row=2, column=1, padx=5, pady=5)
	esemenyek.column("esemenyek", anchor=W)
	esemenyek.heading("esemenyek", text="Események", anchor=W)
	esemenyek.bind('<ButtonRelease-1>', lambda _: esemenyek.delete(esemenyek.selection()) if esemenyek.selection() else None)

	ujesemeny = ttk.Entry(form_frame)
	ujesemeny.bind('<Return>', lambda _: (esemenyek.insert('', 'end', values=(ujesemeny.get().replace(";", " "),)), ujesemeny.delete(0, END)) if ujesemeny.get() else None)
	ujesemeny.grid(row=3, column=1, padx=5, pady=5)

	def __cmd():
		try:
			if not (jatekneve.get() and alanyok.get_children() and esemenyek.get_children()):
				raise Exception("Kitöltetlen mezők")
			db.uj_jatek(currentUser.id, jatekneve.get(), set([str(alanyok.item(x)["values"][0]) for x in alanyok.get_children()]), set([str(esemenyek.item(x)["values"][0]) for x in esemenyek.get_children()]))
			box.destroy()
			updateAll()
		except Exception as e:
			Messagebox.show_error("Hiba történt a játék készítése közben.\nEllenőrizd, hogy mindent helyesen adtál-e meg és próbáld újra!", "KandOS - Hiba", box)
	ujjatekBTN = ttk.Button(form_frame, text="Játék létrehozása", bootstyle="success", command=__cmd)
	ujjatekBTN.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

def fogadas_leadasa(base, jatekId:int):
	jatek = db.jatekok(jatekId)[0]
	box = ttk.Toplevel(base)
	box.title("KandOS - Fogadás leadása")
	box.geometry("500x550")
	
	ttk.Label(box, text="Fogadás leadása", font=("TkDefaultFont", 20)).pack(padx=10, pady=4)
	ttk.Label(box, text=jatek.nev, font=("TkDefaultFont", 12)).pack(padx=10, pady=5)
	
	form_frame = ttk.Frame(box)
	form_frame.pack()

	ttk.Label(form_frame, text=f"Tét (1-{currentUser.pontok}):").grid(row=1, column=0, padx=5, pady=5)
	tet = ttk.Entry(form_frame, width=25)
	tet.grid(row=1, column=1, padx=5, pady=5)

	alanyok = ttk.Treeview(form_frame, columns=('alanyok'), show='headings', selectmode='browse')
	alanyok.grid(row=2, column=0, padx=5, pady=5)
	alanyok.column("alanyok", anchor=W)
	alanyok.heading("alanyok", text="Alany", anchor=W)
	for alany in jatek.alanyok:
		alanyok.insert('', 'end', iid=alany, values=(alany,))

	esemenyek = ttk.Treeview(form_frame, columns=('esemenyek'), show='headings', selectmode='browse')
	esemenyek.grid(row=2, column=1, padx=5, pady=5)
	esemenyek.column("esemenyek", anchor=W)
	esemenyek.heading("esemenyek", text="Esemény", anchor=W)
	for esemeny in jatek.esemenyek:
		esemenyek.insert('', 'end', iid=esemeny, values=(esemeny,))

	ttk.Label(form_frame, text="Eredmény:").grid(row=3, column=0, padx=5, pady=5)
	eredmeny = ttk.Entry(form_frame, width=25)
	eredmeny.grid(row=3, column=1, padx=5, pady=5)

	def __cmd():
		try:
			if not (0 < int(tet.get()) < currentUser.pontok and alanyok.selection()[0] and esemenyek.selection()[0] and eredmeny.get()):
				raise Exception('Kitöltetlen vagy helytelen mezők')
			currentUser.pontok -= int(tet.get())
			db.uj_fogadas(currentUser.id, jatekId, int(tet.get()), alanyok.selection()[0], esemenyek.selection()[0], eredmeny.get())
			box.destroy()
			updateAll()
		except Exception as e:
			Messagebox.show_error("Hiba történt a fogadás leadása közben.\nEllenőrizd, hogy mindent helyesen adtál-e meg és próbáld újra!", "KandOS - Hiba", box)
	fogadasLeadasaBTN = ttk.Button(form_frame, text="Fogadás leadása", bootstyle="success", command=__cmd)
	fogadasLeadasaBTN.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

def jatek_lezarasa(base, jatekId: int):
	jatek = db.jatekok(jatekId)[0]
	box = ttk.Toplevel(base)
	box.title("KandOS - Játék lezárása")
	box.geometry("700x700")
	
	ttk.Label(box, text="Játék lezárása", font=("TkDefaultFont", 20)).pack(padx=10, pady=4)
	ttk.Label(box, text=jatek.nev, font=("TkDefaultFont", 14)).pack(padx=10, pady=5)
	
	form_frame = ScrolledFrame(box)
	form_frame.pack(padx=5, pady=5, expand=True, fill=BOTH)
	eredmenyek = {}
	for alany in jatek.alanyok:
		alany_frame = ttk.Frame(form_frame)
		eredmenyek[alany] = {}
		ttk.Label(alany_frame, text=f"{alany} eredményei:", justify=LEFT, font=("TkDefaultFont", 12)).grid(row=0, column=0, columnspan=2, padx=5, pady=5, )
		for i, esemeny in enumerate(jatek.esemenyek):
			ttk.Label(alany_frame, text=f"{esemeny}:").grid(row=i//2+1, column=0 if i%2==0 else 2, padx=5, pady=5)
			eredmenyek[alany][esemeny] = ttk.Entry(alany_frame)
			eredmenyek[alany][esemeny].grid(row=i//2+1, column=1 if i%2==0 else 3, padx=5, pady=5)
		alany_frame.pack(padx=5, pady=8)

	lezarasBTN = ttk.Button(box, text="Játék lezárása", bootstyle="warning", command=lambda: _lezaras())
	lezarasBTN.pack(padx=5, pady=5)

	def _lezaras():
		for subject in eredmenyek:
			for event in eredmenyek[subject]:
				if eredmenyek[subject][event].get() == '':
					Messagebox.show_error("Hiba történt a fogadás leadása közben.\nEllenőrizd, hogy mindent helyesen adtál-e meg és próbáld újra!", "KandOS - Hiba", box)
					return
		multipliers = queries.showMultipliers(jatek)
		db.closeGame(jatekId, eredmenyek, queries.calcPoints(jatek, eredmenyek, multipliers), multipliers)		
		box.destroy()
	
def jelszo_modositas():
	box = ttk.Toplevel(app)
	box.title("KandOS - Jelszó módosítása")
	box.geometry("300x250")
	
	frame1 = ttk.Frame(box)
	frame1.pack(pady=5)
	ttk.Label(frame1, text="Új jelszó", font=("TkDefaultFont", 14)).pack(padx=5, pady=5, fill=X)
	jelszo1 = ttk.Entry(frame1, show="*")
	jelszo1.pack(padx=5, pady=5, fill=X)
	frame2 = ttk.Frame(box)
	frame2.pack(pady=5)
	ttk.Label(frame2, text="Új jelszó újra", font=("TkDefaultFont", 14)).pack(padx=5, pady=5, fill=X)
	jelszo2 = ttk.Entry(frame2, show="*")
	jelszo2.pack(padx=5, pady=5, fill=X)

	def __cmd():
		if not jelszo1.get() == jelszo2.get():
			Messagebox.show_error("A megadott jelszavak nem egyeznek.\nPróbáld újra!", title="KandOS - Hiba", parent=box)
		db.jelszo_modositas(currentUser.id, jelszo1.get())
		box.destroy()
		Messagebox.ok("A jelszavad sikeresen módosult.", title="KandOS - Sikeres jelszó módosítás")
	jelszomodBTN = ttk.Button(box, text="Jelszó módosítása", bootstyle="warning", command=__cmd)
	jelszomodBTN.pack(padx=5, pady=5)

def importalas():
	box = ttk.Toplevel(app)
	box.title("KandOS - Importálás")
	box.geometry("450x450")
	box.minsize(450, 450)
	ttk.Label(box, text="Importálás", font=("TkDefaultFont", 20)).pack(padx=10, pady=10)
	ttk.Label(box, text="HIBÁS FÁJLOK MEGADÁSA ESETÉN\nAZ ADATBÁZIS SÉRÜLHET", font=("TkDefaultFont", 12)).pack(padx=10, pady=10)

	jatekokL = ttk.Label(box, text="Válassz 'játékok' fájlt")
	jatekokL.pack(padx=5, pady=5)
	def __jatekokselect():
		file_path = filedialog.askopenfilename(title="Válassz egy fájlt",
								filetypes=(("Szöveges fájlok", "*.txt*"), ("All files", "*.*")))
		if file_path:
			jatekokL.config(text=file_path)
	jatekokB = ttk.Button(box, text="Tallózás", command=__jatekokselect)
	jatekokB.pack(padx=5, pady=5)
	
	fogadasokL = ttk.Label(box, text="Válassz 'fogadások' fájlt")
	fogadasokL.pack(padx=5, pady=5)
	def __fogadasokselect():
		file_path = filedialog.askopenfilename(title="Válassz egy fájlt",
								filetypes=(("Szöveges fájlok", "*.txt*"), ("All files", "*.*")))
		if file_path:
			fogadasokL.config(text=file_path)
	fogadasokB = ttk.Button(box, text="Tallózás", command=__fogadasokselect)
	fogadasokB.pack(padx=5, pady=5)
	
	eredmenyekL = ttk.Label(box, text="Válassz 'eredmények' fájlt")
	eredmenyekL.pack(padx=5, pady=5)
	def __eredmenyekselect():
		file_path = filedialog.askopenfilename(title="Válassz egy fájlt",
								filetypes=(("Szöveges fájlok", "*.txt*"), ("All files", "*.*")))
		if file_path:
			eredmenyekL.config(text=file_path)
	eredmenyekB = ttk.Button(box, text="Tallózás", command=__eredmenyekselect)
	eredmenyekB.pack(padx=5, pady=5)

	def __importal():
		try:
			if jatekokL.cget('text') == "Válassz 'játékok' fájlt"\
				or fogadasokL.cget('text') == "Válassz 'fogadások' fájlt"\
				or eredmenyekL.cget('text') == "Válassz 'eredmények' fájlt":
				raise Exception("Kitöltetlen mezők")
			db.importFiles(jatekokL.cget('text'), fogadasokL.cget('text'), eredmenyekL.cget('text'))
			box.destroy()
			updateAll()
		except Exception:
			Messagebox.show_error("Hiba történt importálás közben!", "KandOS - Hiba", box)
	ttk.Button(box, text="Adatok importálása", bootstyle="warning", command=__importal).pack(padx=10, pady=10)

def szervezo_view(base):
	for widget in base.winfo_children():
		widget.destroy()
	app.geometry("700x500")
	app.minsize(600, 400)
	ttk.Label(base, text="Játékaim:", font=("TkDefaultFont", 12)).pack(padx=10, pady=(5,0), fill=X)
	treecontainer = ttk.Frame(base)
	treecontainer.pack(padx=5, pady=5, expand=True, fill=BOTH)
	jatekok = ttk.Treeview(treecontainer, columns=('nev', 'lezart'), show='headings', selectmode='browse')
	jatekok.heading("nev", text="Játék neve")
	jatekok.heading("lezart", text="Lezárt")
	jatekok.pack(padx=5, pady=5, expand=True, fill=BOTH, side=LEFT)
	yscroll = ttk.Scrollbar(treecontainer, orient=VERTICAL, command=jatekok.yview)
	yscroll.pack(side=RIGHT, fill=Y)
	jatekok.configure(yscrollcommand=yscroll.set)
	def update_jatekok():
		for item in jatekok.get_children():
			jatekok.delete(item)
		nemlezart = [x.id for x in db.jatekok(felhasznaloId=currentUser.id, include_lezart=False)]
		for v in db.jatekok(felhasznaloId=currentUser.id):
			jatekok.insert('', 'end', iid=v.id, values=(v.nev, 'Nem' if v.id in nemlezart else 'Igen'))
	updaters.append(update_jatekok)
	update_jatekok()

	actionbar = ttk.Frame(base)
	actionbar.pack(padx=5, pady=5)
	ujjatek = ttk.Button(actionbar, text="Új játék", bootstyle="success", command=lambda: uj_jatek(app))
	ujjatek.pack(padx=5, pady=5, side=LEFT)
	def __jateklezar():
		if not jatekok.selection():
			Messagebox.show_error("Válassz egy játékot!", "KandOS - Hiba", app)
		jatek_lezarasa(app, jatekok.selection()[0])
	lezaras = ttk.Button(actionbar, text="Játék lezárása", bootstyle="warning", command=__jateklezar)
	lezaras.pack(padx=5, pady=5, side=LEFT)
	
def fogado_view(base):
	for widget in base.winfo_children():
		widget.destroy()
	app.geometry("1200x800")
	app.minsize(1100, 700)
	
	ttk.Label(base, text="Elérhető játékok:", font=("TkDefaultFont", 12)).pack(padx=10, pady=(5,0), fill=X)
	treecontainer = ttk.Frame(base)
	treecontainer.pack(padx=5, pady=5, expand=True, fill=BOTH)
	jatekok = ttk.Treeview(treecontainer, columns=('nev', 'szervezo'), show='headings', selectmode='browse')
	jatekok.heading("nev", text="Játék neve")
	jatekok.heading("szervezo", text="Szervező")
	jatekok.pack(padx=5, pady=5, expand=True, fill=BOTH, side=LEFT)
	yscroll = ttk.Scrollbar(treecontainer, orient=VERTICAL, command=jatekok.yview)
	yscroll.pack(side=RIGHT, fill=Y)
	jatekok.configure(yscrollcommand=yscroll.set)
	def update_jatekok():
		for item in jatekok.get_children():
			jatekok.delete(item)
		for v in db.jatekok(include_lezart=False):
			jatekok.insert('', 'end', iid=v.id, values=(v.nev, v.szervezo.nev))
	updaters.append(update_jatekok)
	update_jatekok()

	frame9 = ttk.Frame(base)
	frame9.pack(padx=10, pady=(5,0), fill=X)
	lezartis = IntVar()
	lezartis.set(0)
	ttk.Label(frame9, text="Fogadásaim:", font=("TkDefaultFont", 12)).pack(side=LEFT)
	ttk.Checkbutton(frame9, text="Lezártak mutatása", command=updateAll, variable=lezartis).pack(side=RIGHT)
	treecontainer2 = ttk.Frame(base)
	treecontainer2.pack(padx=5, pady=5, expand=True, fill=BOTH)
	fogadasaim = ttk.Treeview(treecontainer2, columns=('jatek', 'alany', 'esemeny', 'ertek', 'osszeg'), show='headings', selectmode='browse')
	fogadasaim.heading("jatek", text="Játék neve")
	fogadasaim.heading("alany", text="Alany")
	fogadasaim.heading("esemeny", text="Esemény")
	fogadasaim.heading("ertek", text="Érték")
	fogadasaim.heading("osszeg", text="Összeg")
	fogadasaim.pack(padx=5, pady=5, expand=True, fill=BOTH, side=LEFT)
	yscroll2 = ttk.Scrollbar(treecontainer2, orient=VERTICAL, command=fogadasaim.yview)
	yscroll2.pack(side=RIGHT, fill=Y)
	fogadasaim.configure(yscrollcommand=yscroll2.set)
	def update_fogadasaim():
		for item in fogadasaim.get_children():
			fogadasaim.delete(item)
		for v in db.fogadasok(felhasznaloId=currentUser.id, include_lezart=lezartis.get()):
			fogadasaim.insert('', 'end', iid=v.id, values=(v.jatek.nev, v.alany, v.esemeny, v.ertek, v.osszeg))
	updaters.append(update_fogadasaim)
	update_fogadasaim()

	actionbar = ttk.Frame(base)
	actionbar.pack(padx=5, pady=5)
	leadas = ttk.Button(actionbar, text="Fogadás leadása", bootstyle="success", 
			command=lambda: fogadas_leadasa(app, jatekok.selection()[0]) if jatekok.selection() else Messagebox.show_error("Válassz egy játékot!", "KandOS - Hiba", app))
	leadas.pack(padx=5, pady=5, side=LEFT)
	def __torlescmd():
		if not fogadasaim.selection():
			Messagebox.show_error("Válassz egy fogadást!", "KandOS - Hiba")
		else:
			if Messagebox.show_question("Biztos ki szeretnéd törölni a kiválasztott fogadásod?", "KandOS - Fogadás", buttons=['Nem:secondary', 'Igen:primary']) == "Igen":
				db.fogadas_torles(int(fogadasaim.selection()[0]))
				updateAll()
	torles = ttk.Button(actionbar, text="Fogadás törlése", bootstyle="warning", command=__torlescmd)
	torles.pack(padx=5, pady=5, side=LEFT)

def stats_view(base):
	for widget in base.winfo_children():
		widget.destroy()
	app.geometry("1100x1200")
	app.minsize(1100, 800)

	treecontainer1 = ttk.Frame(base)
	treecontainer1.pack(padx=5, pady=5, expand=True, fill=BOTH)
	ttk.Label(treecontainer1, text="Ranglista:", font=("TkDefaultFont", 12)).pack(padx=10, pady=(5,0), fill=X)
	randlista = ttk.Treeview(treecontainer1, columns=('helyezes', 'nev', 'pontok'), show='headings', selectmode='browse')
	randlista.heading("helyezes", text="Helyezés")
	randlista.heading("nev", text="Név")
	randlista.heading("pontok", text="Pontok")
	randlista.pack(padx=5, pady=5, expand=True, fill=BOTH, side=LEFT)
	yscroll2 = ttk.Scrollbar(treecontainer1, orient=VERTICAL, command=randlista.yview)
	yscroll2.pack(side=RIGHT, fill=Y)
	randlista.configure(yscrollcommand=yscroll2.set)
	prev = None
	i = 1
	for v in sorted(db.felhasznalok(), key=lambda x: x.pontok, reverse=True):
		if prev and prev.pontok > v.pontok:
			i += 1
		randlista.insert('', 'end', iid=v.id, values=(i, v.nev, v.pontok))
		prev = v

	container2 = ttk.Frame(base)
	container2.pack(padx=5, pady=5, expand=True, fill=BOTH)
	ttk.Label(container2, text="Játék statisztika:", font=("TkDefaultFont", 12)).pack(padx=10, pady=(5,0), fill=X)
	jatekok = ttk.Treeview(container2, columns=('szervezo', 'nev', 'fogadasok', 'tet', 'nyeremeny'), show='headings', selectmode='browse')
	jatekok.heading("szervezo", text="Szervező")
	jatekok.heading("nev", text="Játék")
	jatekok.heading("fogadasok", text="Fogadások")
	jatekok.heading("tet", text="Feltett tétek")
	jatekok.heading("nyeremeny", text="Nyeremény")
	jatekok.pack(padx=5, pady=5, expand=True, fill=BOTH, side=LEFT)
	yscroll1 = ttk.Scrollbar(container2, orient=VERTICAL, command=jatekok.yview)
	yscroll1.pack(side=RIGHT, fill=Y)
	jatekok.configure(yscrollcommand=yscroll1.set)
	gameStatistics = queries.gameStats()
	for v in db.jatekok():
		jatekok.insert('', 'end', iid=v.id, values=(v.szervezo.nev, v.nev, gameStatistics[v.id]['NumOfBets'], gameStatistics[v.id]['BetAmount'], gameStatistics[v.id]['WinAmount']))

	container3 = ttk.Frame(base)
	container3.pack(padx=5, pady=5, expand=True, fill=BOTH)
	ttk.Label(container3, text="Fogadás statisztika:", font=("TkDefaultFont", 12)).pack(padx=10, pady=(5,0), fill=X)
	fogadas = ttk.Treeview(container3, columns=('alany', 'esemeny', 'fogadasok', 'tet', 'nyeremeny'), show='headings', selectmode='browse')
	fogadas.heading("alany", text="Alany")
	fogadas.heading("esemeny", text="Esemeny")
	fogadas.heading("fogadasok", text="Fogadások")
	fogadas.heading("tet", text="Feltett tétek")
	fogadas.heading("nyeremeny", text="Nyeremény")
	fogadas.pack(padx=5, pady=5, expand=True, fill=BOTH, side=LEFT)
	yscroll1 = ttk.Scrollbar(container3, orient=VERTICAL, command=fogadas.yview)
	yscroll1.pack(side=RIGHT, fill=Y)
	fogadas.configure(yscrollcommand=yscroll1.set)
	jatekok.bind('<ButtonRelease-1>', lambda _: _showBets(jatekok.selection()[0]))

	def _showBets(gameId):
		for bet in fogadas.get_children(): fogadas.delete(bet)
		game = db.jatekok(gameId)[0]
		betStatistics = queries.betStats(game)
		for key in betStatistics:
			fogadas.insert('', 'end', iid=None, values=(key.split(';')[1], key.split(';')[0], betStatistics[key]['NumOfBets'], betStatistics[key]['BetAmount'], betStatistics[key]['WinAmount']))

def mode_select():
	global currentUser
	for widget in mainframe.winfo_children():
		widget.destroy()
	app.geometry("600x250")
	app.minsize(600, 250)
	base = ttk.Frame(mainframe)
	base.pack(fill=X)
	content = ttk.Frame(mainframe)
	content.pack(expand=True, fill=BOTH)
	ttk.Label(content, text="Válassz szerepkört!", font=("TkDefaultFont", 15)).pack(padx=5, pady=5)
	ttk.Label(content, text="Fogadó: fogadás leadása és módosítása", font=("TkDefaultFont", 10)).pack(padx=5, pady=5)
	ttk.Label(content, text="Szervező: játékok készítése és lezárása", font=("TkDefaultFont", 10)).pack(padx=5)
	ttk.Label(content, text="Statisztika: ranglista, játék és fogadás statisztika (eredetileg: Lekérdezések)", font=("TkDefaultFont", 10)).pack(padx=5)
	szervezo = ttk.Button(base, text="Szervező", bootstyle="light", 
			command=lambda:(szervezo_view(content), stats.configure(bootstyle="light"), szervezo.configure(bootstyle="primary"), fogado.configure(bootstyle="light")))
	szervezo.pack(padx=10, pady=10, side=LEFT)
	fogado = ttk.Button(base, text="Fogadó", bootstyle="light", 
			command=lambda:(fogado_view(content), stats.configure(bootstyle="light"), szervezo.configure(bootstyle="light"), fogado.configure(bootstyle="primary")))
	fogado.pack(padx=10, pady=10, side=LEFT)
	stats = ttk.Button(base, text="Statisztika", bootstyle="light", 
			command=lambda:(stats_view(content), stats.configure(bootstyle="primary"), szervezo.configure(bootstyle="light"), fogado.configure(bootstyle="light")))
	stats.pack(padx=10, pady=10, side=LEFT)
	menubtn = ttk.Menubutton(base, direction="below", text=currentUser.nev, bootstyle="light")
	menu = ttk.Menu(menubtn, tearoff=0)
	menubtn['menu'] = menu
	menu.add_command(label="Adatok importálása", command=importalas)
	menu.add_separator()
	menu.add_command(label="Jelszó megváltoztatása", command=jelszo_modositas)
	def __logout():
		global currentUser
		currentUser = "kijelentkezve"
		login_view()
	menu.add_command(label="Kijelentkezés", command=__logout)
	menu.add_separator()
	menu.add_command(label="Kilépés", command=lambda: app.destroy())
	menubtn.pack(padx=10, pady=10, side=RIGHT)

def login_view():
	for widget in mainframe.winfo_children():
		widget.destroy()
	app.geometry("400x250")
	app.minsize(400, 250)
	base = ttk.Frame(mainframe)
	base.pack()
	ttk.Label(base, text="Bejelentkezés", font=("TkDefaultFont", 20)).grid(row=0, column=0, columnspan=100, padx=10, pady=10)
	ttk.Label(base, text="Felhasználónév:").grid(row=1, column=0, padx=10, pady=10)
	nev = ttk.Entry(base)
	nev.grid(row=1, column=1, pady=5)
	ttk.Label(base, text="Jelszó:").grid(row=2, column=0, padx=10, pady=10)
	jelszo = ttk.Entry(base, show="*")
	jelszo.grid(row=2, column=1, pady=5)
	ttk.Button(base, text="Kilépés", bootstyle="danger", command=lambda: app.destroy())\
		.grid(row=3, column=0, padx=5, pady=5)
	def __login_or_register(nev, jelszo):
		global currentUser
		currentUser = db.bejelentkezes(nev, jelszo)
		if currentUser == "nincs_ilyen_felhasznalo":
			if Messagebox.show_question("Nincs felhasználó ilyen névvel.\nSzeretnél regisztrálni a megadott adatokkal?", "KandOS - Regisztráció", app, ["Igen:primary", "Nem:Secondary"], True) == "Igen":
				currentUser = db.regisztracio(nev, jelszo)
				mode_select()
		elif currentUser == "helytelen_jelszo":
			Messagebox.show_error("Helytelen jelszó!\nPróbáld újra.", "KandOS - Hiba", app)
		else:
			mode_select()
	ttk.Button(base, text="Tovább >>", bootstyle="success", command=lambda: __login_or_register(nev.get(), jelszo.get()))\
		.grid(row=3, column=1, padx=5, pady=5)
	

login_view()
app.mainloop()