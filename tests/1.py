from trade import Trade
from finance import Finance
import time

Trade.init({
    "login": 3001486154,
    "password": "R@ul1605",
    "server": "Rico-DEMO"
})

symbols = ['BBAS3.SA', 'PETR4.SA', 'NUBR33.SA']

# while True:
# try:
#     time.sleep(0.8)
#     teste = Finance.checkSymbol({
#         "symbol": symbols,
#     })
#     print(teste)
# except (AttributeError, TypeError):
#     continue
try:
    Trade.request({
        "type": "buy",
        "symbol": "PETR4",
        "qtd": 1.0,
        "action": 'acao'
    })
except (AttributeError):
    print('Ops!! Parece que algo deu errado.')
