import sqlite3
from enum import IntEnum
from datetime import datetime, timedelta

class AccountState(IntEnum):
    #only for reference, it may be complex in other testcase.
    Valid = 1
    Frozen = 2
    Deleted = 3

class Account:
    def __init__(self, account_id, password, balance=0):
        self.account_id = account_id
        self.password = password
        self.balance = balance
        self.history = []
        self.state = AccountState.Valid
    
    def add_to_history(self, transaction_type, amount):
        timestamp = datetime.now()  # 获取当前时间戳
        self.history.append((timestamp, transaction_type, amount))  

conn = sqlite3.connect('user_database.db')
cursor = conn.cursor()

def check_account_exist(account_id):
    cursor.execute('''
        SELECT COUNT(*) FROM accounts
        WHERE account_id = ?
    ''', (account_id,))
    count = cursor.fetchone()[0]
    return count > 0



def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            account_id TEXT NOT NULL,
            password TEXT NOT NULL,
            balance REAL,
            state INTEGER,
            creation_time TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS account_history (
            id INTEGER PRIMARY KEY,
            account_id TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            amount REAL,
            date INTEGER  
        )
    ''')
    conn.commit()

def create_account(account_id, password, balance=0):
    creation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO accounts (account_id, password, balance, state, creation_time)
        VALUES (?, ?, ?, ?, ?)
    ''', (account_id, password, balance, AccountState.Valid, creation_time))
    conn.commit()


def close_account(account_id):
    cursor.execute('''
        UPDATE accounts
        SET state = ?
        WHERE account_id = ?
    ''', (AccountState.Deleted, account_id))
    conn.commit()


def check_password(account_id, password):
    cursor.execute('''
        SELECT * FROM accounts
        WHERE account_id = ? AND password = ?
    ''', (account_id, password))
    return cursor.fetchone() is not None

def update_balance(account_id, value):
    cursor.execute('''
        UPDATE accounts
        SET balance = balance + ?
        WHERE account_id = ?
    ''', (value, account_id))
    conn.commit()

def check_is_valid(account_id):
    cursor.execute('''
        SELECT state FROM accounts
        WHERE account_id = ?
    ''', (account_id,))
    result = cursor.fetchone()
    if result:
        return result[0] == AccountState.Valid
    else:
        return False

def get_recent_transactions(account_id, days=7):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    cursor.execute('''
        SELECT * FROM account_history
        WHERE account_id = ? AND date BETWEEN ? AND ?
    ''', (account_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    return cursor.fetchall()


def change_password(account_id,new_password):
    cursor.execute('''
        UPDATE accounts
        SET password = ?
        WHERE account_id = ?
    ''', (new_password, account_id))
    conn.commit()

def check_enough_balance(account_id,required_balance):
    cursor.execute('''
        SELECT balance FROM accounts
        WHERE account_id = ?
    ''', (account_id,))
    result = cursor.fetchone()
    if result:
        balance = result[0]
        return balance >= required_balance
    else:
        return False


def reset():
    cursor.execute('DROP TABLE IF EXISTS accounts')
    create_table()
    create_account('2023123456',111111,500)
    # create_account('2022123456',123456,500)



def query(account_id):
    cursor.execute('''
        SELECT account_id, balance, creation_time FROM accounts
        WHERE account_id = ?
    ''', (account_id,))
    result = cursor.fetchone()
    if result:
        return {
            'account_id': result[0],
            'balance': result[1],
            'creation_time': result[2]
        }
    else:
        return None


def print_all_accounts():
    cursor.execute('SELECT account_id, password FROM accounts')
    accounts = cursor.fetchall()
    
    for account_id, password in accounts:
        print(f'Account ID: {account_id}, Password: {password}')

# print_all_accounts()
# reset()
# print(query('2023123456'))