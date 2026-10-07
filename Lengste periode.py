import csv
from datetime import datetime 

def tekst_til_tall(tekst):
    if tekst == "-" or tekst == "":
        return None
    tekst = tekst.replace(",",".")
    return float(tekst)

def lengste_periode(data):
    naavaerende = 0
    lengste = 0
    start = None
    lengste_start = None
    lengste_slutt = None
    
    for dag in data:
        dato = dag[0]
        nedbor = dag[1]
        
        if nedbor == 0:
            if naavaerende == 0:
                start = dato   
                
            naavaerende +=1
            
            if naavaerende > lengste:
                lengste = naavaerende
                lengste_start = start
                lengste_slutt = dato
        else:
            naavaerende = 0
            
    return lengste, lengste_start, lengste_slutt
    

#innlesing og kjøring
data = []

with open("sinnes_2014_2025_med_makstemperatur.csv", encoding="utf-8-sig") as fil:
    leser = csv.reader(fil,delimiter=";")
    next(leser)
    for linje in leser:
        if linje[2] == "":
            continue
        dato = datetime.strptime(linje[2],"%d.%m.%Y")
        nedbor = tekst_til_tall(linje[5])
        data.append((dato, nedbor))
        
lengste, start, slutt = lengste_periode(data)

print("Lengste periode uten nedbør mellom 2014 og 2025 var:", lengste, "dager")
print("perioden var fra", start.strftime("%d.%m.%Y"),"til", slutt.strftime("%d.%m.%Y"))

