import sqlite3
import datetime
import pytz

#create table if doesn't exist. Tables will include; accounts, history, time, name, balance
db = sqlite3.connect("accounts.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
db.execute("CREATE TABLE IF NOT EXISTS accounts (name TEXT PRIMARY KEY NOT NULL, balance INTEGER NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS history (time TIMESTAMP NOT NULL,"
           " account TEXT NOT NULL, amount INTEGER NOT NULL, PRIMARY KEY (time, account))")
db.execute("CREATE VIEW IF NOT EXISTS localhistory AS"
           " SELECT strftime('%m-%d-%Y %H:%M:%f', history.time, 'localtime') AS localtime,"
           " history.account, history.amount FROM history ORDER BY history.time")


class Account(object):

    @staticmethod
    def _current_time():
        return pytz.timezone('US/Eastern').localize(datetime.datetime.now())

#initialize database
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

    def _save_update(self, amount):
        '''param: absolute value of amount.
        '''
        new_balance = self._balance + amount
        deposit_time = Account._current_time()
        try:
            db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)", (new_balance, self.name))
            db.execute("INSERT INTO history VALUES(?, ?, ?)", (deposit_time, self.name, amount))
        except sqlite3.Error:
            db.rollback()
        finally:
            db.commit()
#deposit function
    def deposit(self, amount: int) -> float:
        if amount > 0.0:
            # new_balance = self._balance + amount
            # deposit_time = Account._current_time()
            # db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)", (new_balance, self.name))
            # db.execute("INSERT INTO history VALUES(?, ?, ?)", (deposit_time, self.name, amount))
            # db.commit()
            # self._balance = new_balance
            self._save_update(amount)
            print("{:.2f} deposited for {}".format(amount / 100, self.name))
        return self._balance / 100
#withdraw function
    def withdraw(self, amount: int) -> float:
        if 0 < amount <= self._balance:
            # new_balance = self._balance - amount
            # withdraw_time = Account._current_time()
            # db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)", (new_balance, self.name))
            # db.execute("INSERT INTO history VALUES(?, ?, ?)",(withdraw_time, self.name, -amount))
            # db.commit()
            # self._balance = new_balance
            self._save_update(-amount)
            print("{:.2f} withdrawn for {}".format(amount / 100, self.name))
            return amount / 100
        else:
            print("The amount must be great than 0 and less than or equal to your balance.")
            return 0.0
#show current balance
    def show_balance(self):
        print("The balance for {} is {:.2f}".format(self.name,self._balance))

if __name__ == '__main__':
    john = Account("John")
    jackson = Account("Jackson")
    terry = Account("Terry")
    john.deposit(50)
    db.close()


