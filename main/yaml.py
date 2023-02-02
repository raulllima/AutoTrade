import yaml

with open("../config/config.yaml") as file:
    yamlConfig = yaml.safe_load(file)

    cotacoes = {
        "PETR4": {
            "value": 20.0,
            "today": 25.0
        },
        "MXRF11": {
            "value": 20.0,
            "today": 15.0
        }
    }

    if yamlConfig['trade']['mode'] == "manual":
        for actionType in yamlConfig['trade']['actions']:
            if yamlConfig['trade']['actions'][actionType]['strategy']['name'] == "buy-sell":
                for actionName in yamlConfig['trade']['actions'][actionType]['list']:
                    if actionName in cotacoes:
                        valueBefore = cotacoes[actionName]['value']
                        valueNow = cotacoes[actionName]['today']

                        if (
                            (valueNow - valueBefore) / valueBefore * 100
                            <=
                            yamlConfig['trade']['actions'][actionType]['strategy']['toBuy']['percentage']
                        ):
                            print('toBuy')

                        if (
                            (valueNow - valueBefore) / valueBefore * 100
                            >=
                            yamlConfig['trade']['actions'][actionType]['strategy']['toSell']['percentage']
                        ):
                            print('toSell')

            elif yamlConfig['trade']['actions'][actionType]['strategy']['name'] == "buy-hold":
                for actionName in yamlConfig['trade']['actions'][actionType]['list']:
                    if actionName in cotacoes:
                        valueBefore = cotacoes[actionName]['value']
                        valueNow = cotacoes[actionName]['today']

                        if (
                            (valueNow - valueBefore) / valueBefore * 100
                            <=
                            yamlConfig['trade']['actions'][actionType]['strategy']['toBuy']['percentage']
                        ):
                            print('toBuy')

            # else:
            #     print("Invalid strategy.")

    elif yamlConfig['trade']['mode'] == "auto":
        print("Auto mode")

    else:
        print("Invalid mode")
