import csv
import statistics


def KF_szamma(szoveg):
    try:
        ertek = float(str(szoveg).strip().replace(",", "."))
    except (TypeError, ValueError):
        raise ValueError("Számot adj meg, például: 24,5.") from None
    if not 0 <= ertek <= 60000:
        raise ValueError("0 és 60000 ms közötti értéket adj meg.")
    return ertek


class KFMeresiSor:
    def __init__(self):
        self.ertekek = []

    def KF_hozzaad(self, szoveg):
        if len(self.ertekek) >= 500:
            raise ValueError("Egy adatsor legfeljebb 500 mérést tartalmazhat.")
        self.ertekek.append(KF_szamma(szoveg))

    def KF_torol(self, index):
        del self.ertekek[index]

    def KF_statisztika(self, hatar):
        if not self.ertekek:
            return None
        return {
            "darab": len(self.ertekek),
            "atlag": statistics.mean(self.ertekek),
            "median": statistics.median(self.ertekek),
            "szoras": statistics.pstdev(self.ertekek),
            "minimum": min(self.ertekek),
            "maximum": max(self.ertekek),
            "hatar_felett": sum(x > hatar for x in self.ertekek),
        }

    def KF_betolt(self, fajlnev):
        uj = KFMeresiSor()
        with open(fajlnev, newline="", encoding="utf-8-sig") as fajl:
            olvaso = csv.reader(fajl, delimiter=";", strict=True)
            if next(olvaso, None) != ["kesleltetes_ms"]:
                raise ValueError("A CSV első sora ez legyen: kesleltetes_ms")
            for sorszam, sor in enumerate(olvaso, start=2):
                if len(sor) != 1:
                    raise ValueError(f"Hibás CSV-sor: {sorszam}.")
                try:
                    uj.KF_hozzaad(sor[0])
                except ValueError as hiba:
                    raise ValueError(f"{sorszam}. sor: {hiba}") from None
        if not uj.ertekek:
            raise ValueError("A CSV nem tartalmaz mérést.")
        self.ertekek = uj.ertekek

    def KF_ment(self, fajlnev):
        with open(fajlnev, "w", newline="", encoding="utf-8") as fajl:
            iro = csv.writer(fajl, delimiter=";")
            iro.writerow(["kesleltetes_ms"])
            for ertek in self.ertekek:
                iro.writerow([ertek])
