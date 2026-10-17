# import random

# def main():
#     coin = random.choice(["Heads", "Tails"])
#     print(f"The coin landed on: {coin}")


# main()

# import random
# import statistics

# cards = ["jack", "queen", "king"]
# random.shuffle(cards) 
# print(f"{cards}")

import cowsay
import sys

if len(sys.argv) == 2:
    cowsay.trex("hello, " +sys.argv[1])
    