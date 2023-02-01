import MetaTrader5 as mt5


def tradeRequest(info):

    if not mt5.initialize(
            login=info['account']['login'],
            password=info['account']['password'],
            server=info['account']['server']):
        return ({"Erro": "initialize() failed, error code = " + str(mt5.last_error())})

