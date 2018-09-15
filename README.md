# Texas Hold'em Poker tool

## Install

```
pip install THPoker
```

### Requirements

* Python 3.6 or higher

## Usage

### Core

*Core is the main project module that contains base functional to work with Texas Hold'em Poker*

#### Card(sign)

Some card from standard 52 cards deck.

Sign consisting of two symbols (1st symbol is card weight, 2nd symbol is card suit).

Weight symbols: `'2'` (Two), `'3'` (Three), `'4'` (Four), `'5'` (Five), `'6'` (Six), `'7'` (Seven), `'8'` (Eight), `'9'` (Nine), `'T'` (Ten), `'J'` (Jack), `'Q'` (Queen), `'K'` (King), `'A'` or `'1'` (Ace).

Suit symbols: `'c'` (clubs), `'d'` (diamonds), `'h'` (hearts), `'s'` (spades).

> Sign symbols are ignored since 3rd one.

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

#### Deck()

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
print(deck.size)
# 52
cards = deck.push_cards(3) # return generator of 3 random cards
print(list(cards))
# [A♥, 2♥, J♠]
print(deck.size)
# 49
deck.refresh()
print(deck.size)
# 52
```

#### Cards(cards_string=None, max_count=7)

Several cards.

Cards could be set from deck

```python
from thpoker.core import Deck, Cards

cards = Cards()
print(cards.items)
# []

deck = Deck()
cards.pull(deck, 3) # pull 3 random cards
print(cards.size)
# 3
print(cards.items)
# [2♦, 7♣, J♦]

cards.pull(deck, 2) # add 2 cards to a non empty Cards instance
print(cards.size)
# 5
print(cards.items)
# [2♦, 7♣, J♦, 3♣, T♠]

cards.clean()
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

By default Cards can contain no more than 7 items

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

#### Table(cards_string=None)

Several cards on the table

Table is the same as the Cards, except that the Table can contain no more than 5 items

#### Hand(cards_string=None)

Player's hand cards

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

#### Combo(cards_string=None, cards=None, table=None, hand=None, nominal_check=False)

Cards combination.

There are 9 combinations: `Combo.HIGH_CARD`, `Combo.ONE_PAIR`, `Combo.TWO_PAIRS`, `Combo.THREE_OF_A_KIND`, `Combo.STRAIGHT`, `Combo.FLUSH`, `Combo.FULL_HOUSE`, `Combo.FOUR_OF_A_KIND`, `Combo.STRAIGHT_FLUSH`.

Combo could be set by cards string

```python
from thpoker.core import Combo

combo = Combo(cards_string="8h/9h/Th/Jh/Qh/Kh/Ah")
print(combo)
# straight flush (A♥, K♥, Q♥, J♥, T♥)
print(combo.type == Combo.STRAIGHT_FLUSH)
# True
print(combo.name)
# straight flush
print(combo.cards)
# [A♥, K♥, Q♥, J♥, T♥]
```

Also combo could be set by cards

```python
from thpoker.core import Cards, Combo

cards = Cards("3d/8c/Kh/8s/3h/Js/8h")
combo = Combo(cards=cards)
print(combo)
# full house (8♣, 8♠, 8♥, 3♦, 3♥)
```

Also combo could be set by table and hand

```python
from thpoker.core import Table, Hand, Combo

table = Table("Ts/5c/Ac/Kd/5h")
hand = Hand("Qh/5s")
combo = Combo(table=table, hand=hand)
print(combo)
# three of a kind (5♣, 5♥, 5♠, A♣, K♦)
```

