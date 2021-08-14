import sqlite3
db = sqlite3.connect("accounts.sqlite")
db.execute("CREATE TABLE IF NOT EXISTS accounts (name TEXT PRIMARY KEY NOT NULL, balance INTEGER NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS transactions (time TIMESTAMP NOT NULL,"
           " account TEXT NOT NULL, amount INTEGER NOT NULL, PRIMARY KEY (time, account))")



class Account(object):

    def __init__(self, name:str, opening_balance: int = 0):
        cursor = db.execute("SELECT name, balance FROM accounts WHERE (name= ?)", (name,))
        row = cursor.fetchone()

        if row:
            self.name, self._balance = row
            print("Retrieved record for {}. ".format(self.name), end='')
        else:
            self.name = name
            self._balance = opening_balance
            cursor.execute("INSERT INTO accounts VALUES(?, ?)", (name, opening_balance))
            cursor.connection.commit()
            print("Account created for {}.".format(self.name), end='')
        self.show_balance()

    def deposit(self, amount: int) -> float:
        if amount > 0.00:
            self._balance += amount
            print("{:.2f} deposited".format(amount / 100))
        return self._balance / 100

    def withdraw(self, amount: int) -> float:
        if 0 < amount <= self._balance:
            self._balance -= amount
            print("{:.2f} withdrawn".format(amount / 100))
            return amount / 100
        else:
            print("The amount must be great than 0 and less than or equal to your balance.")
            return 0.00

    def show_balance(self):
        print("The balance for {} is {:.2f}".format(self.name,self._balance / 100))

if __name__ == '__main__':
    john = Account("John")
    john.deposit(1010)
    john.deposit(10)
    john.deposit(10)
    john.deposit(1000000)
    john.show_balance()

    terry = Account("Terry", 5000)
    terry.show_balance()
    jackson = Account("Jackson", 4000)

    db.close()