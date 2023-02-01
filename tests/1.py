from trade import Trade

Trade.init({
    "login": 3001486154,
    "password": "R@ul1605",
    "server": "Rico-DEMO"
})
try:
    Trade.request({
        "symbol": "MXRF11",
        "qtd": 1,
        "type": "buy",
    })
except (AttributeError):
    print('Ops!! Parece que algo deu errado.')
