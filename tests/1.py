from trade import Trade
from finance import Finance
import time
import asyncio

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
qtdLimit = [99, 99, 99, 92]


async def taskTrade(qtd):
    print('Iniciando compra de ' + str(qtd) + ' ações.')
    await asyncio.sleep(5)
    Trade.request({
        "type": "buy",
        "symbol": 'PETR4',
        "qtd": float(qtd),
        "action": 'acao'
    })


async def mainTask():
    task = [taskTrade(qtdLimit[i])
            for i in range(0, len(qtdLimit))]
    await asyncio.gather(*task)


async def minha_tarefa_assincrona():

    Trade.request({
        "type": "sell",
        "symbol": 'PETR4',
        "qtd": 99.0,
        "action": 'acao'
    })

try:
    asyncio.run(minha_tarefa_assincrona())

except (AttributeError, TypeError, SystemExit):
    pass
