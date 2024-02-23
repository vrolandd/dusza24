import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs.dialogs import Messagebox
import db


app = ttk.Window(title="KandOS", themename='litera')

currentUser: db.models.Felhasznalo | str = "kijelentkezve"

def uj_jatek(base):
	box = ttk.Toplevel(base)
	box.title("KandOS - Játék létrehozása")
	box.geometry("500x500")
	ttk.Label(box, text="Játék létrehozása", font=("TkDefaultFont", 20)).pack(padx=10, pady=10)
	form_frame = ttk.Frame(box)
	form_frame.pack()
	ttk.Label(form_frame, text="Szervező:").grid(row=0, column=0, padx=5, pady=5)
	szervezo = ttk.Entry(form_frame)
	szervezo.grid(row=0, column=1, padx=5, pady=5)
	ttk.Label(form_frame, text="Játék neve:").grid(row=1, column=0, padx=5, pady=5)
	jatekneve = ttk.Entry(form_frame)
	jatekneve.grid(row=1, column=1, padx=5, pady=5)

	alanyok = ttk.Treeview(form_frame, columns=("alanyok"), show='headings', selectmode='browse')
	alanyok.grid(row=2, column=0, padx=5, pady=5)
	alanyok.column("alanyok", anchor=W)
	alanyok.heading("alanyok", text="Alanyok", anchor=W)
	alanyok.bind('<ButtonRelease-1>', lambda _: alanyok.delete(alanyok.selection()) if alanyok.selection() else None)
	
	ujalany = ttk.Entry(form_frame)
	ujalany.bind('<Return>', lambda _: (alanyok.insert('', 'end', values=(ujalany.get())), ujalany.delete(0, END)))
	ujalany.grid(row=3, column=0, padx=5, pady=5)

	esemenyek = ttk.Treeview(form_frame, columns=("esemenyek"), show='headings', selectmode='browse')
	esemenyek.grid(row=2, column=1, padx=5, pady=5)
	esemenyek.column("esemenyek", anchor=W)
	esemenyek.heading("esemenyek", text="Események", anchor=W)
	esemenyek.bind('<ButtonRelease-1>', lambda _: esemenyek.delete(esemenyek.selection()) if esemenyek.selection() else None)

	ujesemeny = ttk.Entry(form_frame)
	ujesemeny.bind('<Return>', lambda _: (esemenyek.insert('', 'end', values=(ujesemeny.get())), ujesemeny.delete(0, END)))
	ujesemeny.grid(row=3, column=1, padx=5, pady=5)

	ujjatekBTN = ttk.Button(form_frame, text="Játék létrehozása", bootstyle="success", command=lambda: print("ok"))
	ujjatekBTN.grid(row=4, column=0, columnspan=2, padx=5, pady=5)


def fogadas_leadasa(base, jatekId:int):
	box = ttk.Toplevel(base)
	box.title("KandOS - Fogadás leadása")
	box.geometry("500x550")
	
	ttk.Label(box, text="Fogadás leadása", font=("TkDefaultFont", 20)).pack(padx=10, pady=4)
	ttk.Label(box, text="Lajos és Bettina programjának futása", font=("TkDefaultFont", 12)).pack(padx=10, pady=5)
	
	form_frame = ttk.Frame(box)
	form_frame.pack()

	ttk.Label(form_frame, text="Fogadó neve:").grid(row=0, column=0, padx=5, pady=5)
	szervezo = ttk.Entry(form_frame, width=25)
	szervezo.grid(row=0, column=1, padx=5, pady=5)

	ttk.Label(form_frame, text="Tét (1-100):").grid(row=1, column=0, padx=5, pady=5)
	tet = ttk.Entry(form_frame, width=25, state=DISABLED)
	tet.grid(row=1, column=1, padx=5, pady=5)

	alanyok = ttk.Treeview(form_frame, columns=('alanyok'), show='headings', selectmode='browse')
	alanyok.grid(row=2, column=0, padx=5, pady=5)
	alanyok.column("alanyok", anchor=W)
	alanyok.heading("alanyok", text="Alany", anchor=W)

	esemenyek = ttk.Treeview(form_frame, columns=('esemenyek'), show='headings', selectmode='browse')
	esemenyek.grid(row=2, column=1, padx=5, pady=5)
	esemenyek.column("esemenyek", anchor=W)
	esemenyek.heading("esemenyek", text="Esemény", anchor=W)

	ttk.Label(form_frame, text="Eredmény:").grid(row=3, column=0, padx=5, pady=5)
	eredmeny = ttk.Entry(form_frame, width=25)
	eredmeny.grid(row=3, column=1, padx=5, pady=5)

	fogadasLeadasaBTN = ttk.Button(form_frame, text="Fogadás leadása", bootstyle="success", command=lambda: print("ok"))
	fogadasLeadasaBTN.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

