import platform
from enum import Enum
import service
import settings
from utils import timestamp


class TransactionType(Enum):
    ADD = 1
    PAY = 2

    def __str__(self):
        return self.name.lower()


class Transaction:
    def __init__(self, uid, account, amount, transaction_type, name="Transaction", description="Short transaction desc."):
        self.id = uid
        self.transaction_type = transaction_type.value
        self.name = name
        self.description = description
        self.account_id = account.id
        self.amount = "{:.2f}".format(float(amount))

        _acc_bal, amt = float(account.balance), float(self.amount)
        self.balance_after = "{:.2f}".format(_acc_bal) if transaction_type is TransactionType.PAY else "{:.2f}".format(_acc_bal)

        self.sign = self._sign()
        self.platform = "Mobile" if platform.node() == "localhost" else platform.node()
        self.os = platform.platform()
        self.timestamp = timestamp()

        print(f"{account.name}'s Transaction no. {self.id}: {self._sign()}{amount}{service.service.get_currency()}")

    def _sign(self):
        return "-" if self.transaction_type is TransactionType.PAY.value else "+"

    def get_id(self):
        return self.id

    def get_info(self):
        print(f"{self.id}: {self.transaction_type}")
        print(f"Account: {self.account_id}\nAmount:{self.amount}{settings.get_currency()}\n{self.timestamp}")


class PayTransaction(Transaction):
    def __init__(self, uid, account, amount, name, description):
        super().__init__(uid, account, amount, TransactionType.PAY, name=name, description=description)


class AddTransaction(Transaction):
    def __init__(self, uid, account, amount, name, description):
        super().__init__(uid, account, amount, TransactionType.ADD, name=name, description=description)
