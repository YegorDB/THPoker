# Texas Hold'em Poker tool

## Install

`pip install THPoker`

### Requirements

* Python 3.6 or higher

## Usage

### Core

*Core is the main project module that contains base functional to work with Texas Hold'em Poker*

> Since 1.1.0 version there isn't Card and Deck in THPoker core, they uses from [AGStuff](https://github.com/YegorDB/AGStuff).

#### Cards(cards_string=None, cards=None)

Several cards (7 or less).

> Since 1.1.0 version base on [AGStuff](https://github.com/YegorDB/AGStuff) Cards.

#### Table(cards_string=None, cards=None)

Several cards on the table

Table is the same as the Cards, except that the Table can contain no more than 5 items

#### Hand(cards_string=None, cards=None)

Player's hand cards

Hand is the same as the Cards, except that the Hand can contain no more than 2 items and it has additional attributes (hand type and whether hand is a pair or not)

```python
>>> from thpoker.core import Hand

>>> hand1 = Hand("Ad/Js")
>>> hand1.type
'AJo'
>>> hand1.is_pair
False

>>> hand2 = Hand("7c/Tc")
>>> hand2.type
'T7s'
>>> hand2.is_pair
False

>>> hand3 = Hand("2s/2h")
>>> hand3.type
'22'
>>> hand3.is_pair
True
```

#### Combo(cards_string=None, cards=None, table=None, hand=None, nominal_check=False)

Cards combination.

There are 9 combinations: `Combo.HIGH_CARD`, `Combo.ONE_PAIR`, `Combo.TWO_PAIRS`, `Combo.THREE_OF_A_KIND`, `Combo.STRAIGHT`, `Combo.FLUSH`, `Combo.FULL_HOUSE`, `Combo.FOUR_OF_A_KIND`, `Combo.STRAIGHT_FLUSH`.

Combo could be set by cards string

```python
>>> from thpoker.core import Combo

>>> combo = Combo(cards_string="8h/9h/Th/Jh/Qh/Kh/Ah")
>>> combo.type
9
>>> combo.type == Combo.STRAIGHT_FLUSH
True
>>> combo.cards
[A♥, K♥, Q♥, J♥, T♥]
>>> combo.name
'straight flush'
>>> combo
[9, A♥, K♥, Q♥, J♥, T♥]
>>> print(combo)
straight flush (A♥, K♥, Q♥, J♥, T♥)
```

Also combo could be set by cards

```python
>>> from thpoker.core import Cards, Combo

>>> cards = Cards("3d/8c/Kh/8s/3h/Js/8h")
>>> combo = Combo(cards=cards)
>>> print(combo)
full house (8♣, 8♠, 8♥, 3♦, 3♥)
```

Also combo could be set by table and hand

```python
>>> from thpoker.core import Table, Hand, Combo

>>> table = Table("Ts/5c/Ac/Kd/5h")
>>> hand = Hand("Qh/5s")
>>> combo = Combo(table=table, hand=hand)
>>> print(combo)
three of a kind (5♣, 5♥, 5♠, A♣, K♦)
```

Сombo can be compared
```python
>>> from thpoker.core import Combo

>>> combo1 = Combo(cards_string="8h/2c/Jd/Jh/5s/Kh/5c")
>>> print(combo1)
two pairs (J♦, J♥, 5♠, 5♣, K♥)
>>> combo2 = Combo(cards_string="9d/As/3c/9h/Qs/9s/9c")
>>> print(combo2)
four of a kind (9♦, 9♥, 9♠, 9♣, A♠)
>>> combo1 > combo2
False
>>> combo1 < combo2
True
>>> combo1 != combo2
True
>>> combo1 == combo2
False

>>> combo3 = Combo(cards_string="Qd/6d/9d/Kd/2d/8c/7d")
>>> print(combo3)
flush (K♦, Q♦, 9♦, 7♦, 6♦)
>>> combo4 = Combo(cards_string="Qd/6d/9d/Kd/2d/6s/6h")
>>> print(combo4)
flush (K♦, Q♦, 9♦, 6♦, 2♦)
>>> combo3 > combo4
True
>>> combo3 < combo4
False
>>> combo3 != combo4
True
>>> combo3 == combo4
False

>>> combo5 = Combo(cards_string="4s/3c/8d/Kd/8s/8h/3d")
>>> print(combo5)
full house (8♦, 8♠, 8♥, 3♣, 3♦)
>>> combo6 = Combo(cards_string="4s/3c/8d/Kd/8s/3s/8c")
>>> print(combo6)
full house (8♦, 8♠, 8♣, 3♣, 3♠)
>>> combo5 > combo6
False
>>> combo5 < combo6
False
>>> combo5 != combo6
False
>>> combo5 == combo6
True
```

There is an opportunity to check whether combo base cards include hand cards or not

```python
>>> from thpoker.core import Table, Hand, Combo

>>> table1 = Table("7d/Ts/4d/8c/6h")
>>> hand1 = Hand("Ad/9c")
>>> combo1 = Combo(table=table1, hand=hand1, nominal_check=True)
>>> print(combo1)
straight (T♠, 9♣, 8♣, 7♦, 6♥)
>>> combo1.is_real
True
>>> combo1.is_nominal
False
>>> # combo base cards are (T♠, 9♣, 8♣, 7♦, 6♥)

>>> table2 = Table("8h/3c/8c/6d/5s")
>>> hand2 = Hand("Qc/Jc")
>>> combo2 = Combo(table=table2, hand=hand2, nominal_check=True)
>>> print(combo2)
one pair (8♥, 8♣, Q♣, J♣, 6♦)
>>> combo2.is_real
False
>>> combo2.is_nominal
True
>>> # combo base cards are (8♥, 8♣)
```

Full house and two pairs (which combo base cards consist of two parts) can be half nominal

```python
>>> from thpoker.core import Table, Hand, Combo

>>> table1 = Table("Th/6c/5h/Qh/5d")
>>> hand1 = Hand("Qd/Qs")
>>> combo1 = Combo(table=table1, hand=hand1, nominal_check=True)
>>> print(combo1)
full house (Q♥, Q♠, Q♦, 5♥, 5♦)
>>> combo1.is_half_nominal
True
>>> # combo base cards are (Q♥, Q♠, Q♦) and (5♥, 5♦)

>>> table2 = Table("Kd/7s/Th/Ts/Jd")
>>> hand2 = Hand("2h/Kh")
>>> combo2 = Combo(table=table2, hand=hand2, nominal_check=True)
>>> print(combo2)
two pairs (K♦, K♥, T♥, T♠, J♦)
>>> combo1.is_half_nominal
True
>>> # combo base cards are (K♦, K♥) and (T♥, T♠)
```

### HardCore

*HardCore is the project module that allows you to find a combination faster than Core module, but HardCore is not as friendly as Core is. Since version 1.1.0 hardcore module based on [CTHPoker](https://github.com/YegorDB/CTHPoker) module, wich is based on C.*

#### hcard(sign)

Some card from standard 52 cards deck.

Sign is the same as `cards.core.Card` sign from [AGStuff](https://github.com/YegorDB/AGStuff).

```python
>>> from thpoker.hardcore import hcard

>>> card = hcard("5s")
>>> card
54
```

HardCore card is a number.

Weight numbers: `20` (Two), `30` (Three), `40` (Four), `50` (Five), `60` (Six), `70` (Seven), `80` (Eight), `90` (Nine), `100` (Ten), `110` (Jack), `120` (Queen), `130` (King), `140` or `10` (Ace).

Suit numbers: `1` (clubs), `2` (diamonds), `3` (hearts), `4` (spades).

```python
>>> from thpoker.hardcore import hcard

>>> card = hcard("Qd")
>>> isinstance(card, int)
True
>>> card == 122
True
```

#### hdeck()

Standard 52 cards deck.

```python
>>> from thpoker.hardcore import hdeck

>>> deck = hdeck()
>>> deck
[
    21, 22, 23, 24,
    31, 32, 33, 34,
    41, 42, 43, 44,
    51, 52, 53, 54,
    61, 62, 63, 64,
    71, 72, 73, 74,
    81, 82, 83, 84,
    91, 92, 93, 94,
    101, 102, 103, 104,
    111, 112, 113, 114,
    121, 122, 123, 124,
    131, 132, 133, 134,
    141, 142, 143, 144
]

>>> isinstance(deck, list)
True
```

#### hcards(cards_string, in_hand=0)

Several cards.

```python
>>> from thpoker.hardcore import hcards

>>> cards = hcards("7s/Td/3h/Kd/5c")
>>> cards
[74, 102, 33, 132, 51]
>>> isinstance(cards, list)
True
```

Cards can be set as player's hand cards

```python
>>> from thpoker.hardcore import hcards

>>> cards = hcards("Js/Qs", in_hand=1)
>>> cards
[1114, 1124]
>>> # hand cards are more than usual cards in a thousand
```

#### hcombo(cards_string)

Cards combination set by cards string

There are 9 HardCore combinations: `1` (high card), `2` (one pair), `3` (two pairs), `4` (three of a kind), `5` (straight), `6` (flush), `7` (full house), `8` (four of a kind), `9` (straight flush).

```python
>>> from thpoker.hardcore import hcombo

>>> combo1 = hcombo("Tc/9c/8c/7c/6c")
>>> combo1
[9, 10]
>>> # 1st number mean it is straight flush
... # 2nd number mean the highest straight flush card is "ten"

>>> combo2 = hcombo("4d/Js/4s/8d/4h")
>>> combo2
[4, 4, 11, 8]
>>> # 1st number mean it is three of a kind
... # 2nd number mean it is three of "fours"
... # 3nd and 4th numbers mean additional cards ("jack" and "eight")

>>> combo1 > combo2
True
>>> combo1 < combo2
False
>>> combo1 != combo2
True
>>> combo1 == combo2
False
```

#### chcombo(cards)

Cards combination set by cards

```python
>>> from thpoker.hardcore import hcards, chcombo

>>> combo1 = chcombo(hcards("Qs/2h/9s/6s/Ad"))
>>> combo1
[1, 14, 12, 9, 6, 2]
>>> # 1st number mean it is high card
... # other numbers mean combination cards

>>> combo2 = chcombo(hcards("Jd/3d/7d/Kd/5d"))
>>> combo2
[6, 13, 11, 7, 5, 3]
>>> # 1st number mean it is flush
... # other numbers mean combination cards

>>> combo1 > combo2
False
>>> combo1 < combo2
True
>>> combo1 != combo2
True
>>> combo1 == combo2
False
```

#### rhcombo(cards)

Cards combination set by table and hand. Also shows combination ratio that mean whether combination is real or not

```python
>>> from thpoker.hardcore import hcards, rhcombo

>>> combo1, ratio1 = rhcombo(table=hcards("7d/Js/3d/7c/7h"),  hand=hcards("7s/8s", in_hand=1))
>>> combo1
[8, 7, 11]
>>> ratio1
2
>>> # 1st combo number mean it is four of a kind
... # 2nd combo number mean it is four of a "seven"
... # 3rd combo number mean additional combo card is "jack"
... # ratio mean it is real combo

>>> combo2, ratio2 = rhcombo(table=hcards("5h/Qc/8d/Ts/5d"),  hand=hcards("Tc/Kh", in_hand=1))
>>> combo2
[3, 10, 5, 13]
>>> ratio2
1
>>> # 1st combo number mean that it is two pairs
... # 2nd combo number mean that 1st pair is pair of "ten"
... # 3rd combo number mean that 2nd pair is pair of "five"
... # 4th combo number mean that additional combination card is "king"
... # ratio mean it is half nominal combo

>>> combo3, ratio3 = rhcombo(table=hcards("Ad/2s/3c/4c/5h"),  hand=hcards("Ts/Tc", in_hand=1))
>>> combo3
[5, 5]
>>> ratio3
0
>>> # 1st combo number mean that it is straight
... # 2nd combo number mean that the highest straight card is "five"
... # ratio mean it is nominal combo
```
