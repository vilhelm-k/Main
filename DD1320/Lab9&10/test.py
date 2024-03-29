from molParser import checkSyntax, readformel, weight, ATOMS
import unittest


class TestMolParser(unittest.TestCase):
    def test_correct(self):
        self.assertEqual(checkSyntax("Na"), "Formeln är syntaktiskt korrekt")
        self.assertEqual(checkSyntax("H2O"), "Formeln är syntaktiskt korrekt")
        self.assertEqual(checkSyntax("Na332"), "Formeln är syntaktiskt korrekt")
        self.assertEqual(checkSyntax("Si(C3(COOH)2)4(H2O)7"), "Formeln är syntaktiskt korrekt")

    def test_incorrect(self):
        self.assertEqual(checkSyntax("C(Xx4)5"), "Okänd atom vid radslutet 4)5")
        self.assertEqual(checkSyntax("C(OH4)C"), "Saknad siffra vid radslutet C")
        self.assertEqual(checkSyntax("C(OH4C"), "Saknad högerparentes vid radslutet")
        self.assertEqual(checkSyntax("H2O)Fe"), "Felaktig gruppstart vid radslutet )Fe")
        self.assertEqual(checkSyntax("H0"), "För litet tal vid radslutet")
        self.assertEqual(checkSyntax("H1C"), "För litet tal vid radslutet C")
        self.assertEqual(checkSyntax("H02C"), "För litet tal vid radslutet 2C")
        self.assertEqual(checkSyntax("Nacl"), "Saknad stor bokstav vid radslutet cl")
        self.assertEqual(checkSyntax("a"), "Saknad stor bokstav vid radslutet a")
        self.assertEqual(checkSyntax("(Cl)2)3"), "Felaktig gruppstart vid radslutet )3")
        self.assertEqual(checkSyntax(")"), "Felaktig gruppstart vid radslutet )")
        self.assertEqual(checkSyntax("2"), "Felaktig gruppstart vid radslutet 2")

    def test_weights(self):
        self.assertEqual(weight(readformel("Na")), ATOMS["Na"])
        self.assertEqual(weight(readformel("H2O")), ATOMS["H"] * 2 + ATOMS["O"])
        self.assertEqual(weight(readformel("Na332")), ATOMS["Na"] * 332)
        self.assertEqual(
            weight(readformel("Si(C3(COOH)2)4(H2O)7")),
            ATOMS["Si"]
            + (ATOMS["C"] * 3 + (ATOMS["C"] + ATOMS["O"] * 2 + ATOMS["H"]) * 2) * 4
            + (ATOMS["H"] * 2 + ATOMS["O"]) * 7,
        )


if __name__ == "__main__":
    unittest.main()
