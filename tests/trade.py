import MetaTrader5 as mt5
import json


class Trade:
    def init(info):
        if not mt5.initialize(
                login=info['login'],
                password=info['password'],
                server=info['server']):
            return ({
                "Erro": "initialize() failed, error code = " + str(mt5.last_error())
            })
        else:
            return ({
                "currency": mt5.account_info().currency,
                "balance": mt5.account_info().balance,
            })

    def account(symbol):
        wallet = []
        symbol = symbol.split('.SA')[0]
        position = mt5.positions_get(symbol=symbol)
        
        if position is None:
            return ({"Erro": f"'{symbol}' não encontrada."})
        else:
            positionJSON = json.loads(json.dumps(position, indent=4))
            if positionJSON:
                positionStatus = positionJSON[0][5]

                wallet.append({
                    "symbol": positionJSON[0][16],
                    "qtd": positionJSON[0][9] if positionStatus == 0 else -positionJSON[0][9]
                })
                return wallet[0]
            else:
                return ({"Erro": f"'{symbol}' não encontrada."})

    def teste():
        wallet = []
        position = mt5.positions_get()
        if len(position) == 0:
            return ({"Erro": "Nenhuma posição encontrada."})

        positionJSON = json.loads(json.dumps(position, indent=4))
        for ticket in positionJSON:
            wallet.append({
                "symbol": ticket[16],
                "qtd": ticket[9],
            })
        return wallet

    def request(info):
        symbol = info['symbol'].split('.SA')[0]
        symbol_info = mt5.symbol_info(symbol)
        point = mt5.symbol_info(symbol).point

        if info['action'] != "fii" and info['qtd'] != 100.0:
            symbol = f"{symbol}F"

        if symbol_info is None:
            print(symbol, "not found, can not call order_check()")
            mt5.shutdown()
            quit()

        if not symbol_info.visible:
            print(symbol, "is not visible, trying to switch on")
            if not mt5.symbol_select(symbol, True):
                print("symbol_select({}}) failed, exit", symbol)
                mt5.shutdown()
                quit()

        if info['type'] == 'buy':
            order_type = mt5.ORDER_TYPE_BUY
            order_sl = mt5.symbol_info_tick(symbol).ask-100*point
            order_tp = mt5.symbol_info_tick(symbol).ask+100*point
        elif info['type'] == 'sell':
            order_type = mt5.ORDER_TYPE_SELL
            order_sl = mt5.symbol_info_tick(symbol).ask+100*point
            order_tp = mt5.symbol_info_tick(symbol).ask-100*point
        else:
            return ({"Erro": "Tipo de ordem inválido."})

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": info['qtd'],
            "type": order_type,
            "price": mt5.symbol_info_tick(symbol).ask,
            "sl": order_sl,
            "tp": order_tp,
            "deviation": 10,
            "magic": 234000,
            "comment": "python script",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        if not info['qtd'] * mt5.symbol_info_tick(symbol).ask <= mt5.account_info().balance:
            print('Ops!! Saldo insuficiente.')
            quit()

        result = mt5.order_send(request)
        result = result._asdict()

        if result['comment'] == 'Request executed':
            print({"Ordem enviada": {
                "type": info['type'],
                "symbol": symbol,
                "qtd": info['qtd'],
                "price": mt5.symbol_info_tick(symbol).ask * info['qtd']}
            })
        elif result['comment'] == 'AutoTrading disabled by client ':
            print('Ordem não enviada, AutoTrading desabilitado.')
        elif result['comment'] == 'Market closed':
            print('Ordem não enviada, mercado fechado.')
        else:
            print(f"Ordem não enviada, {result['comment']}")
