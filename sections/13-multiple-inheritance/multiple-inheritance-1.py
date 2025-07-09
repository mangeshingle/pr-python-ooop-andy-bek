import re
from random import randint


class CreditCard:
    MIN_FOURTEEN_DIGIT = 10000000000000
    MAX_FOURTEEN_DIGIT = 99999999999999

    def __init__(self):
        self._number = self.generate()

    def generate(self):
        return str(
            randint(CreditCard.MIN_FOURTEEN_DIGIT, CreditCard.MAX_FOURTEEN_DIGIT)
        )

    @property
    def number(self):
        return " ".join(re.findall(".{4}", self._number))


class VisaMixin:
    def generate(self):
        return "42" + super().generate()


class MasterCardMixin:
    def generate(self):
        return "53" + super().generate()


class ValidMixin:
    def generate(self):
        fifteen_digit = super().generate()[0:15]
        checksum = ValidMixin.get_cheksum(fifteen_digit)
        return fifteen_digit + checksum

    @staticmethod
    def get_cheksum(fifteen_digit):
        cumulative_sum = 0
        toggle = True
        for number in fifteen_digit[::-1]:
            number = 2 * int(number) if toggle else int(number)
            toggle = not toggle
            cumulative_sum += number - 9 if number > 9 else number

        return str((10 - cumulative_sum) % 10)


class Visa(VisaMixin, CreditCard):
    pass


class ValidVisa(ValidMixin, VisaMixin, CreditCard):
    pass


class MasterCard(MasterCardMixin, CreditCard):
    pass


class ValidMasterCard(ValidMixin, MasterCardMixin, CreditCard):
    pass


if __name__ == "__main__":
    Visa = Visa()
    print(f"Visa: {Visa.number}".rjust(40))

    MasterCard = MasterCard()
    print(f"MasterCard: {MasterCard.number}".rjust(40))

    valid_visa = ValidVisa()
    print(f"Valid Visa: {valid_visa.number}".rjust(40))

    valid_master_card = ValidMasterCard()
    print(f"Valid MasterCard: {valid_master_card.number}".rjust(40))
