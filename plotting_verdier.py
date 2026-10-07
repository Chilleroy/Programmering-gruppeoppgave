# Plotting: Dere skal la brukeren skrive inn et årstall og så skal programmet plotte
# snødybde, nedbør, middeltemperatur og høyeste middelvind hver dag for dette året.
# Hint: Konverter datoene fra strenger til datetime objekter for å få en finere visning av
# datoene


import csv
import matplotlib.pyplot as plt
from datetime import datetime

datoer = []
snødybde = []
nedbør = []
middeltemperatur = []
middelvind = []

år = input("Skriv inn et årstall mellom 2014-2025: ")

try:
    år = int(år)

    if år < 2014 or år > 2025:
        print("Dette årstallet er ikke gyldig.")
        exit()

except ValueError:
    print("Dette er ikke et årstall.")
    exit()
    

with open(r"C:\Users\aliza\Downloads\sinnes_2014_2025_med_makstemperatur\sinnes_2014_2025_med_makstemperatur.csv", \
"r", encoding="UTF-8") as fil:

    leser = csv.reader(fil, delimiter=";")
    next(leser)

    for rad in leser:
        if len(rad[2].split(".")) == 3:
            if år == int(rad[2].split(".")[2]):

                datoer.append(datetime.strptime(rad[2], "%d.%m.%Y"))

                if rad[7] == "-":
                    snødybde.append(float("nan"))
                else:
                    snødybde.append(float(rad[7].replace(",", ".")))

                if rad[5] == "-":
                    nedbør.append(float("nan"))
                else:
                    nedbør.append(float(rad[5].replace(",", ".")))
                
                if rad[4] == "-":
                    middeltemperatur.append(float("nan"))
                else:
                    middeltemperatur.append(float(rad[4].replace(",", ".")))


                if rad[6] == "-":
                    middelvind.append(float("nan"))
                else:
                    middelvind.append(float(rad[6].replace(",", ".")))


sortert = sorted(zip(datoer, snødybde, nedbør, middeltemperatur, middelvind))

datoer, snødybde, nedbør, middeltemperatur, middelvind = zip(*sortert)


fig, axs = plt.subplots(4, 1)

axs[0].plot(datoer, snødybde)
axs[0].set_ylabel("Snødybde\n(cm)", fontsize=7)

axs[1].plot(datoer, nedbør)
axs[1].set_ylabel("Nedbør\n(mm)", fontsize=7)

axs[2].plot(datoer, middeltemperatur)
axs[2].set_ylabel("Middeltemperatur\n(°C)", fontsize=7)

axs[3].plot(datoer, middelvind)
axs[3].set_ylabel("Høyeste middelvind\n(m/s)", fontsize=7)

fig.autofmt_xdate()
plt.tight_layout()
plt.show()