import json
import time
from pathlib import Path

import pandas as pd
import requests

ALPHA_VANTAGE_API_KEY = 'ES7C3KUBXFKMQMHI'
STOCK_LIST = Path('../data/stock-list.csv')


def pull_stock_data(ticker: str, function='TIME_SERIES_WEEKLY_ADJUSTED', retries=5):
    """
    Pulls stock data from Alpha Vantage API
    Doc Link: https://www.alphavantage.co/documentation/
    :param ticker: Stock ticker (e.g. "MSFT")
    :param function: Type of data (refer to api docs for possible functions)
    :return: Parsed json of stock information
    """
    for i in range(retries):
        if i != 0:
            time.sleep(5)
        resp = requests.get('https://www.alphavantage.co/query', {
            'function': function,
            'symbol': ticker,
            'interval': '5min',
            'datatype': 'json',
            'apikey': ALPHA_VANTAGE_API_KEY,
            'outputsize': 'full'
        })
        if resp.status_code != 200:
            continue
        parsed = json.loads(resp.text)
        if 'Information' in parsed:
            continue
        return parsed
    raise IOError("Unable to retrieve information for to for %s" % ticker)


def save_all_stock_data(dest_dir, file=STOCK_LIST, verbose=True):
    dest_dir = Path(dest_dir)
    file = Path(file)
    df = pd.read_csv(str(file.absolute()))
    for sym in df['Symbol']:
        if verbose:
            print("Saving:", sym)
        subdir = dest_dir / sym
        subdir.mkdir(parents=True, exist_ok=True)
        def save_file(fname, data):
            with (subdir / fname).open('w') as f:
                f.write(data)
        weekly_adjusted = pull_stock_data(sym, function='TIME_SERIES_WEEKLY_ADJUSTED')
        weekly = pull_stock_data(sym, function='TIME_SERIES_WEEKLY')
        save_file('weekly_adjusted', json.dumps(weekly_adjusted))
        save_file('weekly', json.dumps(weekly))

