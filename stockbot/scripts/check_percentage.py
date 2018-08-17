from stockbot.analyzer import pull_percent_change


def main():
    with open('data/stocks/A/daily.json') as f:
        contents = f.read()

    result = pull_percent_change("2018-07-25", contents)
    print(result)


if __name__ == '__main__':
    main()
