import ttkbootstrap as ttk
from ttkbootstrap.constants import *


app = ttk.Window(title="KandOS", themename='litera')

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

	alanyok = ttk.Treeview(form_frame, columns=("alanyok"), show='headings')
	alanyok.grid(row=2, column=0, padx=5, pady=5)
	alanyok.column("alanyok", anchor=W)
	alanyok.heading("alanyok", text="Alanyok", anchor=W)
	alanyok.bind('<ButtonRelease-1>', lambda _: alanyok.delete(alanyok.selection()) if alanyok.selection() else None)
	
	ujalany = ttk.Entry(form_frame)
	ujalany.bind('<Return>', lambda _: (alanyok.insert('', 'end', values=(ujalany.get())), ujalany.delete(0, END)))
	ujalany.grid(row=3, column=0, padx=5, pady=5)

	esemenyek = ttk.Treeview(form_frame, columns=("esemenyek"), show='headings')
	esemenyek.grid(row=2, column=1, padx=5, pady=5)
	esemenyek.column("esemenyek", anchor=W)
	esemenyek.heading("esemenyek", text="Események", anchor=W)
	esemenyek.bind('<ButtonRelease-1>', lambda _: esemenyek.delete(esemenyek.selection()) if esemenyek.selection() else None)

	ujesemeny = ttk.Entry(form_frame)
	ujesemeny.bind('<Return>', lambda _: (esemenyek.insert('', 'end', values=(ujesemeny.get())), ujesemeny.delete(0, END)))
	ujesemeny.grid(row=3, column=1, padx=5, pady=5)

	ujjatekBTN = ttk.Button(form_frame, text="Játék létrehozása", bootstyle="success", command=lambda: print("ok"))
	ujjatekBTN.grid(row=4, column=0, columnspan=2, padx=5, pady=5)


def fogadas_leadasa(base):
	box = ttk.Toplevel(base)
	box.title("KandOS - Fogadás leadása")
	box.geometry("700x550")
	
	ttk.Label(box, text="Fogadás leadása", font=("TkDefaultFont", 20)).pack(padx=10, pady=4)
	ttk.Label(box, text="Lajos és Bettina programjának futása", font=("TkDefaultFont", 12)).pack(padx=10, pady=5)
	form_frame = ttk.Frame(box)
	form_frame.pack()

	ttk.Label(form_frame, text="Fogadó neve:").grid(row=0, column=0, padx=5, pady=5)
	szervezo = ttk.Entry(form_frame, width=50)
	szervezo.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

	ttk.Label(form_frame, text="Tét (1-100):").grid(row=1, column=0, padx=5, pady=5)
	tet = ttk.Entry(form_frame, width=50, state=DISABLED)
	tet.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

	jatekok = ttk.Treeview(form_frame, columns=('jatekok'), show='headings')
	jatekok.grid(row=2, column=0, padx=5, pady=5)
	jatekok.column("jatekok", anchor=W)
	jatekok.heading("jatekok", text="Játék", anchor=W)
	for i in range(100):
		jatekok.insert('', 'end', values=(i,))

	alanyok = ttk.Treeview(form_frame, columns=('alanyok'), show='headings')
	alanyok.grid(row=2, column=1, padx=5, pady=5)
	alanyok.column("alanyok", anchor=W)
	alanyok.heading("alanyok", text="Alany", anchor=W)

	esemenyek = ttk.Treeview(form_frame, columns=('esemenyek'), show='headings')
	esemenyek.grid(row=2, column=2, padx=5, pady=5)
	esemenyek.column("esemenyek", anchor=W)
	esemenyek.heading("esemenyek", text="Esemény", anchor=W)

	ttk.Label(form_frame, text="Eredmény:").grid(row=3, column=0, padx=5, pady=5)
	eredmeny = ttk.Entry(form_frame, width=50)
	eredmeny.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

	fogadasLeadasaBTN = ttk.Button(form_frame, text="Fogadás leadása", bootstyle="success", command=lambda: print("ok"))
	fogadasLeadasaBTN.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

