import unittest
from unittest.mock import patch
import sys
sys.path.append("src")
from processor import Processor
from DB import *

class TestProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = Processor()
        self.processor.current_account = "2023123456"
        reset()
    
    def test_create_account(self):
        self.assertEqual(self.processor.create_account("000"),"failed@create_account")
        self.assertTrue(self.processor.create_account("000000").startswith("account_created@"))
   

    def test_close_account(self):
        self.processor.account_available = True
        # fail
        self.assertEqual(self.processor.close_account(), "failed@close_account")

        #success
        create_account('2022123455',111111,0)
        self.processor.current_account = '2022123455'
        self.assertEqual(self.processor.close_account(),"account_closed@"+ self.processor.current_account)
        
        # reset 
        self.processor.current_account = "2023123456"

    def test_deposit_cash(self,):
        self.processor.account_available = True
        result = self.processor.deposit_cash("1000")
        self.assertEqual(result, "cash_deposited@1000")


    def test_withdraw_cash(self):
        self.processor.account_available = False
        self.assertEqual(self.processor.withdraw_cash("10000", "111211"), "failed@withdraw_cash")
        self.processor.account_available = True
        self.assertEqual(self.processor.withdraw_cash("100", "111111"), "cash_withdrawn@100")

    def test_open_app(self):
        result = self.processor.open_app()
        self.assertEqual(result, "app_opened#1")

    def test_close_app(self):
        self.processor.open_app()
        result = self.processor.close_app("1")
        self.assertEqual(result, "app_closed#1")

    def test_log_in(self):
        self.processor.open_app()
        self.assertEqual(self.processor.log_in("2023123456", "11112", "1"), "failed@log_in#1")
        self.assertEqual(self.processor.log_in("2023123456", "111111", "1"), "logged_in@2023123456#1")

    def test_log_out(self):
        self.processor.open_app()
        self.processor.log_in("2023123456", "111111", "1")

        result = self.processor.log_out("1")
        self.assertEqual(result, "logged_out@2023123456#1")


    def test_transfer_money(self):
        self.processor.account_available = True
        create_account('2022123455',111111,0)
        self.assertTrue(self.processor.transfer_money("0000000", "50000").startswith("failed@transfer_money"))
        self.assertEqual(self.processor.transfer_money("2022123455", "500"), "money_transfered@500")

    def test_change_password(self):
        self.processor.account_available = True
        self.assertEqual(self.processor.change_password("aaaa"), "failed@change_password")
        self.assertEqual(self.processor.change_password("123456"), "password_changed@")


    def test_query(self):
        self.processor.account_available = True
        result = self.processor.query()
        self.assertEqual(result, "query_showed")
        result = self.processor.query()
        self.assertEqual(result, "query_showed")
        
        
    def test_return_card(self):
        self.processor.account_available = True
        self.processor.card_inserted = True
        result = self.processor.return_card()
        # Assert that the returned message is correct
        self.assertEqual(result, "card_returned@2023123456")
        self.assertEqual(self.processor.current_account,None)

    def test_insert_card(self):
        self.processor.return_card()
        self.assertEqual(self.processor.insert_card("1234567890"), "failed@insert_card")
        self.assertEqual(self.processor.insert_card("2023123456"), "card_inserted@2023123456")



if __name__ == '__main__':
    unittest.main()
    reset()
