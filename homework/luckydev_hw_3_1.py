"""
Stephen Smith
Class: CS 521 - Summer 2
Date: July 15, 2025
Homework Problem # 3_1
Description of Problem: Calculates the amount of wrapping paper needed
to wrap a package of a defined dimensions. When given a string quit it will
end the program.
"""


def banner():
    print(
        f"""\033[31;43m
    {"=" *80}
    {"Welcome to the gift-wrap calculator!":^80}
    {"=" *80}\033[0m
    """
    )


def calculate_wrapping_paper(dimensions: str) -> str:
    """
    Calculates the amount of wrapping paper needed
    to wrap a package of a defined dimensions.
    """
    l, w, h = map(int, dimensions.split("x"))
    sides = [h * l, l * w, w * h]
    sides.sort()
    area = 2 * h * l + 2 * l * w + 2 * w * h + sides[0]
    return f"You will need {area}cm of wrapping paper"


if __name__ == "__main__":
    banner()
    while True:
        dimensions = input(
            "\nTo quit simply type quit.\nOtherwise\nPlease enter the box dimensions separated with an x, e.g. 2x4x6: "
        )

        if dimensions.lower() == "quit":
            break
        else:
            print(calculate_wrapping_paper(dimensions))
