import json

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
	
	

	
	

	
	
