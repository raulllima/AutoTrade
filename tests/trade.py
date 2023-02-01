import MetaTrader5 as mt5


class Trade:
    def init(info):
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

        if not symbol_info.visible:
            print(info['symbol'], "is not visible, trying to switch on")
            if not mt5.symbol_select(info['symbol'], True):
                print("symbol_select({}}) failed, exit", info['symbol'])
                mt5.shutdown()
                quit()

        point = mt5.symbol_info(info['symbol']).point

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": info['symbol'],
            "volume": float(info['qtd']),
            "type": mt5.ORDER_TYPE_BUY,
            "price": mt5.symbol_info_tick(info['symbol']).ask,
            "sl": mt5.symbol_info_tick(info['symbol']).ask-100*point,
            "tp": mt5.symbol_info_tick(info['symbol']).ask+100*point,
            "deviation": 10,
            "magic": 234000,
            "comment": "python script",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        if not float(info['qtd'])*mt5.symbol_info_tick(info['symbol']).ask <= mt5.account_info().balance:
            print('Ops!! Saldo insuficiente.')
            quit()

        result = mt5.order_send(request)
        result = result._asdict()

        if result['comment'] == 'Request executed':
            print({"Ordem enviada": {
                "symbol": info['symbol'],
                "qtd": float(info['qtd']),
                "preço": mt5.symbol_info_tick(info['symbol']).ask}
            })
        elif result['comment'] == 'AutoTrading disabled by client ':
            print('Ordem não enviada, AutoTrading desabilitado.')
        elif result['comment'] == 'Market closed':
            print('Ordem não enviada, mercado fechado.')
        else:
            print(f"Ordem não enviada, {result['comment']}")

        mt5.shutdown()
