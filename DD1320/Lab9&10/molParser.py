from linkedQFile import LinkedQ

# <formel>  ::= <mol> \n
# <mol>     ::= <group> | <group><mol>
# <group>   ::= <atom> |<atom><num> | (<mol>)<num>
# <atom>    ::= <LETTER> | <LETTER><letter>
# <LETTER>  ::= A | B | C | ... | Z
# <letter>  ::= a | b | c | ... | z
# <num>     ::= 2 | 3 | 4 | ...

ATOMS = {
    "H",
    "He",
    "Li",
    "Be",
    "B",
    "C",
    "N",
    "O",
    "F",
    "Ne",
    "Na",
    "Mg",
    "Al",
    "Si",
    "P",
    "S",
    "Cl",
    "Ar",
    "K",
    "Ca",
    "Sc",
    "Ti",
    "V",
    "Cr",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "Ga",
    "Ge",
    "As",
    "Se",
    "Br",
    "Kr",
    "Rb",
    "Sr",
    "Y",
    "Zr",
    "Nb",
    "Mo",
    "Tc",
    "Ru",
    "Rh",
    "Pd",
    "Ag",
    "Cd",
    "In",
    "Sn",
    "Sb",
    "Te",
    "I",
    "Xe",
    "Cs",
    "Ba",
    "La",
    "Ce",
    "Pr",
    "Nd",
    "Pm",
    "Sm",
    "Eu",
    "Gd",
    "Tb",
    "Dy",
    "Ho",
    "Er",
    "Tm",
    "Yb",
    "Lu",
    "Hf",
    "Ta",
    "W",
    "Re",
    "Os",
    "Ir",
    "Pt",
    "Au",
    "Hg",
    "Tl",
    "Pb",
    "Bi",
    "Po",
    "At",
    "Rn",
    "Fr",
    "Ra",
    "Ac",
    "Th",
    "Pa",
    "U",
    "Np",
    "Pu",
    "Am",
    "Cm",
    "Bk",
    "Cf",
    "Es",
    "Fm",
    "Md",
    "No",
    "Lr",
    "Rf",
    "Db",
    "Sg",
    "Bh",
    "Hs",
    "Mt",
    "Ds",
    "Rg",
    "Cn",
    "Fl",
    "Lv",
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
