# Antall pr. år: Tell antall sommerdager, høysommerdager og tropedager i det aktuelle året
# og skriv ut dette. En sommerdag er en dag med maksimaltemperatur over 20 grader. En
# høysommerdag har maksimaltemperatur over 25 grader og en tropedag har
# maksimaltemperatur over 30 grader.


# ------------------- sette verdier og tellere
import csv
import matplotlib.pyplot as plt
from datetime import datetime

sommerdag = 0
høysommerdag = 0
tropedag = 0


# ------------------- skrive inn årstall
år = input("Skriv inn et årstall mellom 2014-2025: ")

try:
    år = int(år)

    if år < 2014 or år > 2025:
        print("Dette årstallet er ikke gyldig.")
        exit()
except ValueError:
    print("Dette er ikke et årstall.")
    exit()


# ------------------- åpne fil 
with open(r"C:\Users\aliza\Downloads\sinnes_2014_2025_med_makstemperatur\sinnes_2014_2025_med_makstemperatur.csv", \
"r", encoding="UTF-8") as fil:

    leser = csv.reader(fil, delimiter=";")
    next(leser)

    for rad in leser:
        if len(rad[2].split(".")) == 3:
            if år == int(rad[2].split(".")[2]):


# ------------------- hente maksimaltemperaturen
                if rad[3] != "-":
                    maksimaltemperatur = float(rad[3].replace(",", "."))


# ------------------- teller antall sommerdager, høysommerdager og tropedager i gitt årstall
                if maksimaltemperatur > 30:
                    tropedag = tropedag + 1
                elif maksimaltemperatur > 25:
                    høysommerdag = høysommerdag + 1
                elif maksimaltemperatur > 20:
                    sommerdag = sommerdag + 1


# ------------------- printer resultatet
print(f"Resultat for {år}.")
print("Sommerdager:", sommerdag)
print("Høysommerdager:", høysommerdag)
print("Tropedager:", tropedag)