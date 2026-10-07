import csv
from datetime import datetime
import matplotlib.pyplot as plt

FILA = "programmering_gruppeoppgave/sinnes_2014_2025_med_makstemperatur.csv"  # ligg fila i samme mappe som scriptet
MIN_TEMP = 5  # minimumstemperatur for plantevekst


# ------------------- felles innlesing (gjøres én gang) -------------------

def tekst_til_tall(tekst):
    """Gjør '1,4' om til 1.4. Manglende verdi ('-' eller tom) gir None."""
    if tekst == "-" or tekst == "":
        return None
    return float(tekst.replace(",", "."))


def les_data(filnavn):
    """Leser hele fila og returnerer en liste med én dict per dag, sortert på dato."""
    data = []
    with open(filnavn, "r", encoding="utf-8-sig") as fil:
        leser = csv.reader(fil, delimiter=";")
        next(leser)  # hopper over header
        for rad in leser:
            try:
                dato = datetime.strptime(rad[2], "%d.%m.%Y")
            except (ValueError, IndexError):
                continue  # bunntekst eller feilformatert rad
            data.append({
                "dato": dato,
                "maks_temp": tekst_til_tall(rad[3]),
                "middel_temp": tekst_til_tall(rad[4]),
                "nedbor": tekst_til_tall(rad[5]),
                "vind": tekst_til_tall(rad[6]),
                "snodybde": tekst_til_tall(rad[7]),
            })
    data.sort(key=lambda dag: dag["dato"])
    return data


# ------------------- d) plotting -------------------

def plott_verdier(data, aar):
    dager = [dag for dag in data if dag["dato"].year == aar]
    if not dager:
        print(f"Fant ingen data for {aar}.")
        return

    datoer = [dag["dato"] for dag in dager]
    felt = [("snodybde", "Snødybde\n(cm)"),
            ("nedbor", "Nedbør\n(mm)"),
            ("middel_temp", "Middeltemperatur\n(°C)"),
            ("vind", "Høyeste middelvind\n(m/s)")]

    fig, axs = plt.subplots(len(felt), 1)
    for ax, (nokkel, tittel) in zip(axs, felt):
        verdier = [dag[nokkel] if dag[nokkel] is not None else float("nan") for dag in dager]
        ax.plot(datoer, verdier)
        ax.set_ylabel(tittel, fontsize=7)
    fig.autofmt_xdate()
    plt.tight_layout()
    plt.show()


# ------------------- e) skiføre -------------------

def skifore(data, aar):
    antall = 0
    for dag in data:
        dato = dag["dato"]
        i_sesong = (dato.year == aar - 1 and dato.month >= 11) or (dato.year == aar and dato.month <= 5)
        if i_sesong and dag["snodybde"] is not None and dag["snodybde"] >= 20:
            antall += 1
    print(f"Det var {antall} dager med skiføre i sesongen {aar}.")


# ------------------- f) forenklet plantevekst -------------------

def plantevekst(data, aar):
    temperaturer = [dag["middel_temp"] for dag in data
                    if dag["dato"].year == aar and dag["middel_temp"] is not None]
    if not temperaturer:
        print(f"Fant ingen temperaturdata for {aar}.")
        return
    total = sum(temp - MIN_TEMP for temp in temperaturer if temp >= MIN_TEMP)
    print(f"Total plantevekst i {aar}: {total:.1f} (basert på {len(temperaturer)} dager med data)")


# ------------------- g) lengste periode uten nedbør -------------------

def lengste_periode(data):
    naavaerende = 0
    lengste = 0
    start = None
    lengste_start = None
    lengste_slutt = None

    for dag in data:
        if dag["nedbor"] == 0:
            if naavaerende == 0:
                start = dag["dato"]
            naavaerende += 1
            if naavaerende > lengste:
                lengste = naavaerende
                lengste_start = start
                lengste_slutt = dag["dato"]
        else:
            naavaerende = 0

    print(f"Lengste periode uten nedbør var {lengste} dager,")
    print(f"fra {lengste_start.strftime('%d.%m.%Y')} til {lengste_slutt.strftime('%d.%m.%Y')}.")


# ------------------- h) sommerdager osv. -------------------

def antall_varme_dager(data, aar):
    sommerdag = 0
    hoysommerdag = 0
    tropedag = 0

    for dag in data:
        maks = dag["maks_temp"]
        if dag["dato"].year != aar or maks is None:
            continue
        if maks > 30:
            tropedag += 1
        elif maks > 25:
            hoysommerdag += 1
        elif maks > 20:
            sommerdag += 1

    print(f"Resultat for {aar}.")
    print("Sommerdager:", sommerdag)
    print("Høysommerdager:", hoysommerdag)
    print("Tropedager:", tropedag)


# ------------------- oppslagsverk og meny -------------------
# nøkkel -> (funksjon, trenger_aar)

OPPGAVER = {
    "plotting": (plott_verdier, True),
    "skiføre": (skifore, True),
    "forenklet plantevekst": (plantevekst, True),
    "lengste periode": (lengste_periode, False),
    "sommerdager": (antall_varme_dager, True),
}


def les_aar():
    try:
        aar = int(input("Skriv inn et årstall mellom 2014 og 2025: "))
    except ValueError:
        print("Dette er ikke et årstall.")
        return None
    if aar < 2014 or aar > 2025:
        print("Dette årstallet er ikke gyldig.")
        return None
    return aar


def main():
    try:
        data = les_data(FILA)
    except FileNotFoundError:
        print("Fant ikke fila!")
        return

    print("Tilgjengelige oppgaver:", ", ".join(OPPGAVER))
    valg = input("Hva vil du gjøre? ").strip().lower()

    if valg not in OPPGAVER:
        print("Ukjent valg!")
        return

    funksjon, trenger_aar = OPPGAVER[valg]
    if trenger_aar:
        aar = les_aar()
        if aar is None:
            return
        funksjon(data, aar)
    else:
        funksjon(data)


if __name__ == "__main__":
    main()