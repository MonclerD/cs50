from cs50 import get_float


def main():

    while True:
        change = get_float("Change owed: ")
        if change >= 0:
            break

    cents = round(change * 100)

    coins = 0
    for value in [25, 10, 5, 1]:
        coins += cents // value
        cents %= value

    print(coins)


if __name__ == "__main__":
    main()