Сombo can be compared
```python
from thpoker.core import Combo

combo1 = Combo(cards_string="8h/2c/Jd/Jh/5s/Kh/5c")
print(combo1)
# two pairs (J♦, J♥, 5♠, 5♣, K♠)
combo2 = Combo(cards_string="9d/As/3c/9h/Qs/9s/9c")
print(combo2)
# four of a kind (9♦, 9♥, 9♠, 9♣, A♠)
print(combo1 > combo2, combo1 < combo2, combo1 != combo2, combo1 == combo2)
# False True True False

combo3 = Combo(cards_string="Qd/6d/9d/Kd/2d/8c/7d")
print(combo3)
# flush (K♦, Q♦, 9♦, 7♦, 6♦)
combo4 = Combo(cards_string="Qd/6d/9d/Kd/2d/6s/6h")
print(combo4)
# flush (K♦, Q♦, 9♦, 6♦, 2♦)
print(combo3 > combo4, combo3 < combo4, combo3 != combo4, combo3 == combo4)
# True False True False

combo5 = Combo(cards_string="4s/3c/8d/Kd/8s/8h/3d")
print(combo5)
# full house (8♦, 8♠, 8♥, 3♣, 3♦)
combo6 = Combo(cards_string="4s/3c/8d/Kd/8s/3s/8c")
print(combo6)
# full house (8♦, 8♠, 8♠, 3♣, 3♠)
print(combo5 > combo6, combo5 < combo6, combo5 != combo6, combo5 == combo6)
# False False False True
```

There is an opportunity to check whether combo base cards include hand cards or not

```python
from thpoker.core import Table, Hand, Combo

table1 = Table("7d/Ts/4d/8c/6h")
hand1 = Hand("Ad/9c")
combo1 = Combo(table=table1, hand=hand1, nominal_check=True)
print(combo1)
# straight (T♠, 9♣, 8♣, 7♦, 6♥)
print(combo1.is_real, combo1.is_nominal)
# True False

table2 = Table("8h/3c/8c/6d/5s")
hand2 = Hand("Qc/Jc")
combo2 = Combo(table=table2, hand=hand2, nominal_check=True)
print(combo2)
# one pair (8♥, 8♣, Q♣, J♣, 6♦)
print(combo2.is_real, combo2.is_nominal)
# False True
# because of combo base cards here is (8♥, 8♣)
```

Full house and two pairs (which combo base cards consist of two parts) can be half nominal

```python
from thpoker.core import Table, Hand, Combo

table1 = Table("Th/6c/5h/Qh/5d")
hand1 = Hand("Qd/Qs")
combo1 = Combo(table=table1, hand=hand1, nominal_check=True)
print(combo1)
# straight (Q♥, Q♦, Q♠, 5♥, 5♦)
print(combo1.is_half_nominal)
# True

table2 = Table("Kd/7s/Th/Ts/Jd")
hand2 = Hand("2h/Kh")
combo2 = Combo(table=table2, hand=hand2, nominal_check=True)
print(combo2)
# one pair (K♦, K♥, T♥, T♠, J♦)
print(combo1.is_half_nominal)
# True
```

### HardCore

