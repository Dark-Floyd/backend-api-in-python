"""
Sample test
"""

from django.test import SimpleTestCase
from app import calc

class CalcTest(SimpleTestCase):
    "Test the Calc module"
    
    def test_add_numbers(self):
        res = calc.add(5, 6)
        self.assertEqual(res, 11)
        
    def test_sub_numbers(self):
        res = calc.subtract(15, 10)
        self.assertEqual(res, 5)
        
# TDD:
#  1. Write test for behaviour expected to see in code
#  2. Test fails because there's not code yet
#  3. Complete the code
