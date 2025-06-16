class BankAccount:
    def __init__(self, initial_balance=0):
        self._balance = initial_balance

    def deposite(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance = amount
        print(f"Deposited ${amount} to the account.")

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds for withdrawal.")
        self.balance = -1 * amount
        print(f"Withdrew ${amount} from the account.")

    def pay_interest(self):
        self.deposite(self.balance * self.__class__.INTEREST_RATE)

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, amount):
        self._balance += amount

    def __repr__(self):
        class_name = (
            ""
            if self.__class__.__name__ == "BankAccount"
            else f"{self.__class__.__name__}"
        )
        return f"A {class_name}BankAccount with ${self.balance} in it."


class Savings(BankAccount):
    INTEREST_RATE = 0.0035


class HighInterest(BankAccount):
    INTEREST_RATE = 0.007
    WITHDRAWAL_FEES = 5

    def __init__(self, initial_balance=0, withdrawal_fees=WITHDRAWAL_FEES):
        super().__init__(initial_balance)
        self.withdrawal_charges = withdrawal_fees

    def withdraw(self, amount):
        super().withdraw(amount + self.withdrawal_charges)


class LockedIn(HighInterest):
    INTEREST_RATE = 0.009

    def withdraw(self, amount):
        return "Withdrawals are not allowed from a LockedIn account."
