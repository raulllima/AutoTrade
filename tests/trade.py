import MetaTrader5 as mt5


class Trade:
    def init(info):
        print('passei')
        if not mt5.initialize(
                login=info['login'],
                password=info['password'],
                server=info['server']):
            return ({"Erro": "initialize() failed, error code = " + str(mt5.last_error())})

    def request(info):
        print(f"Account balance: R$ {mt5.account_info().balance}")
        print(f"Account currency: {mt5.account_info().currency}\n")

        symbol_info = mt5.symbol_info(info['symbol'])

        if symbol_info is None:
            print(info['symbol'], "not found, can not call order_check()")
            mt5.shutdown()
            quit()

        # if the symbol is unavailable in MarketWatch, add it
        if not symbol_info.visible:
            print(info['symbol'], "is not visible, trying to switch on")
            if not mt5.symbol_select(info['symbol'], True):
                print("symbol_select({}}) failed, exit", info['symbol'])
                mt5.shutdown()
                quit()
