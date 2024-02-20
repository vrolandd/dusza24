import ttkbootstrap as ttk
from ttkbootstrap.constants import *


app = ttk.Window(title="KandOS", themename='litera')

content_box = ttk.Frame(app)
content_box.pack(side=RIGHT, expand=YES, fill=BOTH, padx=10, pady=10)

def uj_jatek(parent):
	for widget in parent.winfo_children():
		widget.destroy()
	ttk.Label(parent, text="Játék létrehozása", font=("TkDefaultFont", 20)).pack(padx=10, pady=10)
	form_frame = ttk.Frame(parent)
	form_frame.pack()
	ttk.Label(form_frame, text="Szervező:").grid(row=0, column=0, padx=5, pady=5)
	szervezo = ttk.Entry(form_frame)
	szervezo.grid(row=0, column=1, padx=5, pady=5)
	ttk.Label(form_frame, text="Játék neve:").grid(row=1, column=0, padx=5, pady=5)
	jatekneve = ttk.Entry(form_frame)
	jatekneve.grid(row=1, column=1, padx=5, pady=5)

	alanyok = ttk.Treeview(form_frame, columns=('1', '2'), show='headings')
	alanyok.grid(row=2, column=0, padx=5, pady=5)
	alanyok["columns"] = ("alanyok")
	alanyok.column("alanyok", anchor=W)
	alanyok.heading("alanyok", text="Alanyok", anchor=W)
	alanyok.bind('<ButtonRelease-1>', lambda _: alanyok.delete(alanyok.selection()) if alanyok.selection() else None)
	
	ujalany = ttk.Entry(form_frame)
	ujalany.bind('<Return>', lambda _: (alanyok.insert('', 'end', values=(ujalany.get())), ujalany.delete(0, END)))
	ujalany.grid(row=3, column=0, padx=5, pady=5)

	esemenyek = ttk.Treeview(form_frame, columns=('1', '2'), show='headings')
	esemenyek.grid(row=2, column=1, padx=5, pady=5)
	esemenyek["columns"] = ("esemenyek")
	esemenyek.column("esemenyek", anchor=W)
	esemenyek.heading("esemenyek", text="Események", anchor=W)
	esemenyek.bind('<ButtonRelease-1>', lambda _: esemenyek.delete(esemenyek.selection()) if esemenyek.selection() else None)

	ujesemeny = ttk.Entry(form_frame)
	ujesemeny.bind('<Return>', lambda _: (esemenyek.insert('', 'end', values=(ujesemeny.get())), ujesemeny.delete(0, END)))
	ujesemeny.grid(row=3, column=1, padx=5, pady=5)

	ujjatekBTN = ttk.Button(form_frame, text="Játék létrehozása", bootstyle="success", command=lambda: print(szervezo.get(), jatekneve.get(), alanyok.get_children(), esemenyek.get_children()))
	ujjatekBTN.grid(row=4, column=0, columnspan=2, padx=5, pady=5)


buttons = {
	'Játék Létrehozása': lambda: uj_jatek(content_box),
	'Fogadás Leadása': lambda: app.quit(),
	'Játék Lezárása': lambda: app.quit(),
	'Lekérdezések': lambda: app.quit(),
	'Kilépés': lambda: app.quit(),
}
sidebar = ttk.Frame(app, width=200)
sidebar.pack(side=LEFT, fill=Y, padx=(10, 0), pady=10)
for label, func in buttons.items():
	btn = ttk.Button(sidebar, text=label, command=func)
	btn.pack(fill=X, padx=10, pady=5)

app.mainloop()
