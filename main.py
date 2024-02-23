import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs.dialogs import Messagebox
import queries
import db


app = ttk.Window(title="KandOS", themename='litera')

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
	ujalany.bind('<Return>', lambda _: (alanyok.insert('', 'end', values=(ujalany.get())), ujalany.delete(0, END)) if ujalany.get() else None)
	ujalany.grid(row=3, column=0, padx=5, pady=5)

	esemenyek = ttk.Treeview(form_frame, columns=("esemenyek"), show='headings', selectmode='browse')
	esemenyek.grid(row=2, column=1, padx=5, pady=5)
	esemenyek.column("esemenyek", anchor=W)
	esemenyek.heading("esemenyek", text="Események", anchor=W)
	esemenyek.bind('<ButtonRelease-1>', lambda _: esemenyek.delete(esemenyek.selection()) if esemenyek.selection() else None)

	ujesemeny = ttk.Entry(form_frame)
	ujesemeny.bind('<Return>', lambda _: (esemenyek.insert('', 'end', values=(ujesemeny.get())), ujesemeny.delete(0, END)) if ujesemeny.get() else None)
	ujesemeny.grid(row=3, column=1, padx=5, pady=5)

	def __cmd():
		try:
			if not (jatekneve.get() and alanyok.get_children() and esemenyek.get_children()):
				raise Exception("Kitöltetlen mezők")
			db.uj_jatek(currentUser.id, jatekneve.get(), set([alanyok.item(x)["values"][0] for x in alanyok.get_children()]), set([esemenyek.item(x)["values"][0] for x in esemenyek.get_children()]))
			box.destroy()
			updateAll()
		except Exception as e:
			print(e)
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
			print(e)
			Messagebox.show_error("Hiba történt a fogadás leadása közben.\nEllenőrizd, hogy mindent helyesen adtál-e meg és próbáld újra!", "KandOS - Hiba", box)
	fogadasLeadasaBTN = ttk.Button(form_frame, text="Fogadás leadása", bootstyle="success", command=__cmd)
	fogadasLeadasaBTN.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

