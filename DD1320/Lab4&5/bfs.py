from bintreeFile import Bintree
from linkedQFile import LinkedQ

class ParentNode:
    def __init__(self, word, parent = None):
        self.word = word
        self.parent: ParentNode = parent
    def __str__(self):
        return self.word
    def writechain(self):
        if self.parent == None:
            return self.word
        else:
            return self.parent.writechain() + " -> " + self.word

class SolutionFound(Exception):
    pass

def makechildren(parent: ParentNode, alla_ord: Bintree, dumma_barn: Bintree, queue: LinkedQ):
    for i in range(len(parent.word)):
        for letter in "abcdefghijklmnopqrstuvwxyzåäö":
            child = parent.word[:i] + letter + parent.word[i+1:]
            if child in alla_ord and child not in dumma_barn:
                dumma_barn.put(child)
                queue.enqueue(ParentNode(child, parent))
            
def main():
    svenska = Bintree()
    with open("word3.txt", "r", encoding = "utf-8") as svenskfil:
        for rad in svenskfil:
            ordet = rad.strip()
            svenska.put(ordet)

    gamla = Bintree()
    q = LinkedQ()
    start_ord, slut_ord = input("startord slutord: ").split(" ")
    q.enqueue(ParentNode(start_ord))
    gamla.put(start_ord)
    
    while not q.isEmpty():
        nod: ParentNode = q.dequeue()
        if nod.word == slut_ord:
            print("Det finns en väg till", slut_ord)
            print(nod.writechain())
            raise SolutionFound()
        makechildren(nod, svenska, gamla, q)
    print(f"det är ej möjligt att gå från {start_ord} till {slut_ord}")
    
if __name__ == "__main__":
    main()