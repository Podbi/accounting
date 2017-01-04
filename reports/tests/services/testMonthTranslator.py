from django.test import TestCase
from reports.service import MonthTranslator

class MonthTranslatorTests(TestCase):
    def test_translator_translates_january_correctly(self):
        """
        Translator should return "Leden" for first month
        """
        self.assertEquals('Leden', MonthTranslator().translate(1))
    
    def test_translator_translates_december_correctly(self):
        """
        Translator should return "Prosinec" for last month
        """
        self.assertEquals('Prosinec', MonthTranslator().translate(12))
    
    def test_translator_translates_july_correctly(self):
        """
        Translator should return "Červenec" for last month
        """
        self.assertEquals('Červenec', MonthTranslator().translate(7))