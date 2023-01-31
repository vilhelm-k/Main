from bintreeFile import Bintree
svenska = Bintree()
with open("word3.txt", "r", encoding = "utf-8") as svenskfil:
    for rad in svenskfil:
        ordet = rad.strip()                # Ett trebokstavsord per rad
        if ordet in svenska:
            print(ordet, end = " ") 
        else:
            svenska.put(ordet)             # in i sökträdet
print("\n")
engelska = Bintree()
with open("engelska.txt", "r", encoding = "utf-8") as engelskfil:
    for line in engelskfil:
        ord = line.strip().split(" ")
        for ordet in ord:
            if ordet in engelska:
                continue
            engelska.put(ordet)             # in i sökträdet
            if ordet in svenska:
                print(ordet, end = " ")