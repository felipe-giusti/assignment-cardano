from abc import ABC
from typing import Any


class TransactionModel(ABC):
    lei: str
    legalName: str
    bic: Any
    notional: float
    rate: float
    transaction_costs: float

    def get_transaction_cost(self, country):
        if country == 'GB':
            return (self.notional*self.rate) - self.notional
        elif country == 'NL':
            return abs((self.notional*(1/self.rate) - self.notional))
        else:
            return None


class TransactionModelPandas(TransactionModel):
    def __init__(self, row) -> None:
        super().__init__()
        self.row = row

    def __getattr__(self, name):
        return self.row[name]
    
    def __setattr__(self, name: str, value: Any) -> None:
        if name == 'row':
            super().__setattr__(name, value)
        else:
            self.row[name] = value 
