from linkedQFile import LinkedQ

# <formel>  ::= <mol> \n
# <mol>     ::= <group> | <group><mol>
# <group>   ::= <atom> |<atom><num> | (<mol>)<num>
# <atom>    ::= <LETTER> | <LETTER><letter>
# <LETTER>  ::= A | B | C | ... | Z
# <letter>  ::= a | b | c | ... | z
# <num>     ::= 2 | 3 | 4 | ...

ATOMS = {
    "H": 1.00794,
    "He": 4.002602,
    "Li": 6.941,
    "Be": 9.012182,
    "B": 10.811,
    "C": 12.0107,
    "N": 14.0067,
    "O": 15.9994,
    "F": 18.9984032,
    "Ne": 20.1797,
    "Na": 22.98976928,
    "Mg": 24.3050,
    "Al": 26.9815386,
    "Si": 28.0855,
    "P": 30.973762,
    "S": 32.065,
    "Cl": 35.453,
    "K": 39.0983,
    "Ar": 39.948,
    "Ca": 40.078,
    "Sc": 44.955912,
    "Ti": 47.867,
    "V": 50.9415,
    "Cr": 51.9961,
    "Mn": 54.938045,
    "Fe": 55.845,
    "Ni": 58.6934,
    "Co": 58.933195,
    "Cu": 63.546,
    "Zn": 65.38,
    "Ga": 69.723,
    "Ge": 72.64,
    "As": 74.92160,
    "Se": 78.96,
    "Br": 79.904,
    "Kr": 83.798,
    "Rb": 85.4678,
    "Sr": 87.62,
    "Y": 88.90585,
    "Zr": 91.224,
    "Nb": 92.90638,
    "Mo": 95.96,
    "Tc": 98,
    "Ru": 101.07,
    "Rh": 102.90550,
    "Pd": 106.42,
    "Ag": 107.8682,
    "Cd": 112.411,
    "In": 114.818,
    "Sn": 118.710,
    "Sb": 121.760,
    "I": 126.90447,
    "Te": 127.60,
    "Xe": 131.293,
    "Cs": 132.9054519,
    "Ba": 137.327,
    "La": 138.90547,
    "Ce": 140.116,
    "Pr": 140.90765,
    "Nd": 144.242,
    "Pm": 145,
    "Sm": 150.36,
    "Eu": 151.964,
    "Gd": 157.25,
    "Tb": 158.92535,
    "Dy": 162.500,
    "Ho": 164.93032,
    "Er": 167.259,
    "Tm": 168.93421,
    "Yb": 173.054,
    "Lu": 174.9668,
    "Hf": 178.49,
    "Ta": 180.94788,
    "W": 183.84,
    "Re": 186.207,
    "Os": 190.23,
    "Ir": 192.217,
    "Pt": 195.084,
    "Au": 196.966569,
    "Hg": 200.59,
    "Tl": 204.3833,
    "Pb": 207.2,
    "Bi": 208.98040,
    "Po": 209,
    "At": 210,
    "Rn": 222,
    "Fr": 223,
    "Ra": 226,
    "Ac": 227,
    "Pa": 231.03588,
    "Th": 232.03806,
    "Np": 237,
    "U": 238.02891,
    "Am": 243,
    "Pu": 244,
    "Cm": 247,
    "Bk": 247,
    "Cf": 251,
    "Es": 252,
    "Fm": 257,
    "Md": 258,
    "No": 259,
    "Lr": 262,
    "Rf": 265,
    "Db": 268,
    "Hs": 270,
    "Sg": 271,
    "Bh": 272,
    "Mt": 276,
    "Rg": 280,
    "Ds": 281,
    "Cn": 285,
}
UPPER_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER_LETTERS = "abcdefghijklmnopqrstuvwxyz"
NUMBERS = "0123456789"


class Ruta:
    def __init__(self, atom="( )", num=1):
        self.atom = atom
        self.num = num
        self.next: Ruta = None
        self.down: Ruta | None = None

    def __repr__(self):
        return f"Ruta(atom={self.atom}, num={self.num})"

    def show(self, depth=0):
        print(" " * depth, self)
        if self.down is not None:
            self.down.show(depth + 1)
        if self.next is not None:
            self.next.show(depth)


def throw_syntax_error(error, radslut):
    raise SyntaxError(f"{error} vid radslutet {radslut}")


def readformel(formula: str):
    q = LinkedQ()
    for char in formula:
        q.enqueue(char)
    return readmol(q)


def readmol(q: LinkedQ, in_brackets=False) -> Ruta:
    root = readgroup(q)
    if q.peek() is not None and not (q.peek() == ")" and in_brackets):
        root.next = readmol(q, in_brackets)
    return root


def readgroup(q: LinkedQ) -> Ruta:
    if q.peek() == "(":
        q.dequeue()
        root = Ruta()
        root.down = readmol(q, True)
        if q.dequeue() != ")":
            throw_syntax_error("Saknad högerparentes", q)
        root.num = readnum(q)
    elif q.peek() in UPPER_LETTERS:
        root = Ruta(readatom(q))
        if q.peek() is not None and q.peek() in NUMBERS:
            root.num = readnum(q)
    elif q.peek() in LOWER_LETTERS:
        throw_syntax_error("Saknad stor bokstav", q)
    else:
        throw_syntax_error("Felaktig gruppstart", q)
    return root


def readatom(q: LinkedQ) -> int:
    atom = q.dequeue()
    if q.peek() is not None and q.peek() in LOWER_LETTERS:
        atom += q.dequeue()
    if atom is None or atom not in ATOMS:
        throw_syntax_error("Okänd atom", q)
    return atom


def readnum(q: LinkedQ) -> int:
    if q.peek() == "0":
        q.dequeue()
        throw_syntax_error("För litet tal", q)  # helt idiotiskt att uppgiften hanterar 0 speciellt
    num = ""
    while q.peek() is not None and q.peek() in NUMBERS:
        num += q.dequeue()
    if not num:
        throw_syntax_error("Saknad siffra", q)

    output = int(num)
    if output < 2:  # kan lägga till or num[0] == "0" här men i guess not (:
        throw_syntax_error("För litet tal", q)
    return output


def checkSyntax(molekyl):
    try:
        readformel(molekyl)
        return "Formeln är syntaktiskt korrekt"
    except SyntaxError as e:
        return str(e).rstrip()


def weight(mol: Ruta, multiplier=1) -> float:
    if mol is None:
        return 0
    own_weight = ATOMS[mol.atom] * mol.num * multiplier if mol.atom != "( )" else 0
    return own_weight + weight(mol.down, mol.num * multiplier) + weight(mol.next, multiplier)
