# Vilhelm Karlin och Ismael Parada

import re

# Funktion som läser filer och gör dem till ordlistor
def textToList(f):
    with open(f, "r") as file:
        words = re.sub('[^a-ö ]+', ' ', file.read().lower()).split(' ')
    return list(filter(lambda x: x is not '', words))

# Funktion som hittar sällsynta ord
def notIntersection(ourText, referenceWords):
    return list(filter(lambda word: word not in referenceWords, ourText))

# Main
def main():
    inputList = textToList(input('Vilken fil vill du läsa in?'))
    commonWords = textToList('vanligaord.txt')
    
    outputList = notIntersection(inputList, commonWords)
    print(f"Texten innehåller {str(len(inputList))} ord.")
    print(f"Funnit {len(outputList)} ovanliga ord.")
    
    for i in outputList:
        print(i)

main()