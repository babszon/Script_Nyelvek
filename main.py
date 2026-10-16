import csv
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from KF_meresek import KFMeresiSor, KF_szamma


class KFNaploApp:
    def __init__(self, root):
        self.root = root
        self.meresek = KFMeresiSor()
        self.hatar = 50.0
        self.modosult = False
        self.pontok = []
        self.bevitel = tk.StringVar()
        self.hatar_bevitel = tk.StringVar(value="50")
        self.osszefoglalo = tk.StringVar()
        self.reszletek = tk.StringVar()
        self.allapot = tk.StringVar(
            value="Adj hozzá egy mérést, vagy tölts be példát.")
        root.title("Hálózati késleltetésnapló - Kovács Ferenc")
        root.geometry("1060x780")
        root.minsize(960, 740)
        root.protocol("WM_DELETE_WINDOW", self.KF_bezar)
        stilus = ttk.Style(root)
        stilus.theme_use("clam")
        stilus.configure("TLabel", font=("Helvetica", 12))
        stilus.configure("TButton", padding=(10, 7))
        stilus.configure("Treeview", rowheight=26)
        keret = ttk.Frame(root, padding=20)
        keret.pack(fill="both", expand=True)
        ttk.Label(keret, text="Hálózati késleltetésnapló",
                  font=("Helvetica", 22, "bold")).pack(anchor="w")
        ttk.Label(keret, text="Rögzíts válaszidőket, és hasonlítsd "
                  "össze őket.").pack(anchor="w", pady=(5, 16))
        eszkozok = ttk.Frame(keret)
        eszkozok.pack(fill="x", pady=(0, 12))
        for szoveg, muvelet in [
            ("Példa betöltése", self.KF_pelda),
            ("CSV megnyitása", self.KF_megnyit),
            ("CSV mentése", self.KF_ment),
            ("Új adatsor", self.KF_uj),
        ]:
            ttk.Button(eszkozok, text=szoveg, command=muvelet).pack(
                side="left", padx=(0, 8))
        kozep = ttk.Frame(keret)
        kozep.pack(fill="both", expand=True)
        bal = ttk.Frame(kozep, width=300)
        bal.pack(side="left", fill="y", padx=(0, 20))
        bevitel_sor = ttk.Frame(bal)
        bevitel_sor.pack(fill="x", pady=(0, 8))
        ttk.Label(bevitel_sor, text="Válaszidő (ms):").pack(side="left")
        self.mezo = ttk.Entry(bevitel_sor, textvariable=self.bevitel, width=10)
        self.mezo.pack(side="left", padx=8)
        self.mezo.bind("<Return>", self.KF_hozzaad)
        ttk.Button(bal, text="Mérés hozzáadása", command=self.KF_hozzaad).pack(
            fill="x", pady=(0, 12))
        tabla_keret = ttk.Frame(bal)
        tabla_keret.pack(fill="both", expand=True)
        self.tabla = ttk.Treeview(
            tabla_keret, columns=("sorszam", "ms", "jelzes"),
            show="headings", selectmode="browse", height=12)
        for oszlop, cim, szelesseg in [
            ("sorszam", "Mérés", 58),
            ("ms", "Válaszidő (ms)", 105),
            ("jelzes", "Határ felett", 100),
        ]:
            self.tabla.heading(oszlop, text=cim)
            self.tabla.column(oszlop, width=szelesseg, anchor="center")
        gorgeto = ttk.Scrollbar(tabla_keret, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=gorgeto.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        gorgeto.pack(side="right", fill="y")
        self.tabla.tag_configure("magas", foreground="#a33a27")
        self.tabla.bind("<<TreeviewSelect>>", self.KF_kijelol)
        ttk.Button(bal, text="Kijelölt mérés törlése",
                   command=self.KF_torol).pack(fill="x", pady=(10, 0))
        jobb = ttk.Frame(kozep)
        jobb.pack(side="left", fill="both", expand=True)
        hatar_sor = ttk.Frame(jobb)
        hatar_sor.pack(fill="x", pady=(0, 10))
        ttk.Label(hatar_sor, text="Figyelmeztetési határ (ms):").pack(
            side="left")
        hatar_mezo = ttk.Entry(
            hatar_sor, textvariable=self.hatar_bevitel, width=8)
        hatar_mezo.pack(side="left", padx=8)
        hatar_mezo.bind("<Return>", self.KF_hatar)
        ttk.Button(hatar_sor, text="Alkalmaz", command=self.KF_hatar).pack(
            side="left")
        self.rajz = tk.Canvas(jobb, background="white", highlightthickness=1,
                              highlightbackground="#ccd2d6", height=285)
        self.rajz.pack(fill="both", expand=True)
        self.rajz.bind("<Configure>", self.KF_rajzol)
        self.rajz.bind("<Button-1>", self.KF_grafikon_kattintas)
        ttk.Label(jobb, text="Kék: mérés   Piros: határ felett   "
                  "Szaggatott: határ",
                  font=("Helvetica", 10)).pack(anchor="w", pady=(6, 10))
        ttk.Label(jobb, textvariable=self.osszefoglalo,
                  font=("Helvetica", 14, "bold")).pack(anchor="w")
        ttk.Label(jobb, textvariable=self.reszletek,
                  justify="left").pack(anchor="w", pady=7)
        ttk.Label(jobb, text="A grafikon pontjára kattintva "
                  "kijelölheted a mérést.",
                  font=("Helvetica", 10)).pack(anchor="w")
        ttk.Separator(keret).pack(fill="x", pady=(14, 9))
        ttk.Label(keret, textvariable=self.allapot,
                  font=("Helvetica", 11)).pack(anchor="w")
        self.KF_frissit()
        self.mezo.focus_set()

    def KF_hozzaad(self, event=None):
        try:
            self.meresek.KF_hozzaad(self.bevitel.get())
        except ValueError as hiba:
            messagebox.showerror("Hibás mérés", str(hiba), parent=self.root)
            return
        self.bevitel.set("")
        self.modosult = True
        self.KF_frissit()
        self.KF_sor_kivalaszt(len(self.meresek.ertekek) - 1)
        self.allapot.set("Mérés hozzáadva. Az adatsort CSV-fájlba mentheted.")
        self.mezo.focus_set()

    def KF_torol(self):
        kijelolt = self.tabla.selection()
        if not kijelolt:
            self.allapot.set("Először jelölj ki egy mérést a táblázatban.")
            return
        self.meresek.KF_torol(int(kijelolt[0]))
        self.modosult = True
        self.KF_frissit()
        self.allapot.set("A mérés törölve. A sorszámok újraszámozódtak.")

    def KF_hatar(self, event=None):
        try:
            self.hatar = KF_szamma(self.hatar_bevitel.get())
        except ValueError as hiba:
            messagebox.showerror(
                "Hibás határérték", str(hiba), parent=self.root)
            return
        self.KF_frissit()
        self.allapot.set(f"A határérték {self.hatar:g} ms. "
                         "Ez saját összehasonlítási érték.")

    def KF_ment(self):
        if not self.meresek.ertekek:
            self.allapot.set("Még nincs menthető mérés.")
            return False
        utvonal = filedialog.asksaveasfilename(
            parent=self.root, title="Mérések mentése", defaultextension=".csv",
            initialfile="meresek.csv", filetypes=[("CSV-fájl", "*.csv")])
        if not utvonal:
            return False
        try:
            self.meresek.KF_ment(utvonal)
        except OSError as hiba:
            messagebox.showerror(
                "Sikertelen mentés", str(hiba), parent=self.root)
            return False
        self.modosult = False
        self.allapot.set(f"Mentve: {Path(utvonal).name}")
        return True

    def KF_elhagyhato(self):
        if not self.modosult:
            return True
        valasz = messagebox.askyesnocancel(
            "Nem mentett mérések", "Elmented az adatsort a folytatás előtt?",
            parent=self.root)
        if valasz is None:
            return False
        if valasz:
            return self.KF_ment()
        return True

    def KF_betolt(self, utvonal, pelda=False):
        try:
            self.meresek.KF_betolt(utvonal)
        except (OSError, UnicodeError, ValueError, csv.Error) as hiba:
            messagebox.showerror(
                "Sikertelen megnyitás", str(hiba), parent=self.root)
            return
        self.modosult = False
        self.KF_frissit()
        if pelda:
            self.allapot.set("Példaadatok betöltve. "
                             "Ezek kitalált, szemléltető értékek.")
        else:
            self.allapot.set(f"Betöltve: {Path(utvonal).name}")

    def KF_pelda(self):
        if self.KF_elhagyhato():
            self.KF_betolt(Path(__file__).with_name("pelda_meresek.csv"), True)

    def KF_megnyit(self):
        if not self.KF_elhagyhato():
            return
        utvonal = filedialog.askopenfilename(
            parent=self.root, title="Mérések megnyitása",
            filetypes=[("CSV-fájl", "*.csv"), ("Minden fájl", "*")])
        if utvonal:
            self.KF_betolt(utvonal)

    def KF_uj(self):
        if self.KF_elhagyhato():
            self.meresek = KFMeresiSor()
            self.modosult = False
            self.KF_frissit()
            self.allapot.set("Új, üres adatsor.")

    def KF_bezar(self):
        if self.KF_elhagyhato():
            self.root.destroy()

    def KF_frissit(self):
        self.tabla.delete(*self.tabla.get_children())
        for index, ertek in enumerate(self.meresek.ertekek):
            magas = ertek > self.hatar
            self.tabla.insert(
                "", "end", iid=str(index),
                values=(index + 1, f"{ertek:.2f}", "igen" if magas else "-"),
                tags=("magas",) if magas else ())
        adatok = self.meresek.KF_statisztika(self.hatar)
        if adatok is None:
            self.osszefoglalo.set("Még nincs mérés.")
            self.reszletek.set(
                "Az átlag, a medián és a szórás itt jelenik meg.")
        else:
            self.osszefoglalo.set(f"{adatok['darab']} mérés | "
                                 f"Átlag: {adatok['atlag']:.2f} ms")
            self.reszletek.set(
                f"Medián: {adatok['median']:.2f} ms    "
                f"Szórás: {adatok['szoras']:.2f} ms\n"
                f"Minimum: {adatok['minimum']:.2f} ms    "
                f"Maximum: {adatok['maximum']:.2f} ms\n"
                f"Határ felett: {adatok['hatar_felett']} / {adatok['darab']}")
        self.KF_rajzol()

    def KF_rajzol(self, event=None):
        self.rajz.delete("all")
        self.pontok = []
        szelesseg = self.rajz.winfo_width()
        magassag = self.rajz.winfo_height()
        if szelesseg < 120 or magassag < 100:
            return
        if not self.meresek.ertekek:
            self.rajz.create_text(szelesseg / 2, magassag / 2,
                                  text="A mérések grafikonja itt jelenik meg.",
                                  fill="#66727b", font=("Helvetica", 12))
            return
        bal, jobb, fent, lent = 62, szelesseg - 22, 30, magassag - 42
        maximum = max(max(self.meresek.ertekek), self.hatar, 1) * 1.15
        for index in range(5):
            ertek = maximum * index / 4
            y = lent - (lent - fent) * ertek / maximum
            self.rajz.create_line(bal, y, jobb, y, fill="#e6e9ec")
            self.rajz.create_text(bal - 8, y, text=f"{ertek:.0f}",
                                  anchor="e", fill="#3f4850")
        self.rajz.create_text(bal, 13, text="Válaszidő (ms)",
                              anchor="w", fill="#3f4850")
        self.rajz.create_line(bal, fent, bal, lent, jobb, lent, fill="#7d8790")
        hatar_y = lent - (lent - fent) * self.hatar / maximum
        self.rajz.create_line(bal, hatar_y, jobb, hatar_y,
                              fill="#a33a27", dash=(5, 4))
        darab = len(self.meresek.ertekek)
        for index, ertek in enumerate(self.meresek.ertekek):
            x = bal + (jobb - bal) * index / max(darab - 1, 1)
            y = lent - (lent - fent) * ertek / maximum
            self.pontok.append((x, y))
        for index in range(1, darab):
            self.rajz.create_line(*self.pontok[index - 1], *self.pontok[index],
                                  fill="#246884", width=2)
        kijelolt = self.tabla.selection()
        for index, (x, y) in enumerate(self.pontok):
            magas = self.meresek.ertekek[index] > self.hatar
            szin = "#a33a27" if magas else "#246884"
            sugar = 5 if kijelolt == (str(index),) else 3
            self.rajz.create_oval(x - sugar, y - sugar, x + sugar, y + sugar,
                                  fill=szin, outline="white")
        lepes = max(1, (darab - 1 + 4) // 5)
        for index in range(darab):
            if index % lepes == 0 or index == darab - 1:
                self.rajz.create_text(self.pontok[index][0], lent + 15,
                                      text=str(index + 1), fill="#3f4850")
        self.rajz.create_text((bal + jobb) / 2, magassag - 9,
                              text="Mérés sorszáma", fill="#3f4850")

    def KF_kijelol(self, event=None):
        kijelolt = self.tabla.selection()
        if kijelolt:
            index = int(kijelolt[0])
            self.allapot.set(f"{index + 1}. mérés: "
                             f"{self.meresek.ertekek[index]:.2f} ms")
        self.KF_rajzol()

    def KF_sor_kivalaszt(self, index):
        self.tabla.selection_set(str(index))
        self.tabla.see(str(index))

    def KF_grafikon_kattintas(self, event):
        if not self.pontok:
            return
        tavolsagok = [(x - event.x) ** 2 + (y - event.y) ** 2
                      for x, y in self.pontok]
        index = tavolsagok.index(min(tavolsagok))
        if tavolsagok[index] <= 400:
            self.KF_sor_kivalaszt(index)


if __name__ == "__main__":
    root = tk.Tk()
    app = KFNaploApp(root)
    root.mainloop()
