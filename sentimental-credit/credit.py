from cs50 import get_string


def main():

    card_number = get_string("Number: ")

    if not is_valid(card_number):
        print("INVALID")
        return

    card_type = get_card_type(card_number)
    print(card_type)


def is_valid(card_number):

    total = 0
    reverse_digits = card_number[::-1]

    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n

    return total % 10 == 0


def get_card_type(card_number):

    length = len(card_number)
    first_two = int(card_number[:2]) if len(card_number) > 1 else 0
    first_one = int(card_number[0])

    if length == 15 and first_two in [34, 37]:
        return "AMEX"

    elif length == 16 and 51 <= first_two <= 55:
        return "MASTERCARD"

    elif (length == 13 or length == 16) and first_one == 4:
        return "VISA"
    else:
        return "INVALID"


if __name__ == "__main__":
    main()
