from datetime import datetime
from pandas_datareader import data as pdr
import yfinance as yf
import json
import numpy as np

# data = pdr.get_data_yahoo(
#     acoes,
#     start=startdate,
#     end=enddate)

yf.pdr_override()

acoes = ['BBAS3.SA', 'VALE3.SA', 'PETR4.SA']

startdate = datetime(2022, 12, 1)
enddate = datetime.now()

# dividendos = yf.Ticker('BBAS3.SA').dividends
# dividends_filtered = dividendos[
#     (dividendos.index >= '2022-12-01')
#     &
#     (dividendos.index <= '2023-01-31')
# ]
data = yf.download(
    acoes,
    start='2022-11-01',
    end='2023-01-31')

dataNovo = data["Close"]
dataNovo = dataNovo.to_json(date_format='str', date_unit='s')
resultado = json.loads(json.dumps(json.loads(dataNovo), indent=4))
#print(json.dumps(json.loads(dataNovo), indent=4))
primeiroValor = '1669863600'
ultimoValor = '1674702000'

view = 'PETR4.SA'

diferenca = (float(resultado[view][ultimoValor]) - float(resultado[view]
                                                               [primeiroValor])) / float(resultado[view][primeiroValor]) * 100

print(f"Ação: {view}\n")
print("Primeiro: R${0:.2f}".format(
    float(resultado[view][primeiroValor])))
print("Ultimo: R${0:.2f}".format(
    float(resultado[view][ultimoValor])))
print('Alteração: {0:.2f}%'.format(diferenca))

# print(datetime.utcfromtimestamp(ts).strftime('%d/%m/%Y')) # Converte timestamp para data.
