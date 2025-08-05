global_var_brand = 'Milton' # mix modeule global var with class var


class Kettle:
    """
    Kettle class

    Attributes:
        brand (str): brand bane
        desc (str): Description of product
    """
    brand = global_var_brand
    desc = None

    def __init__(self, name):
        """
        Kettle clas init method

        Args:
            name (str): brand name
        """
        self.name = name
        self.on = False

    def switch_on(self):
        self.on = True

    def print(self):
        print(self.name, self.on, self.brand, self.desc)

Kettle. desc = 'Indias no. 1 brand' # should update with instance.
k1 = Kettle('k1'); k1.switch_on()
k1.print(); print(k1.__dict__)

k2 = Kettle('k2');
k2.print(); print(k2.__dict__)

# java did good job to prevent access to  intance attribute using private accessfier
# py has difference approach

print('**'*30, 'prg-2')
import datetime, pytz


class Account:
    """ Simple Account class with Balance"""
    # def __new__(cls, *args, **kwargs):
    def __init__(self, name, balance, ):
        self.__balance = balance # _Account__balance --> Data mangling / renamed to hide it.
        self.name = name
        self.tnx_list = []
        print("Account created for ", self.name)

    @staticmethod
    def _current_time(): # remove self , _ is public method.
        return pytz.utc.localize(datetime.datetime.utcnow())

    def deposit(self, amt):
        if amt > 0:
            self.__balance += amt
            self.show_balance()
            self.tnx_list.append((Account._current_time(), amt, 'DEPOSIT')) # append tuple
            # self.tnx_list.append((self._current_time(), amt, 'DEPOSIT'))


    def withdraw(self, amt):
        if self.__balance >= amt > 0:
            self.__balance -= amt
            self.show_balance()
            self.tnx_list.append( (Account._current_time(), -amt, 'WITHDRAW'))  # append tuple
        else: print('Insufficient balance for withdrwal transaction of ', amt)

    def show_balance(self):
        print("balance is {}".format(self.__balance))

    def show_txn(self):
        for date, amount, type in self.tnx_list:
            print(f'{date} : {amount:6} : {type}')
        self.show_balance()


if __name__ == '__main__':
    liu = Account("liu bofa", 0)
    liu.show_balance()
    liu.deposit(5000);
    liu.withdraw(500);
    liu.withdraw(4000)
    liu.__balance = 200; # private variable and has no impact
    liu.show_txn()
    print( liu.__dict__)



