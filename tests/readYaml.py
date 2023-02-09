from trade import Trade
from finance import Finance
import yaml
import time
import math

counter = 0

account = Trade.init({
    "login": 3001486154,
    "password": "R@ul1605",
    "server": "Rico-DEMO"
})


with open("../config/config.yaml") as file:
    yamlConfig = yaml.safe_load(file)

    tradeLimit = (
        account['balance'] *
        (yamlConfig['trade']['balance-limit'] / 100))

    if yamlConfig['trade']['mode'] == "manual":
        for actionType in yamlConfig['trade']['actions']:
            if yamlConfig['trade']['actions'][actionType]['strategy']['name'] == "buy-sell":
                for actionName in yamlConfig['trade']['actions'][actionType]['list']:
                    try:
                        time.sleep(0.8)
                        response = Finance.checkSymbol({
                            "symbol": yamlConfig['trade']['actions'][actionType]['list'],
                        })

                        lastValue = list(response)[
                            counter][actionName]['lastData']

                        diferenca = list(response)[
                            counter][actionName]['diferenca']

                        if lastValue <= tradeLimit:
                            totalQtdLimit = math.floor(tradeLimit / lastValue)
                            qtdLimit = []
                            while totalQtdLimit >= 99:
                                qtdLimit.append(99)
                                totalQtdLimit -= 99

                            qtdLimit.append(totalQtdLimit)

                        if diferenca <= yamlConfig['trade']['actions'][actionType]['strategy']['toBuy']['percentage']:
                            # for qtd in qtdLimit:
                            Trade.request({
                                "type": "buy",
                                "symbol": actionName,
                                "qtd": float(qtdLimit[0]),
                                "action": actionType
                            })
                            
                        if diferenca >= yamlConfig['trade']['actions'][actionType]['strategy']['toSell']['percentage']:
                            Trade.request({
                                "type": "sell",
                                "symbol": actionName,
                                "qtd": 1.0,
                                "action": actionType
                            })

                        counter += 1
                    except (AttributeError, TypeError):
                        continue

            elif yamlConfig['trade']['actions'][actionType]['strategy']['name'] == "buy-hold":
                for actionName in yamlConfig['trade']['actions'][actionType]['list']:
                    pass

    elif yamlConfig['trade']['mode'] == "auto":
        print("Auto mode")

    else:
        print("Invalid mode")