def jatek_lezarasa(base, jatekId:int):
	box = ttk.Toplevel(base)
	box.title("KandOS - Játék lezárása")
	box.geometry("700x550")
	
	ttk.Label(box, text="Játék lezárása", font=("TkDefaultFont", 20)).pack(padx=10, pady=4)
	ttk.Label(box, text="Lajos és Bettina programjának futása", font=("TkDefaultFont", 12)).pack(padx=10, pady=5)
	
	form_frame = ScrolledFrame(box)
	form_frame.pack(padx=5, pady=5, expand=True, fill=BOTH)

	for i in range(20):
		asdf = ttk.Frame(form_frame)
		ttk.Label(asdf, text=f"{i}. alany eredményei").grid(row=0, column=0, padx=5, pady=5)
		ttk.Label(asdf, text="Esemény 1:").grid(row=1, column=0, padx=5, pady=5)
		ttk.Entry(asdf).grid(row=1, column=1, padx=5, pady=5)
		ttk.Label(asdf, text="Esemény 2:").grid(row=1, column=2, padx=5, pady=5)
		ttk.Entry(asdf).grid(row=1, column=3, padx=5, pady=5)
		ttk.Label(asdf, text="Esemény 3:").grid(row=2, column=0, padx=5, pady=5)
		ttk.Entry(asdf).grid(row=2, column=1, padx=5, pady=5)
		ttk.Label(asdf, text="Esemény 4:").grid(row=2, column=2, padx=5, pady=5)
		ttk.Entry(asdf).grid(row=2, column=3, padx=5, pady=5)
		asdf.pack(padx=5, pady=8)


	lezarasBTN = ttk.Button(box, text="Játék lezárása", bootstyle="warning", command=lambda: print("ok"))
	lezarasBTN.pack(padx=5, pady=5)


mainframe = ttk.Frame(app)
mainframe.pack(fill=BOTH, expand=True, padx=10, pady=10)

def majd_kirotlom_de_most_jo():
	app.geometry("650x500")
	app.minsize(600, 400)
	for widget in mainframe.winfo_children():
		widget.destroy()
	treecontainer = ttk.Frame(mainframe)
	treecontainer.pack(padx=5, pady=5, expand=True, fill=BOTH)
	jatekok = ttk.Treeview(treecontainer, columns=('szervezo', 'nev'), show='headings', selectmode='browse')
	jatekok.heading("szervezo", text="Szervező")
	jatekok.heading("nev", text="Játék neve")
	jatekok.pack(padx=5, pady=5, expand=True, fill=BOTH, side=LEFT)
	yscroll = ttk.Scrollbar(treecontainer, orient=VERTICAL, command=jatekok.yview)
	yscroll.pack(side=RIGHT, fill=Y)
	jatekok.configure(yscrollcommand=yscroll.set)

	for v in db.jatekok():
		jatekok.insert('', 'end', iid=v.id, values=(v.szervezo.nev, v.nev))

	actionbar = ttk.Frame(mainframe)
	actionbar.pack(padx=5, pady=5)
	ujjatek = ttk.Button(actionbar, text="Játék létrehozása", bootstyle="success", command=lambda: uj_jatek(app))
	ujjatek.pack(padx=5, pady=5, side=LEFT)
	fogadas = ttk.Button(actionbar, text="Fogadás leadása", bootstyle="success", command=lambda: fogadas_leadasa(app, jatekok.selection()[0]) if jatekok.selection() else Messagebox.show_error("Válassz egy játékot!", "KandOS - Hiba", app))
	fogadas.pack(padx=5, pady=5, side=LEFT)
	lezaras = ttk.Button(actionbar, text="Játék lezárása", bootstyle="warning", command=lambda: jatek_lezarasa(app, jatekok.selection()[0]) if jatekok.selection() else Messagebox.show_error("Válassz egy játékot!", "KandOS - Hiba", app))
	lezaras.pack(padx=5, pady=5, side=LEFT)
	lezaras = ttk.Button(actionbar, text="Kilépés", bootstyle="danger", command=lambda: app.destroy())
	lezaras.pack(padx=5, pady=5, side=LEFT)

def szervezo_view(base):
	for widget in base.winfo_children():
		widget.destroy()
	app.geometry("700x500")
	app.minsize(600, 400)
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

	for v in db.jatekok():
		jatekok.insert('', 'end', iid=v.id, values=(v.nev, 'Nem', '2024.02.23 14:33'))

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
	for v in db.jatekok():
		jatekok.insert('', 'end', iid=v.id, values=(v.nev, v.szervezo.nev))

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
	for v in db.fogadasok():
		fogadasaim.insert('', 'end', iid=v.id, values=(v.jatek.nev, v.alany, v.esemeny, v.ertek, v.osszeg))

	actionbar = ttk.Frame(base)
	actionbar.pack(padx=5, pady=5)
	ujjatek = ttk.Button(actionbar, text="Fogadás leadása", bootstyle="success", command=lambda: uj_jatek(app))
	ujjatek.pack(padx=5, pady=5, side=LEFT)
	lezaras = ttk.Button(actionbar, text="Fogadás módosítása", bootstyle="success", 
			command=lambda: jatek_lezarasa(app, jatekok.selection()[0]) if jatekok.selection() else Messagebox.show_error("Válassz egy játékot!", "KandOS - Hiba", app))
	lezaras.pack(padx=5, pady=5, side=LEFT)
	lezaras = ttk.Button(actionbar, text="Fogadás törlése", bootstyle="warning", 
			command=lambda: jatek_lezarasa(app, jatekok.selection()[0]) if jatekok.selection() else Messagebox.show_error("Válassz egy játékot!", "KandOS - Hiba", app))
	lezaras.pack(padx=5, pady=5, side=LEFT)

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
	menu.add_command(label="Jelszó megváltoztatása")
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
