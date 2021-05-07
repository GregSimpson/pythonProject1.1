from dataclasses import dataclass


@dataclass
class Card:
    rank: str
    suit: str

def my_awesome_func():
    ...


card = Card("Q", "hearts")

print(card == card)
# True

print(card.rank)
# 'Q'

print(card)
Card(rank='Q', suit='hearts')

