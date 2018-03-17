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
# True True False False
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

A number of cards.

Cards could be set from deck

```python
from thpoker.core import Deck, Cards

cards = Cards()
print(cards.items)
# []

deck = Deck()
cards.pull(deck, 5) # pull 5 random cards
print(cards.items)
# [2♦, 7♣, J♦, 3♣, T♠]

cards.clean() # it is not necessary because of pull overwrites items
print(cards.items)
# []
```

Also cards could be set by cards string

```python
from thpoker.core import Cards

cards = Cards("2c/3c/4c/5c/6c")
print(cards.items)
# [2♣, 3♣, 4♣, 5♣, 6♣]
```

There is a possibility to find out whether the cards contain a card or not

```python
from thpoker.core import Card, Cards

card1 = Card("Qd")
card2 = Card("8s")
cards = Cards("Ad/Kd/Qd/Jd/Td")

print(card1 in cards, card2 in cards)
# True False
```

Cards can contain no more than 7 items

```python
from thpoker.core import Deck, Cards

cards1 = Cards()
deck = Deck()
cards1.pull(deck, 10)
print(cards1.items)
# [2♥, A♣, 7♣, T♠, 9♠, 6♦, 3♥]

cards2 = Cards("2s/3s/4s/5s/6s/7s/8s/9s/Ts/Js/Qs/Ks/As")
print(cards2.items)
# [2♠, 3♠, 4♠, 5♠, 6♠, 7♠, 8♠]
```

Table is the same as the Cards, except that the Table can contain no more than 5 items

Hand is the same as the Cards, except that the Hand can contain no more than 2 items and it has additional attributes (hand type and whether hand is a pair or not)

```python
from thpoker.core import Hand

hand1 = Hand("Ad/Js")
print(hand1.type, hand1.is_pair)
# 'AJo' False

hand2 = Hand("7c/Tc")
print(hand2.type, hand2.is_pair)
# 'T7s' False

hand3 = Hand("2s/2h")
print(hand3.type, hand3.is_pair)
# '22' True
```

### Combo

## License
[Apache License](https://choosealicense.com/licenses/apache-2.0/)