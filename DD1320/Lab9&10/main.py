from molParser import checkSyntax
import sys


def main():
    output = ""
    while True:
        molekyl = sys.stdin.readline().rstrip()
        if molekyl == "#":
            break
        resultat = checkSyntax(str(molekyl))
        output += resultat + "\n"
    output.rstrip()
    print(output)


if __name__ == "__main__":
    main()
