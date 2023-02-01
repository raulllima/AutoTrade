from datetime import datetime, timedelta
from pandas_datareader import data as pdr
import yfinance as yf
import json
import time
from termcolor import colored

yf.pdr_override()

acoes = ['BBAS3.SA', 'PETR4.SA']

startdate = datetime(2022, 12, 1)
enddate = datetime.now()

# dividendos = yf.Ticker('BBAS3.SA').dividends
# dividends_filtered = dividendos[
#     (dividendos.index >= '2022-12-01')
#     &
#     (dividendos.index <= '2023-01-31')
# ]

while True:
    time.sleep(0.5)
    def converter_float_para_timestamp(data):
        data = datetime.fromtimestamp(data)
        data = data.strftime('%d/%m/%Y %H:%M:%S')
        return data

    def conveter_para_timestamp(data):
        data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
        timestamp = datetime.timestamp(data)
        converter_float_para_timestamp(timestamp)

    teste = conveter_para_timestamp('31/01/2023 00:00:00')

    try:

        data = yf.download(
            acoes,  # list of tickers
            period="30d",         # time period
            interval="1d",       # trading interval
            ignore_tz=True,      # ignore timezone when aligning data from different exchanges?
            prepost=False,
            progress=False,
            show_errors=False)

        # data = yf.download(
        #     acoes,
        #     start='2022-12-31',
        #     end=teste,
        #     progress=False)

        dataNovo = data["Close"]
        dataNovo = dataNovo.to_json(date_format='str', date_unit='s')
        # print(dataNovo)
        resultado = json.loads(json.dumps(json.loads(dataNovo), indent=4))
        firstDate = list(resultado['BBAS3.SA'].keys())[0]
        lastDate = list(resultado['BBAS3.SA'].keys())[-1]
        # print(json.dumps(json.loads(dataNovo), indent=4))
        # print(f"{first} - {last}")

        view = 'BBAS3.SA'

        diferenca = (float(resultado[view][lastDate]) - float(resultado[view]
                                                              [firstDate])) / float(resultado[view][firstDate]) * 100

        print(f"Ação: {view}\n")
        print("Primeiro: R${0:.2f}".format(
            float(resultado[view][firstDate])))
        print("Ultimo: R${0:.2f}".format(
            float(resultado[view][lastDate])))
        print("Alteração:", colored(f"+{diferenca:.2f}%\n", "green") if diferenca > 0 else colored(f"-{diferenca:.2f}%\n", "red"))

    except (ValueError, TypeError, KeyError, IndexError) as e:
        print(e)
        continue