def jatek_lezarasa(base):
	box = ttk.Toplevel(base)
	box.title("KandOS - Játék lezárása")
	box.geometry("700x550")
	
	ttk.Label(box, text="Játék lezárása", font=("TkDefaultFont", 20)).pack(padx=10, pady=4)
	ttk.Label(box, text="Lajos és Bettina programjának futása", font=("TkDefaultFont", 12)).pack(padx=10, pady=5)
	form_frame = ttk.Frame(box)
	form_frame.pack()

	ttk.Label(form_frame, text="Fogadó neve:").grid(row=0, column=0, padx=5, pady=5)
	szervezo = ttk.Entry(form_frame, width=50)
	szervezo.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

	ttk.Label(form_frame, text="Tét (1-100):").grid(row=1, column=0, padx=5, pady=5)
	tet = ttk.Entry(form_frame, width=50, state=DISABLED)
	tet.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

	jatekok = ttk.Treeview(form_frame, columns=('jatekok'), show='headings')
	jatekok.grid(row=2, column=0, padx=5, pady=5)
	jatekok.column("jatekok", anchor=W)
	jatekok.heading("jatekok", text="Játék", anchor=W)
	for i in range(100):
		jatekok.insert('', 'end', values=(i,))

	alanyok = ttk.Treeview(form_frame, columns=('alanyok'), show='headings')
	alanyok.grid(row=2, column=1, padx=5, pady=5)
	alanyok.column("alanyok", anchor=W)
	alanyok.heading("alanyok", text="Alany", anchor=W)

	esemenyek = ttk.Treeview(form_frame, columns=('esemenyek'), show='headings')
	esemenyek.grid(row=2, column=2, padx=5, pady=5)
	esemenyek.column("esemenyek", anchor=W)
	esemenyek.heading("esemenyek", text="Esemény", anchor=W)

	ttk.Label(form_frame, text="Eredmény:").grid(row=3, column=0, padx=5, pady=5)
	eredmeny = ttk.Entry(form_frame, width=50)
	eredmeny.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

	fogadasLeadasaBTN = ttk.Button(form_frame, text="Fogadás leadása", bootstyle="success", command=lambda: print("ok"))
	fogadasLeadasaBTN.grid(row=4, column=0, columnspan=3, padx=5, pady=5)


mainframe = ttk.Frame(app)
mainframe.pack(fill=BOTH, expand=True, padx=10, pady=10)

tview = ttk.Frame(mainframe)
tview.pack(padx=5, pady=5, expand=True, fill=BOTH)
jatekok = ttk.Treeview(tview, columns=('szervezo', 'nev'), show='headings')
jatekok.heading("szervezo", text="Szervező")
jatekok.heading("nev", text="Játék neve")
jatekok.pack(padx=5, pady=5, expand=True, fill=BOTH, side=LEFT)
yscroll = ttk.Scrollbar(tview, orient=VERTICAL, command=jatekok.yview)
yscroll.pack(side=RIGHT, fill=Y)
jatekok.configure(yscrollcommand=yscroll.set)

for i in range(100):
	jatekok.insert('', 'end', values=(f"Kovács Imre {i}", "Lajos és Bettina programjainak futtatása"))

actionbar = ttk.Frame(mainframe)
actionbar.pack(padx=5, pady=5)
ujjatek = ttk.Button(actionbar, text="Játék létrehozása", bootstyle="success", command=lambda: uj_jatek(app))
ujjatek.pack(padx=5, pady=5, side=LEFT)
fogadas = ttk.Button(actionbar, text="Fogadás leadása", bootstyle="success", command=lambda: fogadas_leadasa(app))
fogadas.pack(padx=5, pady=5, side=LEFT)
lezaras = ttk.Button(actionbar, text="Játék lezárása", bootstyle="warning", command=uj_jatek)
lezaras.pack(padx=5, pady=5, side=LEFT)
lezaras = ttk.Button(actionbar, text="Kilépés", bootstyle="danger", command=lambda: app.destroy())
lezaras.pack(padx=5, pady=5, side=LEFT)

app.geometry("650x500")
app.minsize(600, 400)
app.mainloop()
