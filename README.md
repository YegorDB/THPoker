# Texas Hold'em Poker tool

## Requirements
* Python 3.6

## Usage

### Card

Some card from standard 52 cards deck.

Takes one positional argument consisting of two symbols (1st symbol is card weight, 2nd symbol is card suit).

All weight symbols: '2' (Two), '3' (Three), '4' (Four), '5' (Five), '6' (Six), '7' (Seven), '8' (Eight), '9' (Nine), 'T' (Ten), 'J' (Jack), 'Q' (Queen), 'K' (King), 'A' or '1' (Ace).

All suit symbols: 'c' (clubs), 'd' (diamonds), 'h' (hearts), 's' (spades).

```python
from thpoker.core import Card

card = Card('As')
print(card, card.name)
# A♠ 'Ace of spades'
```

Сards can be compared

```python
from thpoker.core import Card

card1 = Card('9h')
card2 = Card('5d')
print(card1 != card2, card1 < card2, card1 > card2, card1 == card2)
# True False True False

card3 = Card('Qc')
card4 = Card('Qs')
print(card3 != card4, card3 < card4, card3 > card4, card3 == card4)
# False False False True
```

Card weights or suits can be compared directly

```python
from thpoker.core import Card

card1 = Card('Td')
card2 = Card('3d')
print(
    card1.weight != card2.weight,
    card1.weight < card2.weight,
    card1.weight > card2.weight,
    card1.weight == card2.weight,
    card1.suit != card2.suit,
    card1.suit == card2.suit)
# True False True False False True

card3 = Card('7h')
card4 = Card('7c')
print(
    card3.weight != card4.weight,
    card3.weight < card4.weight,
    card3.weight > card4.weight,
    card3.weight == card4.weight,
    card3.suit != card4.suit,
    card3.suit == card4.suit)
# False False False True True False
```

Also possible use abstract cards

```python
from thpoker.core import Card

card1 = Card('8s')
card2 = Card('K') # abstract king card
card3 = Card('8') # abstract eight card
print(card1 != card2, card1 < card2, card1 > card2, card1 == card2)
# True False True False
print(card1 != card3, card1 < card3, card1 > card3, card1 == card3)
# False False False True

card4 = Card('4h')
card5 = Card('d') # abstract diamonds card
card6 = Card('h') # abstract hearts card
print(card4 != card5, card4 == card5)
# True False
print(card4 != card6, card4 == card6)
# False True
```

### Deck

Standard 52 cards deck.

There are 13 weights (Two, Three, Four, Five, Six, Seven, Eight, Nine, Ten, Jack, Queen, King, Ace) and 4 suits (clubs, diamonds, hearts, spades).

```python
from thpoker.core import Deck

deck = Deck()
print(deck)
# [
#     2♣, 2♦, 2♥, 2♠,
#     3♣, 3♦, 3♥, 3♠,
#     4♣, 4♦, 4♥, 4♠,
#     5♣, 5♦, 5♥, 5♠,
#     6♣, 6♦, 6♥, 6♠,
#     7♣, 7♦, 7♥, 7♠,
#     8♣, 8♦, 8♥, 8♠,
#     9♣, 9♦, 9♥, 9♠,
#     T♣, T♦, T♥, T♠,
#     J♣, J♦, J♥, J♠,
#     Q♣, Q♦, Q♥, Q♠,
#     K♣, K♦, K♥, K♠,
#     A♣, A♦, A♥, A♠,
# ]
print(len(deck.cards))
# 52
cards = deck.push_cards(3) # return generator of 3 random cards
print(list(cards))
# [A♥, 2♥, J♠]
print(len(deck.cards))
# 49
deck.refresh()
print(len(deck.cards))
# 52
```

### Cards, Table, Hand

### Combo

## License
[Apache License](https://choosealicense.com/licenses/apache-2.0/)