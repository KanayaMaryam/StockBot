import json
import time
from pathlib import Path

import pandas as pd
import requests

ALPHA_VANTAGE_API_KEY = 'ES7C3KUBXFKMQMHI'
STOCK_LIST = Path('data/stock-list.csv')


def check_stock_results(parsed):
    if parsed is None:
        return False
    if 'Meta Data' not in parsed:
        return False
    for v in parsed.keys():
        if v.startswith('Time Series'):
            break
    else:
        return False
    return True


def pull_stock_data(ticker,
                    function='TIME_SERIES_WEEKLY_ADJUSTED',
                    retries=100):
    """
    Pulls stock data from Alpha Vantage API
    Doc Link: https://www.alphavantage.co/documentation/
    :param ticker: Stock ticker (e.g. "MSFT")
    :param function: Type of data (refer to api docs for possible functions)
    :return: Parsed json of stock information
    """
    for i in range(retries):
        if i != 0:
            time.sleep(10)
        resp = requests.get(
            'https://www.alphavantage.co/query', {
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
        if not check_stock_results(parsed):
            return None
        return parsed
    raise IOError("Unable to retrieve information for to for %s" % ticker)


def save_all_stock_data(dest_dir, file=STOCK_LIST, verbose=True):
    """
    :param dest_dir: (str or Path) Destination directory to place downloaded
        stocks. Directory will be created if it does not already exist
    """
    dest_dir = Path(dest_dir)
    file = Path(file)
    df = pd.read_csv(str(file.absolute()))
    for sym in df['Symbol']:
        if verbose:
            print("Saving:", sym)
        subdir = dest_dir / sym
        subdir.mkdir(parents=True, exist_ok=True)

        dest_file = subdir / 'daily.json'

        if dest_file.exists():
            with dest_file.open() as f:
                downloaded_parsed = json.load(f)
            if not check_stock_results(downloaded_parsed):
                dest_file.unlink()
            else:
                print("{} already downloaded".format(sym))
                continue
        try:
            daily = pull_stock_data(sym, function='TIME_SERIES_DAILY')
            if daily is None:
                print("{} not found in api".format(sym))
                continue
            with (subdir / 'daily.json').open('w') as f:
                json.dump(daily, f)
        except IOError:
            print("Unable to download %s" % sym)
