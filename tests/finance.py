import yfinance as yf
import json
import time
from datetime import datetime
from termcolor import colored


class Finance:
    def init():
        yf.pdr_override()

    def checkSymbol(info):
        try:
            data = yf.download(
                info['symbol'],
                period="30d",
                interval="1d",
                ignore_tz=True,
                prepost=False,
                progress=False,
                show_errors=False)

            dataNovo = data["Close"]
            dataNovo = dataNovo.to_json(date_format='str', date_unit='s')
            resultado = json.loads(json.dumps(json.loads(dataNovo), indent=4))

            if len(info['symbol']) == 1:
                returnDataSymbol = []
                firstDate = list(resultado.keys())[0]
                lastDate = list(resultado.keys())[-1]

                diferenca = (
                    (float(resultado[lastDate]) -
                     float(resultado[firstDate])) /
                    float(resultado[firstDate]) * 100
                )

                returnDataSymbol.append({
                    info['symbol'][0]: {
                        "firstData": float(f"{resultado[firstDate]:.2f}"),
                        "lastData": float(f"{resultado[lastDate]:.2f}"),
                        "diferenca": float(f"{diferenca:.2f}")
                    }
                })
                return returnDataSymbol

            elif len(info['symbol']) > 1:
                returnDataSymbol = []
                for symbol in info['symbol']:
                    firstDate = list(resultado[symbol].keys())[0]
                    lastDate = list(resultado[symbol].keys())[-1]

                    diferenca = (
                        (float(resultado[symbol][lastDate]) -
                         float(resultado[symbol][firstDate])) /
                        float(resultado[symbol][firstDate]) * 100
                    )

                    returnDataSymbol.append({
                        symbol: {
                            "firstData": float(f"{resultado[symbol][firstDate]:.2f}"),
                            "lastData": float(f"{resultado[symbol][lastDate]:.2f}"),
                            "diferenca": float(f"{diferenca:.2f}")
                        }
                    })
                    # print(f"Ação: {symbol}\n")
                    # print("Primeiro: R${0:.2f}".format(
                    #     float(resultado[symbol][firstDate])))
                    # print("Ultimo: R${0:.2f}".format(
                    #     float(resultado[symbol][lastDate])))
                    # print("Alteração:",
                    #       colored(
                    #           f"+{diferenca:.2f}%\n", "green") if diferenca > 0 else colored(f"-{diferenca:.2f}%\n", "red"
                    #                                                                          )
                    #       )
                return returnDataSymbol
            # else:
            #     return ('Ops!! Parece que algo deu errado.')

        except Exception as e:
            print(e)

        except (AttributeError, TypeError, KeyError, IndexError, ValueError):
            return ('Ops!! Parece que algo deu errado.')
