import json
from stockbot.analyzer import get_losers


def main():
    losers = get_losers("2018-07-20")
    print(losers)


if __name__ == '__main__':
    main()
