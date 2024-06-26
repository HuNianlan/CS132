import unittest
import sqlite3
import sys
import os
sys.path.append("src")
from DB import AccountState, Account,check_account_exist,create_table,create_account,close_account,check_password,update_balance,check_is_valid,get_recent_transactions,change_password,check_enough_balance,reset,query,print_all_accounts



class TestDB(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect('user_database.db')
        cls.cursor = cls.conn.cursor()
        cls.create_table()
    
    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    @classmethod
    def create_table(cls):
        cls.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY,
                account_id TEXT NOT NULL,
                password TEXT NOT NULL,
                balance REAL,
                state INTEGER,
                creation_time TEXT
            )
        ''')
        cls.cursor.execute('''
            CREATE TABLE IF NOT EXISTS account_history (
                id INTEGER PRIMARY KEY,
                account_id TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                amount REAL,
                date INTEGER  
            )
        ''')
        cls.conn.commit()

    def setUp(self):
        reset()

    def test_create_account(self):
        account = Account('2023123457', '123456', 1000)
        create_account(account.account_id, account.password, account.balance)
        self.assertTrue(check_account_exist('2023123457'))

    def test_close_account(self):
        account = Account('2023123456', '111111', 500)
        close_account(account.account_id)
        self.cursor.execute('SELECT state FROM accounts WHERE account_id = ?', (account.account_id,))
        state = self.cursor.fetchone()[0]
        self.assertEqual(state, AccountState.Deleted)

    def test_check_password(self):
        account = Account('2023123456', '111111', 500)
        self.assertTrue(check_password(account.account_id, account.password))
        self.assertFalse(check_password(account.account_id, 'wrong_password'))

    def test_update_balance(self):
        account = Account('2023123456', '111111', 500)
        update_balance(account.account_id, 200)
        self.cursor.execute('SELECT balance FROM accounts WHERE account_id = ?', (account.account_id,))
        balance = self.cursor.fetchone()[0]
        self.assertEqual(balance, 700)

    def test_check_is_valid(self):
        account = Account('2023123456', '111111', 500)
        self.assertTrue(check_is_valid(account.account_id))
        close_account(account.account_id)
        self.assertFalse(check_is_valid(account.account_id))

    # def test_get_recent_transactions(self):
    #     account = Account('2023123456', '111111', 500)
    #     create_account(account.account_id, account.password, account.balance)
    #     account.add_to_history('withdrawal', 100)
    #     account.add_to_history('deposit', 200)
    #     transactions = get_recent_transactions(account.account_id)
    #     self.assertEqual(len(transactions), 2)

    def test_change_password(self):
        account = Account('2023123456', '111111', 500)
        change_password(account.account_id, '123456')
        self.assertTrue(check_password(account.account_id, '123456'))
        self.assertFalse(check_password(account.account_id, '111111'))

    def test_check_enough_balance(self):
        account = Account('2023123456', '111111', 500)
        self.assertTrue(check_enough_balance(account.account_id, 200))
        self.assertFalse(check_enough_balance(account.account_id, 600))

    def test_query(self):
        account = Account('2023123456', '111111', 500)
        result = query(account.account_id)
        self.assertEqual(result['account_id'], account.account_id)
        self.assertEqual(result['balance'], account.balance)

if __name__ == '__main__':
    unittest.main()
