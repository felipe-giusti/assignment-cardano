


def get_transaction_costs(notional, rate, country):
    if country == 'GB':
        return (notional*rate) - notional
    elif country == 'NL':
        return abs((notional*(1/rate) - notional))
    else:
        return None