# Texas Hold'em Poker tool


## Install
`pip install THPoker`


## Requirements
- python>=3.8


## Usage

### Core
```python
>>> from thpoker.core import Cards, Combo, Hand, Table

>>> combo1 = Combo(hand=Hand("Kh/Ah"), table=Table("8h/9h/Th/Jh/Qh"))
>>> print(combo1)
straight flush (A♥, K♥, Q♥, J♥, T♥)
>>> combo2 = Combo(cards=Cards("Td/As/3h/Th/Ah/Ts/9c"))
>>> print(combo2)
full house (T♦, T♥, T♠, A♠, A♥)
>>> combo1 > combo2
True
```

### Hardcore
```python
>>> from thpoker.hardcore import hcombo

>>> combo1 = hcombo("Kh/Ah/8h/9h/Th/Jh/Qh")
>>> print(combo1)
[9, 14]
>>> combo2 = hcombo("Td/As/3h/Th/Ah/Ts/9c")
>>> print(combo2)
[7, 10, 14]
>>> combo1 > combo2
True
```


## Documentation
[Explore](https://github.com/YegorDB/THPoker/docs)
