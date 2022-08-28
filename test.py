import unittest
from unittest.mock import patch
import questionnaire

def additionner(a,b):
    return a+b

def converstion_nombre():
    num_str = input("Entrer un nombre: ")
    return int(num_str)

class TestUnitaireDemo(unittest.TestCase):
    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")
    
    # Toutes les méthodes doivent commencer par 'test' pour être testm
    def test_additionner1(self):
        print("test_additionner_1")
        self.assertEqual(additionner(5, 10), 15)
        self.assertEqual(additionner(6, 10), 16)

    def test_additionner2(self):
        print("test_additionner_2")
        self.assertEqual(additionner(5, 10), 15)

    def test_conversion_nb_valide(self):
        with patch("builtins.input", return_value="10"):
            self.assertEqual(converstion_nombre(), 10)
        with patch("builtins.input", return_value="100"):
            self.assertEqual(converstion_nombre(), 100)

    def test_conversion_nb_invalide(self):
        with patch("builtins.input", return_value="abcd"):
            self.assertRaises(ValueError, converstion_nombre)


class TestQuestion(unittest.TestCase):
    def test_question_bonne_mauvaise_reponse(self):
        choix = ("choix1", "choix2", "choix3")
        q = questionnaire.Question("titre_question", choix, "choix2")
        with patch("builtins.input", return_value="1"):
            self.assertFalse(q.poser(1, 1))
        with patch("builtins.input", return_value="2"):
            self.assertTrue(q.poser(1, 1))
        with patch("builtins.input", return_value="3"):
            self.assertFalse(q.poser(1, 1))

            
unittest.main()