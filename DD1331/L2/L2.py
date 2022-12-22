# Vilhelm Karlin och Ismael Parada

import statistics

# Funktion som lägger till värden i scores
def inmatning():
    print("\nMata in de tävlandes resultat")
    participants = range(int(input("Hur många tävlande: ")))

    return list(map(lambda x: float(input(f'Ange värde för deltagare {x + 1}: ')), participants))


# Prints the stats from input values
def statistik(list):
        if not list:
            print('Du måste först ange data')
            return []

        list.sort()
        mean = statistics.mean(list)
        stdev = statistics.stdev(list) if len(list) > 1 else 'N/A'
        print(f"Medelvärdet är {str(mean)}m med en standardavvikelse på {str(stdev)}m. Det högsta värde är {str(list[-1])}m och det lägsta är {str(list[0])}m.")

# Main function
def main():
    scores = []
    while True:
        menus = ["Mata in de tävlandes resultat", "Se statistik för tidigare inmatade värden", "Avsluta"]
        
        print("\nMeny")
        for i in range(len(menus)):
            print(i + 1, menus[i])

        select = input("\nDitt val: ")

        if select == '1':
            scores = inmatning()
        if select == '2':
            statistik(scores)
        if select == '3':
            break
main()