# Core

*Base functional to work with Texas Hold'em Poker*

> Since version 1.1.0 Card and Deck uses from [AGStuff](https://github.com/YegorDB/AGStuff).

## Cards(cards_string=None, cards=None)

Several cards (7 or less).

> Since 1.1.0 version base on [AGStuff](https://github.com/YegorDB/AGStuff) Cards.

## Table(cards_string=None, cards=None)

Several cards on a table. Unlike Cards Table holds 5 items or less.

## Hand(cards_string=None, cards=None)

Player's hand cards. Unlike Cards Hand holds 2 items and has additional information like specific hand type and whether hand is a pair or not.

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

## Combo(cards_string=None, cards=None, table=None, hand=None, ratio_check=False)

Cards combination.

### Combinations
1. High card - `Combo.HIGH_CARD`
2. One pair - `Combo.ONE_PAIR`
3. Two pairs - `Combo.TWO_PAIRS`
4. Three of a kind - `Combo.THREE_OF_A_KIND`
5. Straight - `Combo.STRAIGHT`
6. Flush - `Combo.FLUSH`
7. Full house - `Combo.FULL_HOUSE`
8. Four of a kind - `Combo.FOUR_OF_A_KIND`
9. Straight flush - `Combo.STRAIGHT_FLUSH`

### Combo creation by cards string
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

### Combo creation by cards
```python
>>> from thpoker.core import Cards, Combo

>>> cards = Cards("3d/8c/Kh/8s/3h/Js/8h")
>>> combo = Combo(cards=cards)
>>> print(combo)
full house (8♣, 8♠, 8♥, 3♦, 3♥)
```

### Combo creation by table and hand
```python
>>> from thpoker.core import Table, Hand, Combo

>>> table = Table("Ts/5c/Ac/Kd/5h")
>>> hand = Hand("Qh/5s")
>>> combo = Combo(table=table, hand=hand)
>>> print(combo)
three of a kind (5♣, 5♥, 5♠, A♣, K♦)
```

### Сombo comparison
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

### Ratio check
> Inspect whether combo base cards inlude hand cards

```python
>>> from thpoker.core import Table, Hand, Combo

>>> table1 = Table("7d/Ts/4d/8c/6h")
>>> hand1 = Hand("Ad/9c")
>>> combo1 = Combo(table=table1, hand=hand1, ratio_check=True)
>>> print(combo1)
straight (T♠, 9♣, 8♣, 7♦, 6♥)
>>> combo1.is_real
True
>>> combo1.is_nominal
False
>>> # combo base cards are (T♠, 9♣, 8♣, 7♦, 6♥)

>>> table2 = Table("Th/6c/5h/Qh/5d")
>>> hand2 = Hand("Qd/Qs")
>>> combo2 = Combo(table=table2, hand=hand2, ratio_check=True)
>>> print(combo2)
full house (Q♥, Q♠, Q♦, 5♥, 5♦)
>>> combo2.is_half_nominal
True
>>> # combo base cards are (Q♥, Q♠, Q♦) and (5♥, 5♦)

>>> table3 = Table("Kd/7s/Th/Ts/Jd")
>>> hand3 = Hand("2h/Kh")
>>> combo3 = Combo(table=table3, hand=hand3, ratio_check=True)
>>> print(combo3)
two pairs (K♦, K♥, T♥, T♠, J♦)
>>> combo3.is_half_nominal
True
>>> # combo base cards are (K♦, K♥) and (T♥, T♠)

>>> table4 = Table("8h/3c/8c/6d/5s")
>>> hand4 = Hand("Qc/Jc")
>>> combo4 = Combo(table=table4, hand=hand4, ratio_check=True)
>>> print(combo4)
one pair (8♥, 8♣, Q♣, J♣, 6♦)
>>> combo4.is_real
False
>>> combo4.is_nominal
True
>>> # combo base cards are (8♥, 8♣)
```