def jatek_lezarasa(base, jatekId: int):
	jatek = db.jatekok(jatekId)[0]
	box = ttk.Toplevel(base)
	box.title("KandOS - Játék lezárása")
	box.geometry("700x550")
	
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
			eredmenyek[alany][esemeny] = ttk.Entry(alany_frame).grid(row=i//2+1, column=1 if i%2==0 else 3, padx=5, pady=5)
		alany_frame.pack(padx=5, pady=8)

	lezarasBTN = ttk.Button(box, text="Játék lezárása", bootstyle="warning", command=lambda: print("ok"))
	lezarasBTN.pack(padx=5, pady=5)

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


mainframe = ttk.Frame(app)
mainframe.pack(fill=BOTH, expand=True, padx=10, pady=10)

def szervezo_view(base):
	for widget in base.winfo_children():
		widget.destroy()
	app.geometry("700x500")
	app.minsize(600, 400)
	ttk.Label(base, text="Játékaim:", font=("TkDefaultFont", 12)).pack(padx=10, pady=(5,0), fill=X)
	treecontainer = ttk.Frame(base)
	treecontainer.pack(padx=5, pady=5, expand=True, fill=BOTH)
	jatekok = ttk.Treeview(treecontainer, columns=('nev', 'lezart', 'autolezar'), show='headings', selectmode='browse')
	jatekok.heading("nev", text="Játék neve")
	jatekok.heading("lezart", text="Lezárt")
	jatekok.heading("autolezar", text="Automatikus lezárás")
	jatekok.pack(padx=5, pady=5, expand=True, fill=BOTH, side=LEFT)
	yscroll = ttk.Scrollbar(treecontainer, orient=VERTICAL, command=jatekok.yview)
	yscroll.pack(side=RIGHT, fill=Y)
	jatekok.configure(yscrollcommand=yscroll.set)
	def update_jatekok():
		for item in jatekok.get_children():
			jatekok.delete(item)
		nemlezart = [x.id for x in db.jatekok(felhasznaloId=currentUser.id, include_lezart=False)]
		for v in db.jatekok(felhasznaloId=currentUser.id):
			jatekok.insert('', 'end', iid=v.id, values=(v.nev, 'Nem' if v.id in nemlezart else 'Igen', '2024.02.23 14:33'))
	updaters.append(update_jatekok)
	update_jatekok()

	actionbar = ttk.Frame(base)
	actionbar.pack(padx=5, pady=5)
	ujjatek = ttk.Button(actionbar, text="Új játék", bootstyle="success", command=lambda: uj_jatek(app))
	ujjatek.pack(padx=5, pady=5, side=LEFT)
	lezaras = ttk.Button(actionbar, text="Játék lezárása", bootstyle="warning", command=lambda: jatek_lezarasa(app, jatekok.selection()[0]) if jatekok.selection() else Messagebox.show_error("Válassz egy játékot!", "KandOS - Hiba", app))
	lezaras.pack(padx=5, pady=5, side=LEFT)
	
def fogado_view(base):
	for widget in base.winfo_children():
		widget.destroy()
	app.geometry("1200x800")
	app.minsize(1200, 800)
	
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

	ttk.Label(base, text="Fogadásaim:", font=("TkDefaultFont", 12)).pack(padx=10, pady=(5,0), fill=X)
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
		for v in db.fogadasok(felhasznaloId=currentUser.id):
			fogadasaim.insert('', 'end', iid=v.id, values=(v.jatek.nev, v.alany, v.esemeny, v.ertek, v.osszeg))
	updaters.append(update_fogadasaim)
	update_fogadasaim()

	actionbar = ttk.Frame(base)
	actionbar.pack(padx=5, pady=5)
	leadas = ttk.Button(actionbar, text="Fogadás leadása", bootstyle="success", 
			command=lambda: fogadas_leadasa(app, jatekok.selection()[0]) if jatekok.selection() else Messagebox.show_error("Válassz egy játékot!", "KandOS - Hiba", app))
	leadas.pack(padx=5, pady=5, side=LEFT)
	modositas = ttk.Button(actionbar, text="Fogadás módosítása", bootstyle="success", 
			command=lambda: jatek_lezarasa(app, jatekok.selection()[0]) if jatekok.selection() else Messagebox.show_error("Válassz egy játékot!", "KandOS - Hiba", app))
	modositas.pack(padx=5, pady=5, side=LEFT)
	torles = ttk.Button(actionbar, text="Fogadás törlése", bootstyle="warning", 
			command=lambda: jatek_lezarasa(app, jatekok.selection()[0]) if jatekok.selection() else Messagebox.show_error("Válassz egy játékot!", "KandOS - Hiba", app))
	torles.pack(padx=5, pady=5, side=LEFT)

def mode_select():
	global currentUser
	for widget in mainframe.winfo_children():
		widget.destroy()
	app.geometry("400x200")
	app.minsize(400, 200)
	base = ttk.Frame(mainframe)
	base.pack(fill=X)
	content = ttk.Frame(mainframe)
	content.pack(expand=True, fill=BOTH)
	ttk.Label(content, text="Válassz szerepkört!", font=("TkDefaultFont", 15)).pack(padx=5, pady=5)
	ttk.Label(content, text="Fogadó: fogadás leadása és módosítása", font=("TkDefaultFont", 10)).pack(padx=5, pady=5)
	ttk.Label(content, text="Szervező: játékok készítése és lezárása", font=("TkDefaultFont", 10)).pack(padx=5)
	szervezo = ttk.Button(base, text="Szervező", bootstyle="light", 
			command=lambda:(szervezo_view(content), szervezo.configure(bootstyle="primary"), fogado.configure(bootstyle="light")))
	szervezo.pack(padx=10, pady=10, side=LEFT)
	fogado = ttk.Button(base, text="Fogadó", bootstyle="light", 
			command=lambda:(fogado_view(content), szervezo.configure(bootstyle="light"), fogado.configure(bootstyle="primary")))
	fogado.pack(padx=10, pady=10, side=LEFT)
	menubtn = ttk.Menubutton(base, direction="below", text=currentUser.nev, bootstyle="light")
	menu = ttk.Menu(menubtn, tearoff=0)
	menubtn['menu'] = menu
	menu.add_command(label="Jelszó megváltoztatása", command=jelszo_modositas)
	menu.add_command(label="Kijelentkezés", command=logout)
	menu.add_separator()
	menu.add_command(label="Kilépés", command=lambda: app.destroy())
	menubtn.pack(padx=10, pady=10, side=RIGHT)

def logout():
	global currentUser
	currentUser = "kijelentkezve"
	login_view()

def login_or_register(nev, jelszo):
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
	ttk.Button(base, text="Tovább >>", bootstyle="success", command=lambda: login_or_register(nev.get(), jelszo.get()))\
		.grid(row=3, column=1, padx=5, pady=5)

# TODO: fogadas vagy szervezes view válaszó ✅
# TODO: user menu jobb felül és szerepkör választó bal felül ✅
# TODO: fogado view: saját fogadásaim, fogadás törlése?, elérhető jatekok ✅
# TODO: szervezo view: saját versenyeim, lezárás lehetősége, új verseny ✅
# TODO: automatikusan lezáruló játékok (idő) 🧠
	

login_view()
app.mainloop()
