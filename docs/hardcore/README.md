# HardCore

*Faster than Core, but not as friendly as Core is. Based on [CTHPoker](https://github.com/YegorDB/CTHPoker) module, wich is based on C.*


## hcard(sign)

Some card from standard 52 cards deck.

> Sign is the same as `cards.core.Card` sign from [AGStuff](https://github.com/YegorDB/AGStuff).

> HardCore card is a number.

### Weights
- Deuce - `20`
- Three - `30`
- Four - `40`
- Five - `50`
- Six - `60`
- Seven - `70`
- Eight - `80`
- Nine - `90`
- Ten - `100`
- Jack - `110`
- Queen - `120`
- King - `130`
- Ace - `140` or `10`

### Suits
- Сlubs - `1`
- Diamonds - `2`
- Hearts - `3`
- Spades - `4`

```python
>>> from thpoker.hardcore import hcard

>>> card = hcard("5s")
>>> card
54
```


## hdeck()

Standard 52 cards deck.

```python
>>> from thpoker.hardcore import hdeck

>>> deck = hdeck()
>>> deck
[
     21,  22,  23,  24,
     31,  32,  33,  34,
     41,  42,  43,  44,
     51,  52,  53,  54,
     61,  62,  63,  64,
     71,  72,  73,  74,
     81,  82,  83,  84,
     91,  92,  93,  94,
    101, 102, 103, 104,
    111, 112, 113, 114,
    121, 122, 123, 124,
    131, 132, 133, 134,
    141, 142, 143, 144
]

>>> isinstance(deck, list)
True
```


## hcards(cards_string, in_hand=False)

Several cards.

```python
>>> from thpoker.hardcore import hcards

>>> cards = hcards("7s/Td/3h/Kd/5c")
>>> cards
[74, 102, 33, 132, 51]
>>> isinstance(cards, list)
True

>>> cards = hcards("Js/Qs", in_hand=True)
>>> cards
[1114, 1124]
>>> # hand cards are more than usual cards in a thousand
```


## hcombo(cards_string)

Cards combination created by cards string.

### Combinations
1. High card - `1`
2. One pair - `2`
3. Two pairs - `3`
4. Three of a kind - `4`
5. Straight - `5`
6. Flush - `6`
7. Full house - `7`
8. Four of a kind - `8`
9. Straight flush - `9`

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

## chcombo(cards)

Cards combination created by cards.

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


## rhcombo(cards)

Cards combination created by table and hand. Also shows combination ratio (whether combo base cards inlude hand cards).

```python
>>> from thpoker.hardcore import hcards, rhcombo

>>> combo1, ratio1 = rhcombo(table=hcards("7d/Js/3d/7c/7h"),  hand=hcards("7s/8s", in_hand=True))
>>> combo1
[8, 7, 11]
>>> ratio1
2
>>> # 1st combo number mean it is four of a kind
... # 2nd combo number mean it is four of a "seven"
... # 3rd combo number mean additional combo card is "jack"
... # ratio mean it is real combo

>>> combo2, ratio2 = rhcombo(table=hcards("5h/Qc/8d/Ts/5d"),  hand=hcards("Tc/Kh", in_hand=True))
>>> combo2
[3, 10, 5, 13]
>>> ratio2
1
>>> # 1st combo number mean that it is two pairs
... # 2nd combo number mean that 1st pair is pair of "ten"
... # 3rd combo number mean that 2nd pair is pair of "five"
... # 4th combo number mean that additional combination card is "king"
... # ratio mean it is half nominal combo

>>> combo3, ratio3 = rhcombo(table=hcards("Ad/2s/3c/4c/5h"),  hand=hcards("Ts/Tc", in_hand=True))
>>> combo3
[5, 5]
>>> ratio3
0
>>> # 1st combo number mean that it is straight
... # 2nd combo number mean that the highest straight card is "five"
... # ratio mean it is nominal combo
```
