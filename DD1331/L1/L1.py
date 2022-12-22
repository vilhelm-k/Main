# Vilhelm Karlin och Ismael Parada

# ----------------------------------------------------------------------------------------------
# UPPGIFT 1
def growth (amount, time):
   return amount * 1.05 ** time

print('Se hur mycket pengar du kommer ha efter x antal år med 5 procent i ränta')
pengar = float(input('Hur mycket pengar sparar du? '))
tid = float(input('Hur länge sparar du? '))

print("Du har:", growth(pengar, tid),"om", tid, "år")

# ----------------------------------------------------------------------------------------------
# UPPGIFT 2
from cmath import pi

def massSatelite (distance, period): 
    #distance in km, period in days
    seconds = period * 86400
    return 4 * (pi ** 2) * ((1000 * distance) ** 3) / (6.67 * (10 ** (-11)) * (seconds ** 2)) 
    
   
avstånd =  float(input('hur långt är sateliten från jorden i km? ')) 
omloppstid =  float(input('hur långt omloppstid har sateliten i dagar? ')) 

print("Jorden väger:", massSatelite(avstånd, omloppstid), "kg")
# ----------------------------------------------------------------------------------------------