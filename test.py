import unittest
from unittest.mock import patch
import questionnaire
import questionnaire_import
import os
import json


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


class TestQuestionnaire(unittest.TestCase):
    def test_questionnaire_lancer_animaux_chien_debutant(self):
        filename = os.path.join("test_data", "animaux_leschiens_debutant.json")
        q = questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNotNone(q)

    # nb de questions
        self.assertEqual(len(q.questions), 10)
    # titre, categorie, difficulte
        self.assertEqual(q.titre, "Les Chiens")
        self.assertEqual(q.categorie, "Animaux")
        self.assertEqual(q.difficulte, "débutant")
    # patcher le input -> forcer de répondre toujours à 1 et résultat toujours 4
        with patch("builtins.input", return_value="1"):
            self.assertEqual(q.lancer(), 2)

    def test_questionnaire_format_invalide(self):
        filename = os.path.join("test_data", "format_invalide1.json")
        q = questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNotNone(q)
        self.assertEqual(q.categorie, "inconnue")
        self.assertEqual(q.difficulte, "inconnue")
        self.assertIsNotNone(q.questions)

        filename = os.path.join("test_data", "format_invalide2.json")
        q = questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNone(q)

        filename = os.path.join("test_data", "format_invalide3.json")
        q = questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNone(q)


class TestImportQuestionnaire(unittest.TestCase):
    def test_import_questionnaire(self):
        questionnaire_import.generate_json_file("Animaux", "Les chats", "https://www.kiwime.com/oqdb/files/1050634995/OpenQuizzDB_050/openquizzdb_50.json")
        
        filenames = ("animaux_leschats_confirme.json", "animaux_leschats_debutant.json", "animaux_leschats_expert.json")

        for filename in filenames:
            self.assertTrue(os.path.isfile(filename))
            file = open(filename, "r")
            json_data = file.read()
            file.close()
            try:
                data = json.loads(json_data)
            except:
                self.fail("Problème de désserialisation pour le fichier : " + filename)
            
            self.assertIsNotNone(data.get("titre"))
            self.assertIsNotNone(data.get("questions"))
            self.assertIsNotNone(data.get("categorie"))
            self.assertIsNotNone(data.get("difficulte"))

            for question in data.get("questions"):
                self.assertIsNotNone(question.get("titre"))
                self.assertIsNotNone(question.get("choix"))

                for choix in question.get("choix"):
                    self.assertGreater(len(choix[0]), 0)
                    self.assertTrue(isinstance(choix[1], bool))
                bonne_reponse = [i[0] for i in question.get("choix") if i[1]]
                self.assertEqual(len(bonne_reponse), 1)
       
unittest.main()