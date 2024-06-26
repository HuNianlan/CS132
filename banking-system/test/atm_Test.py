import unittest
import sys
import os
sys.path.append("src")
from atm.atm import ATM  


class TestATM(unittest.TestCase):
    def test_deposit(self):
        atm = ATM(1000)
        
        result = atm.deposit(-100)
        self.assertFalse(result)
        self.assertEqual(atm.check_balance(), 1000)  
             
        result = atm.deposit(500)
        self.assertTrue(result)
        self.assertEqual(atm.check_balance(), 1500)

    def test_withdraw(self):
        atm = ATM(1000)
        
        result = atm.withdraw(1200)
        self.assertFalse(result)
        self.assertEqual(atm.check_balance(), 1000)
        
        result = atm.withdraw(200)
        self.assertTrue(result)
        self.assertEqual(atm.check_balance(), 800)

 

    def test_check_balance(self):
        atm = ATM(1000)
        self.assertEqual(atm.check_balance(), 1000)
        atm.deposit(500)
        self.assertEqual(atm.check_balance(), 1500)
        atm.withdraw(200)
        self.assertEqual(atm.check_balance(), 1300)


if __name__ == "__main__":
    unittest.main()
