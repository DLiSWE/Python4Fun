import datetime
import pytz

class Account:

    @staticmethod
    def current_time():
        utc_time = datetime.datetime.utcnow()
        return pytz.utc.localize(utc_time)

    def __init__(self, name, balance):
        self.name = name
        self.balance = balacne
        self._transaction_list = [(Account._current_time(),balance)]
        print("Account created for " + self.name)
        self.show_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.show_balance()

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transaction_list.append((Account._current_time(), -amount))
        else:
            print("The amount you entered is more than what you have")

    def show_balance(self):
        print("Balance is {}".format(self._balance))

    def show_transactions(self):
        for date, amount in self.transaction_list:
          if ("{:6} {} on {} (local time was {})".format(amount, tran_type)):
              if amount > 0:
                tran_type = 0
                tran_type = "deposited"
              else:
                tran_type = "withdraw"
                amount *= -1
              print("")