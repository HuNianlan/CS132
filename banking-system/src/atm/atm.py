class ATM:
    '''
    This is a class for ATM.

    Attributes:
        cash:               The amount of money in the ATM.
        deposit_amount:     The amount of money a user put in the cash box
    '''
    def __init__(self, balance=800000):
        self.cash: int = balance  
        self.deposit_amount: int = 0

    def deposit(self, amount):
        """deposit"""
        if amount > 0:
            self.cash += amount
            return True
        else:
            return False

    def withdraw(self, amount):
        """withdraw"""
        if amount > 0 and self.cash >= amount:
            self.cash -= amount
            return True
        else:
            return False

    def check_balance(self):
        """check_balance"""
        return self.cash


if __name__ == "__main__":
    atm = ATM(1000)

    atm.deposit(500)

    print("cash in ATM:", atm.check_balance())  # cash in ATM: 1500

    atm.withdraw(200)

    print("cash in ATM:", atm.check_balance())  # cash in ATM: 1300
