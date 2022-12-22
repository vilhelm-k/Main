# Vilhelm Karlin och Ismael Parada

import re

class Europa:
    def __init__(self, name, area, pop):
        self.name = name
        self.pop = float(pop)
        self.area = float(area)
        self.density = self.calcDensity()
    
    def calcDensity(self):
        return self.pop/self.area
        
    def __str__(self):
        return (f"{self.name}  {self.pop}  {self.area}  {round(self.density, 1)}")

def __main__():
    with open(input('Ange filnamn: '), 'r') as file:
        lines = file.readlines()
    
    countries = [Europa(*re.split('[\s]*,[\s]*', line.strip())) for line in lines]
    
    for country in countries:
        print(country)

__main__()