*HardCore is the project module that allows you to find a combination faster than Core module, but HardCore is not as friendly as Core is. Since version 2.0.0 hardcore module based on [CTHPoker](https://github.com/YegorDB/CTHPoker) module, wich is based on C.*

#### hcard(sign)

Some card from standard 52 cards deck.

Sign is the same as `core.Card` sign.

```python
from thpoker.hardcore import hcard

card = hcard("5s")
print(card)
# 54
```

HardCore card is a number.

Weight numbers: `20` (Two), `30` (Three), `40` (Four), `50` (Five), `60` (Six), `70` (Seven), `80` (Eight), `90` (Nine), `100` (Ten), `110` (Jack), `120` (Queen), `130` (King), `140` or `10` (Ace).

Suit numbers: `1` (clubs), `2` (diamonds), `3` (hearts), `4` (spades).

```python
from thpoker.hardcore import hcard

card = hcard("Qd")
print(isinstance(card, int))
# True
print(card == 122)
# True
```

#### hdeck()

Standard 52 cards deck.

```python
from thpoker.hardcore import hdeck

deck = hdeck()
print(deck)
# [
#      21,  22,  23,  24,
#      31,  32,  33,  34,
#      41,  42,  43,  44,
#      51,  52,  53,  54,
#      61,  62,  63,  64,
#      71,  72,  73,  74,
#      81,  82,  83,  84,
#      91,  92,  93,  94,
#     101, 102, 103, 104,
#     111, 112, 113, 114,
#     121, 122, 123, 124,
#     131, 132, 133, 134,
#     141, 142, 143, 144,
# ]
print(isinstance(deck, list))
# True
```

#### hcards(cards_string, in_hand=0)

Several cards.

```python
from thpoker.hardcore import hcards

cards = hcards("7s/Td/3h/Kd/5c")
print(cards)
# [74, 102, 33, 132, 51]
print(isinstance(cards, list))
# True
```

Cards can be set as player's hand cards

```python
from thpoker.hardcore import hcards

cards = hcards("Js/Qs", in_hand=1)
print(cards)
# [1114, 1124]
# hand cards are more than usual cards in a thousand
```

#### hcombo(cards_string)

Cards combination set by cards string

There are 9 HardCore combinations: `1` (high card), `2` (one pair), `3` (two pairs), `4` (three of a kind), `5` (straight), `6` (flush), `7` (full house), `8` (four of a kind), `9` (straight flush).

```python
from thpoker.hardcore import hcombo

combo1 = hcombo("Tc/9c/8c/7c/6c")
print(combo1)
# [9, 10]
# 1st number mean that it is straight flush
# 2nd number mean that the highest straight flush card is "ten"

combo2 = hcombo("4d/Js/4s/8d/4h")
print(combo2)
# [4, 4, 11, 8]
# 1st number mean that it is three of a kind
# 2nd number mean that it is three of "fours"
# 3nd and 4th numbers mean additional cards ("jack" and "eight")

print(combo1 > combo2, combo1 < combo2, combo1 != combo2, combo1 == combo2)
# True False True False
```

#### chcombo(cards)

Cards combination set by cards

```python
from thpoker.hardcore import hcards, chcombo

combo1 = chcombo(hcards("Qs/2h/9s/6s/Ad"))
print(combo1)
# [1, 14, 12, 9, 6, 2]
# 1st number mean that it is high card
# other numbers mean combination cards

combo2 = chcombo(hcards("Jd/3d/7d/Kd/5d"))
print(combo2)
# [6, 13, 11, 7, 5, 3]
# 1st number mean that it is flush
# other numbers mean combination cards

print(combo1 > combo2, combo1 < combo2, combo1 != combo2, combo1 == combo2)
# False True True False
```

#### rhcombo(cards)

Cards combination set by table and hand. Also shows combination ratio that mean whether combination is real or not

```python
from thpoker.hardcore import hcards, chcombo

combo1, ratio1 = chcombo(table=hcards("7d/Js/3d/7c/7h"),  hand=hcards("7s/8s", in_hand=1))
print(combo1)
# [8, 7, 11]
# 1st number mean that it is four of a kind
# 2nd number mean that it is four of a "seven"
# 3rd number mean that additional combo card is "jack"
print(ratio1)
# 2
# mean that it is real combo

combo2, ratio2 = chcombo(table=hcards("5h/Qc/8d/Ts/5d"),  hand=hcards("Tc/Kh", in_hand=1))
print(combo2)
# [3, 10, 5, 13]
# 1st number mean that it is two pairs
# 2nd number mean that 1st pair is pair of "ten"
# 3rd number mean that 2nd pair is pair of "five"
# 4th number mean that additional combination card is "king"
print(ratio2)
# 1
# mean that it is half nominal combo

combo3, ratio3 = chcombo(table=hcards("Ad/2s/3c/4c/5h"),  hand=hcards("As/Ac", in_hand=1))
print(combo3)
# [5, 5]
# 1st number mean that it is straight
# 2nd number mean that the highest straight card is "five"
print(ratio3)
# 0
# mean that it is nominal combo
```

## License
[Apache License](https://choosealicense.com/licenses/apache-2.0/)
