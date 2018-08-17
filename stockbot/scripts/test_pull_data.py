from stockbot.analyzer import pull_data_point


def main():
    numpyarray = pull_data_point("2018-06-06", "CAT")
    print(numpyarray)


if __name__ == '__main__':
    main()
