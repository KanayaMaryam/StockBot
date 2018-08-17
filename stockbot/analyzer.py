import json
from pathlib import Path
from tqdm import tqdm
import numpy as np
import datetime as dt


def is_loser(stock_history):
    """
    Determines if the stock is a "loser" stock and exploitable
    :param stock_history: Dictionary of date, price pairs
    :return:
    """
    pass


def pull_percent_change(date, stock_history):
    parsed = json.loads(stock_history)
    opening = float(parsed["Time Series (Daily)"][date]["1. open"])
    closing = float(parsed["Time Series (Daily)"][date]["4. close"])
    percent = (closing - opening) / opening
    return percent


def get_losers(date):
    """
    returns array of tuples with first element as percentage and
    second as jsonfile
    """
    datadir = Path("data/stocks/")
    losers = []

    for stock in tqdm(datadir.iterdir()):
        with (stock / "daily.json").open() as f:
            jsonfile = f.read()
        try:
            percentage = pull_percent_change(date, jsonfile)
            losers.append((percentage, stock.name))
        except KeyError:
            pass

    losers.sort()
    return losers[:20]


def pull_data_point(date, stock):
    datadir = Path("data/stocks/")

    with (datadir / stock / "daily.json").open() as f:
        jsonfile = f.read()
    time = dt.datetime.strptime(date, "%Y-%m-%d")
    percentlist = []
    delta = dt.timedelta(1)
    while len(percentlist) < 31:
        try:
            percentlist.append(
                pull_percent_change(time.strftime("%Y-%m-%d"), jsonfile))
        except KeyError as e:
            pass
        finally:
            time = time - delta

    nparray = np.array(percentlist[1:])
    return (percentlist[0], nparray)
