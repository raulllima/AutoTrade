import time
import MetaTrader5 as mt5

contaProducao = (1486154, "R@ul1605", "Rico-PRD")
contaDemo = (3001486154, "R@ul1605", "Rico-DEMO")

if not mt5.initialize(login=contaDemo[0], server=contaDemo[2], password=contaDemo[1]):
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# if not mt5.initialize(login=contaProducao[0], server=contaProducao[2], password=contaProducao[1]):
#     print("initialize() failed, error code =", mt5.last_error())
#     quit()

symbol = "MXRF11"
qtd = 1.0

print(f"Account balance: R$ {mt5.account_info().balance}")
print(f"Account currency: {mt5.account_info().currency}\n")

# prepare the request structure
symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
    print(symbol, "not found, can not call order_check()")
    mt5.shutdown()
    quit()

# if the symbol is unavailable in MarketWatch, add it
if not symbol_info.visible:
    print(symbol, "is not visible, trying to switch on")
    if not mt5.symbol_select(symbol, True):
        print("symbol_select({}}) failed, exit", symbol)
        mt5.shutdown()
        quit()

point = mt5.symbol_info(symbol).point
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": qtd,
    "type": mt5.ORDER_TYPE_BUY,
    "price": mt5.symbol_info_tick(symbol).ask,
    "sl": mt5.symbol_info_tick(symbol).ask-100*point,
    "tp": mt5.symbol_info_tick(symbol).ask+100*point,
    "deviation": 10,
    "magic": 234000,
    "comment": "python script",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_RETURN,
}

if not qtd*mt5.symbol_info_tick(symbol).ask <= mt5.account_info().balance:
    print('Ops!! Saldo insuficiente.')
    quit()

result = mt5.order_send(request)
result = result._asdict()

if result['comment'] == 'Request executed':
    print({"Ordem enviada": {
        "symbol": symbol,
        "qtd": qtd,
        "preço": mt5.symbol_info_tick(symbol).ask}
    })
elif result['comment'] == 'AutoTrading disabled by client ':
    print('Ordem não enviada, AutoTrading desabilitado.')
elif result['comment'] == 'Market closed':
    print('Ordem não enviada, mercado fechado.')
else:
    print(f"Ordem não enviada, {result['comment']}")

mt5.shutdown()
