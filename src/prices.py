import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import dateutil

ALPHA_VANTAGE_API_KEY = 'ES7C3KUBXFKMQMHI'

def pull_stock_data(ticker: str):
    resp = requests.get('https://www.alphavantage.co/query', {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': ticker,
        'interval': '5min',
        'datatype': 'json',
        'apikey': ALPHA_VANTAGE_API_KEY,
        'outputsize': 'full'
    })
    if resp.status_code == 200:
        return json.loads(resp.text)['Time Series (5min)']

def main():
    res = pull_stock_data('MSFT')
    t = [dateutil.parser.parse(k) for k in res.keys()]
    vals = [float(v['1. open']) for v in res.values()]
    plt.plot(t, vals)
    plt.show()

if __name__ == '__main__':
    main()
