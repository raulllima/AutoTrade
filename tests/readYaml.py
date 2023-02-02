from trade import Trade
from finance import Finance
import yaml
import time

counter = 0

with open("../config/config.yaml") as file:
    yamlConfig = yaml.safe_load(file)
    if yamlConfig['trade']['mode'] == "manual":
        for actionType in yamlConfig['trade']['actions']:
            if yamlConfig['trade']['actions'][actionType]['strategy']['name'] == "buy-sell":
                for actionName in yamlConfig['trade']['actions'][actionType]['list']:
                    try:
                        time.sleep(0.8)
                        response = Finance.checkSymbol({
                            "symbol": yamlConfig['trade']['actions'][actionType]['list'],
                        })
                        diferenca = list(response)[
                            counter][actionName]['diferenca']

                        if diferenca <= yamlConfig['trade']['actions'][actionType]['strategy']['toBuy']['percentage']:
                            Trade.request({
                                "type": "buy",
                                "symbol": actionName,
                                "qtd": 1,
                            })
                            print(
                                f"Compra {actionName}: {diferenca} - {yamlConfig['trade']['actions'][actionType]['strategy']['toBuy']['percentage']}")

                        if diferenca >= yamlConfig['trade']['actions'][actionType]['strategy']['toSell']['percentage']:
                            Trade.request({
                                "type": "sell",
                                "symbol": actionName,
                                "qtd": 1,
                            })
                            print(
                                f"Venda {actionName}: {diferenca} - {yamlConfig['trade']['actions'][actionType]['strategy']['toSell']['percentage']}")

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
