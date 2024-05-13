

import pytest

from api.models.transaction import TransactionModelPandas, TransactionModel

@pytest.fixture
def transaction():
    row = {'lei': '123', 'legalName': 'Example Company', 'bic': 'EXAMPLEBIC', 'notional': 100.0, 'rate': 0.1}
    return TransactionModelPandas(row)

def test_get_transaction_costs_gb(transaction: TransactionModelPandas):
    cost = transaction.get_transaction_cost('GB')
    assert cost == -90.0

def test_get_transaction_costs_nl(transaction: TransactionModelPandas):
    costs = transaction.get_transaction_cost('NL')
    assert costs == 900.0

def test_get_transaction_costs_invalid_country(transaction: TransactionModelPandas):
    assert transaction.get_transaction_cost('XX') == None