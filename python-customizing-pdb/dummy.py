from random import random


def print_the_things(number: int, text: str, big_list: list):
    import debug; debug.stop()  # custom breakpoint

    print(f"Number: {number}, Text: {text}, List: {big_list}")


print_the_things(
    number=10,
    text="Blame and lies, contradictions arise",
    big_list=[random() for _ in range(100000)]
)