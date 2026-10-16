# Hálózati késleltetésnapló

## Hallgató

Kovács Ferenc (KF) - GVNY7C

## Feladat leírása

A program kézzel megadott hálózati válaszidőket tárol. Egy mérési sorból
kirajzolja a válaszidők alakulását, és kiszámítja az átlagot, a mediánt,
a szórást, a minimumot és a maximumot. A felhasználó saját határértéket
állíthat be; az ennél nagyobb válaszidők piros jelölést kapnak.

Egy hálózati gyakorlat során rögzített válaszidőket így egy helyen lehet
áttekinteni. A program nem indít pinget, a válaszidőket a felhasználó adja
meg vagy CSV-fájlból tölti be.

## Indítás

Python 3.10 vagy újabb, Tkinter-támogatással. Külső Python-csomag nem kell.

A projekt mappájában:

```text
python3 KF_kornyezet.py
.venv/bin/python main.py
```

Windows alatt:

```text
py KF_kornyezet.py
.venv\Scripts\python.exe main.py
```

A `KF_kornyezet.py` a `venv` modullal hoz létre egy helyi `.venv` mappát.
Az elkészült környezet a létrehozásához használt Python Tkinter-támogatását
használja. Meglévő, megfelelő Pythonból a `python3 main.py` közvetlen indítás is működik.

A belépési fájl `main.py`. Az alapablak változója `root`, a programé `app`.

## Használat

1. A **Példa betöltése** gombbal kipróbálható a program. A mellékelt
   értékek kitalált, szemléltető adatok.
2. A válaszidő mezőbe írt számot a **Mérés hozzáadása** gomb vagy az Enter
   rögzíti. Tizedesvessző és tizedespont is használható.
3. A figyelmeztetési határ módosítását az **Alkalmaz** gomb vagy az Enter
   érvényesíti. A határral egyenlő érték nem számít határ felettinek.
4. A grafikon egy pontjára kattintva a hozzá tartozó sor kijelölődik.
   A táblázatban is választható sor, majd törölhető a kijelölt mérés.
5. Az adatsor CSV-be menthető és később visszaolvasható. Új adatsor,
   betöltés vagy kilépés előtt a program rákérdez a nem mentett változásokra.

Egy adatsor legfeljebb 500 mérést fogad, egy mérés 0 és 60000 ms közötti
véges szám lehet. A határérték ugyanebbe a tartományba eshet. A grafikon
a mérések sorrendjét mutatja; nem feltételez azonos időközöket.

## CSV-formátum

UTF-8 szöveg, egy oszlop, az első sor kötelező neve `kesleltetes_ms`.
Például:

```text
kesleltetes_ms
18.5
21
55
```

Importnál tizedesvessző is elfogadott. Az Excel által hozzáadott UTF-8 BOM
is kezelhető. Hibás fájl megnyitása esetén az előző adatsor megmarad.
A CSV a méréseket tartalmazza. A kijelölés és a határérték nem része a fájlnak.


## Osztályok

`KFMeresiSor` tartja a válaszidők listáját, ellenőrzi az új értékeket,
elvégzi a számításokat, és kezeli a CSV-fájlokat. Nem függ a grafikus
felülettől, így külön is kipróbálható.

`KFNaploApp` felépíti az ablakot, és a gombok, a billentyűzet, a táblázat
és a grafikon eseményeire reagál. A számításokat a `KFMeresiSor` objektumra
bízza. Minden saját függvény és osztály nevében szerepel a KF monogram;
a Python által előírt konstruktor neve `__init__`.

## Eseménykezelés

- A gombok `command` paramétere meghívja a hozzájuk tartozó metódust.
- `<Return>`: mérés hozzáadása vagy a határérték alkalmazása.
- `<<TreeviewSelect>>`: a kijelölt mérés kiemelése a grafikonon.
- `<Button-1>`: grafikonpont kiválasztása.
- `<Configure>`: a grafikon újrarajzolása ablakméret-változáskor.
- `WM_DELETE_WINDOW`: mentési kérdés kilépés előtt.

## Projektfájlok

| Fájl | Tartalom |
| --- | --- |
| `main.py` | Grafikus felület és eseménykezelők |
| `KF_meresek.py` | Adatok, számítások és CSV-kezelés |
| `KF_kornyezet.py` | Virtuális környezet létrehozása |
| `pelda_meresek.csv` | A kipróbáláshoz használható mintaadatok |
| `.gitignore` | A helyi környezet és az átmeneti fájlok kizárása |

A `.venv` és a `__pycache__` helyi fájlok, nem részei a tárolónak.
