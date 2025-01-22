from cs50 import get_int


def main():

    height = get_valid_height()

    for i in range(1, height + 1):
        spaces = " " * (height - i)
        hashes = "#" * i
        print(spaces + hashes)


def get_valid_height():

    while True:
        height = get_int("Height: ")
        if 1 <= height <= 8:
            return height


if __name__ == "__main__":
    main()
