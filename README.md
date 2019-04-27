# Texas Hold'em Poker tool

## Install

`pip install THPoker`

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
>>> from thpoker.core import Card

>>> card = Card('As')
>>> card
A♠
>>> card.name
'Ace of spades'
```

Сards can be compared

```python
>>> from thpoker.core import Card

>>> card1 = Card('9h')
>>> card2 = Card('5d')
>>> card1 != card2
True
>>> card1 < card2
False
>>> card1 > card2
True
>>> card1 == card2
False

>>> card3 = Card('Qc')
>>> card4 = Card('Qs')
>>> card3 != card4
False
>>> card3 < card4
False
>>> card3 > card4
False
>>> card3 == card4
True
```

Card weights or suits can be compared directly

```python
>>> from thpoker.core import Card

>>> card1 = Card('Td')
>>> card2 = Card('3d')
>>> card1.weight != card2.weight
True
>>> card1.weight < card2.weight
False
>>> card1.weight > card2.weight
True
>>> card1.weight == card2.weight
False
>>> card1.suit != card2.suit
False
>>> card1.suit == card2.suit
True

>>> card3 = Card('7h')
>>> card4 = Card('7c')
>>> card3.weight != card4.weight
False
>>> card3.weight < card4.weight
False
>>> card3.weight > card4.weight
False
>>> card3.weight == card4.weight
True
>>> card3.suit != card4.suit
True
>>> card3.suit == card4.suit
False
```

Also possible use abstract cards

```python
>>> from thpoker.core import Card

>>> card1 = Card('8s')
>>> card2 = Card('K') # abstract king card
>>> card3 = Card('8') # abstract eight card
>>> card1 != card2
True
>>> card1 < card2
True
>>> card1 > card2
False
>>> card1 == card2
False
>>> card1 != card3
False
>>> card1 < card3
False
>>> card1 > card3
False
>>> card1 == card3
True

>>> card4 = Card('4h')
>>> card5 = Card('d') # abstract diamonds card
>>> card6 = Card('h') # abstract hearts card
>>> card4 != card5
True
>>> card4 == card5
False
>>> card4 != card6
False
>>> card4 == card6
True
```

#### Deck()

Standard 52 cards deck.

There are 13 weights (Two, Three, Four, Five, Six, Seven, Eight, Nine, Ten, Jack, Queen, King, Ace) and 4 suits (clubs, diamonds, hearts, spades).

```python
>>> from thpoker.core import Deck

>>> deck = Deck()
>>> deck
[
    2♣, 2♦, 2♥, 2♠,
    3♣, 3♦, 3♥, 3♠,
    4♣, 4♦, 4♥, 4♠,
    5♣, 5♦, 5♥, 5♠,
    6♣, 6♦, 6♥, 6♠,
    7♣, 7♦, 7♥, 7♠,
    8♣, 8♦, 8♥, 8♠,
    9♣, 9♦, 9♥, 9♠,
    T♣, T♦, T♥, T♠,
    J♣, J♦, J♥, J♠,
    Q♣, Q♦, Q♥, Q♠,
    K♣, K♦, K♥, K♠,
    A♣, A♦, A♥, A♠
]
>>> deck.size
52
>>> cards = deck.push_cards(3)
>>> cards # generator of 3 random cards
<generator object Deck.push_cards at 0x7f5b1d52e228>
>>> list(cards)
[6♦, 4♣, J♠]
>>> deck.size
49
>>> deck.refresh()
>>> deck.size
52
```

#### Cards(cards_string=None, max_count=7)

Several cards.

Cards could be set from deck

```python
>>> from thpoker.core import Deck, Cards

>>> cards = Cards()
>>> cards.size
0
>>> cards
[]

>>> deck = Deck()
>>> deck.size
52
>>> cards.pull(deck, 3) # pull 3 random cards
>>> deck.size
49
>>> cards.size
3
>>> cards
[4♣, 5♠, 7♦]

>>> cards.pull(deck, 2) # add 2 more cards
>>> cards.size
5
>>> cards
[4♣, 5♠, 7♦, 9♥, J♠]

>>> cards.clean()
>>> cards.size
0
>>> cards
[]
```

Also cards could be set by cards string

```python
>>> from thpoker.core import Cards

>>> cards = Cards("2c/3c/4c/5c/6c")
>>> cards
[2♣, 3♣, 4♣, 5♣, 6♣]
```

There is a possibility to find out whether the cards contain a card or not

```python
>>> from thpoker.core import Card, Cards

>>> card1 = Card("Qd")
>>> card2 = Card("8s")
>>> cards = Cards("Ad/Kd/Qd/Jd/Td")
>>> card1 in cards
True
>>> card2 in cards
False
```

By default Cards can contain no more than 7 items

```python
>>> from thpoker.core import Deck, Cards

>>> cards1 = Cards()
>>> deck = Deck()
>>> cards1.pull(deck, 10)
>>> cards1
[5♣, 3♥, Q♠, J♣, J♦, 8♠, 9♣]

>>> cards2 = Cards("2s/3s/4s/5s/6s/7s/8s/9s/Ts/Js/Qs/Ks/As")
>>> cards2
[2♠, 3♠, 4♠, 5♠, 6♠, 7♠, 8♠]
```

#### Table(cards_string=None)

Several cards on the table

Table is the same as the Cards, except that the Table can contain no more than 5 items

#### Hand(cards_string=None)

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

*HardCore is the project module that allows you to find a combination faster than Core module, but HardCore is not as friendly as Core is. Since version 2.0.0 hardcore module based on [CTHPoker](https://github.com/YegorDB/CTHPoker) module, wich is based on C.*

#### hcard(sign)

Some card from standard 52 cards deck.

Sign is the same as `core.Card` sign.

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

### Game

*Game is project module that allows create Texas Hold'em Poker game and handle its logic*

#### Player.Action(kind, bet=0)

Player's action.

There are six kinds of action: `Player.Action.FOLD`, `Player.Action.CALL`, `Player.Action.CHECK`, `Player.Action.RAISE`, `Player.Action.BLIND_BET`, `Player.Action.ALL_IN`.

Takes two argumens: action kind and bet value (second one is used only in raise or blind bet kind of situation).

```python
>>> from thpoker.game import Player

>>> raise_action = Player.Action(Player.Action.RAISE, 20)
>>> raise_action.kind
'raise'
>>> raise_action.bet
20

>>> call_action = Player.Action(Player.Action.CALL)
>>> call_action.kind
'call'
```

#### Player(identifier)

Player activity.

Takes one argument: identifier wich can help distinguish one player from other. Identifier need to provide __hash__ method.

```python
>>> from thpoker.game import Player

>>> player = Player(12345) # set player with number identifier
>>> player.identifier
12345

>>> player = Player('asdfg') # set player with string identifier
>>> player.identifier
'asdfg'
```

#### Game.Stage

There are four game stages: `Game.Stage.PRE_FLOP`, `Game.Stage.FLOP`, `Game.Stage.TURN`, `Game.Stage.RIVER`.

#### Game states

There are five game states: `Game.NORMAL`, `Game.FOLD`, `Game.ALL_IN`, `Game.SHOW_DOWN`, `Game.THE_END`.

#### Game points

There are three game points: `Game.ACTION_NEEDED`, `Game.STAGE_NEEDED`, `Game.ROUND_NEEDED`.

#### Game(settings, \*players)

Texas Hold'em poker game logic handler.

Takes settings argument and Player instanses (from two to ten). Settings includes "chips" (player start chips count) and "blindes" parameters.

```python
>>> from thpoker.game import Game, Player

>>> game = Game(
...     {"chips": 1000, "blindes": [10, 20]},
...     Player("qwerty"),
...     Player("asdfgh"),
...     Player("zxcvbn"),
... )

>>> context = game.new_round()
>>> context
{
    'success': True,
    'description': 'Redy to accept action.',
    'point': 'action_needed',
    'last_action': {
        'identifier': 'qwerty',
        'kind': 'blind_bet',
        'bet': 20
    },
    'state': 'normal',
    'table': [],
    'stage': {
        'name': 'pre_flop',
        'depth': 0
    },
    'bank': 30,
    'result': None,
    'current_player': 'asdfgh',
    'players': {
        'asdfgh': {
            'chips': 1000,
            'stage_bets': 0,
            'round_bets': 0,
            'dif': 20,
            'abilities': {
                'raise': {
                    'min': 21,
                    'max': 1000
                },
                'call': 20,
                'check': False
            },
            'cards': [2♥, 2♠],
            'hand_type': '22',
            'combo': None,
            'last_action': None
        },
        'zxcvbn': {
            'chips': 990,
            'stage_bets': 10,
            'round_bets': 10,
            'cards': [8♣, 5♦],
            'hand_type': '85o',
            'combo': None,
            'last_action': {
                'kind': 'blind_bet',
                'bet': 10
            }
        },
        'qwerty': {
            'chips': 980,
            'stage_bets': 20,
            'round_bets': 20,
            'cards': [7♥, 5♥],
            'hand_type': '75s',
            'combo': None,
            'last_action': {
                'kind': 'blind_bet',
                'bet': 20
            }
        }
    }
}
>>> context["point"] == Game.ACTION_NEEDED
True
>>> context["state"] == Game.NORMAL
True
>>> context["stage"]["name"] == Game.Stage.PRE_FLOP
True
>>> context["last_action"]["kind"] == Player.Action.BLIND_BET
True

>>> game.action(Player.Action.RAISE, 60)
{
    'success': True,
    'description': 'Redy to accept action.',
    'point': 'action_needed',
    'last_action': {
        'identifier': 'asdfgh',
        'kind': 'raise',
        'bet': 60
    },
    'state': 'normal',
    'table': [],
    'stage': {
        'name': 'pre_flop',
        'depth': 0
    },
    'bank': 90,
    'result': None,
    'current_player': 'zxcvbn',
    'players': {
        'asdfgh': {
            'chips': 940,
            'stage_bets': 60,
            'round_bets': 60,
            'cards': [2♥, 2♠],
            'hand_type': '22',
            'combo': None,
            'last_action': {
                'kind': 'raise',
                'bet': 60
            }
        },
        'zxcvbn': {
            'chips': 990,
            'stage_bets': 10,
            'round_bets': 10,
            'dif': 50,
            'abilities': {
                'raise': {
                    'min': 51,
                    'max': 990
                },
                'call': 50,
                'check': False
            },
            'cards': [8♣, 5♦],
            'hand_type': '85o',
            'combo': None,
            'last_action': {
                'kind': 'blind_bet',
                'bet': 10
            }
        },
        'qwerty': {
            'chips': 980,
            'stage_bets': 20,
            'round_bets': 20,
            'cards': [7♥, 5♥],
            'hand_type': '75s',
            'combo': None,
            'last_action': {
                'kind': 'blind_bet',
                'bet': 20
            }
        }
    }
}

>>> game.action(Player.Action.FOLD)
{
    'success': True,
    'description': 'Redy to accept action.',
    'point': 'action_needed',
    'last_action': {
        'identifier': 'zxcvbn',
        'kind': 'fold',
        'bet': 0
    },
    'state': 'normal',
    'table': [],
    'stage': {
        'name': 'pre_flop',
        'depth': 0
    },
    'bank': 90,
    'result': None,
    'current_player': 'qwerty',
    'players': {
        'asdfgh': {
            'chips': 940,
            'stage_bets': 60,
            'round_bets': 60,
            'cards': [2♥, 2♠],
            'hand_type': '22',
            'combo': None,
            'last_action': {
                'kind': 'raise',
                'bet': 60
            }
        },
        'zxcvbn': {
            'chips': 990,
            'stage_bets': 10,
            'round_bets': 10,
            'cards': [8♣, 5♦],
            'hand_type': '85o',
            'combo': None,
            'last_action': {
                'kind': 'fold',
                'bet': 0
            }
        },
        'qwerty': {
            'chips': 980,
            'stage_bets': 20,
            'round_bets': 20,
            'dif': 40,
            'abilities': {
                'raise': {
                    'min': 41,
                    'max': 980
                },
                'call': 40,
                'check': False
            },
            'cards': [7♥, 5♥],
            'hand_type': '75s',
            'combo': None,
            'last_action': {
                'kind': 'blind_bet',
                'bet': 20
            }
        }
    }
}

>>> game.action(Player.Action.CALL)
{
    'success': True,
    'description': 'Redy to start new stage.',
    'point': 'stage_needed',
    'last_action': {
        'identifier': 'qwerty',
        'kind': 'call',
        'bet': 40
    },
    'state': 'normal',
    'table': [],
    'stage': {
        'name': 'pre_flop',
        'depth': 0
    },
    'bank': 130,
    'result': None,
    'players': {
        'asdfgh': {
            'chips': 940,
            'stage_bets': 60,
            'round_bets': 60,
            'cards': [2♥, 2♠],
            'hand_type': '22',
            'combo': None,
            'last_action': {
                'kind': 'raise',
                'bet': 60
            }
        },
        'zxcvbn': {
            'chips': 990,
            'stage_bets': 10,
            'round_bets': 10,
            'cards': [8♣, 5♦],
            'hand_type': '85o',
            'combo': None,
            'last_action': {
                'kind': 'fold',
                'bet': 0
            }
        },
        'qwerty': {
            'chips': 940,
            'stage_bets': 60,
            'round_bets': 60,
            'cards': [7♥, 5♥],
            'hand_type': '75s',
            'combo': None,
            'last_action': {
                'kind': 'call',
                'bet': 40
            }
        }
    }
}

>>> game.new_stage()
{
    'success': True,
    'description': 'Redy to accept action.',
    'point': 'action_needed',
    'last_action': {
        'identifier': 'qwerty',
        'kind': 'call',
        'bet': 40
    },
    'state': 'normal',
    'table': [T♠, 8♠, J♦],
    'stage': {
        'name': 'flop',
        'depth': 0
    },
    'bank': 130,
    'result': None,
    'current_player': 'asdfgh',
    'players': {
        'asdfgh': {
            'chips': 940,
            'stage_bets': 0,
            'round_bets': 60,
            'dif': 0,
            'abilities': {
                'raise': {
                    'min': 1,
                    'max': 940
                },
                'call': 0,
                'check': True
            },
            'cards': [2♥, 2♠],
            'hand_type': '22',
            'combo': None,
            'last_action': None
        },
        'zxcvbn': {
            'chips': 990,
            'stage_bets': 0,
            'round_bets': 10,
            'cards': [8♣, 5♦],
            'hand_type': '85o',
            'combo': None,
            'last_action': None
        },
        'qwerty': {
            'chips': 940,
            'stage_bets': 0,
            'round_bets': 60,
            'cards': [7♥, 5♥],
            'hand_type': '75s',
            'combo': None,
            'last_action': None
        }
    }
}

>>> game.action(Player.Action.CHECK)
{
    'success': True,
    'description': 'Redy to accept action.',
    'point': 'action_needed',
    'last_action': {
        'identifier': 'asdfgh',
        'kind': 'check',
        'bet': 0
    },
    'state': 'normal',
    'table': [T♠, 8♠, J♦],
    'stage': {
        'name': 'flop',
        'depth': 0
    },
    'bank': 130,
    'result': None,
    'current_player': 'qwerty',
    'players': {
        'asdfgh': {
            'chips': 940,
            'stage_bets': 0,
            'round_bets': 60,
            'cards': [2♥, 2♠],
            'hand_type': '22',
            'combo': None,
            'last_action': {
                'kind': 'check',
                'bet': 0
            }
        },
        'zxcvbn': {
            'chips': 990,
            'stage_bets': 0,
            'round_bets': 10,
            'cards': [8♣, 5♦],
            'hand_type': '85o',
            'combo': None,
            'last_action': None
        },
        'qwerty': {
            'chips': 940,
            'stage_bets': 0,
            'round_bets': 60,
            'dif': 0,
            'abilities': {
                'raise': {
                    'min': 1,
                    'max': 940
                },
                'call': 0,
                'check': True
            },
            'cards': [7♥, 5♥],
            'hand_type': '75s',
            'combo': None,
            'last_action': None
        }
    }
}

>>> game.action(Player.Action.RAISE, 100)
{
    'success': True,
    'description': 'Redy to accept action.',
    'point': 'action_needed',
    'last_action': {
        'identifier': 'qwerty',
        'kind': 'raise',
        'bet': 100
    },
    'state': 'normal',
    'table': [T♠, 8♠, J♦],
    'stage': {
        'name': 'flop',
        'depth': 1
    },
    'bank': 230,
    'result': None,
    'current_player': 'asdfgh',
    'players': {
        'asdfgh': {
            'chips': 940,
            'stage_bets': 0,
            'round_bets': 60,
            'dif': 100,
            'abilities': {
                'raise': {
                    'min': 101,
                    'max': 940
                },
                'call': 100,
                'check': False
            },
            'cards': [2♥, 2♠],
            'hand_type': '22',
            'combo': None,
            'last_action': {
                'kind': 'check',
                'bet': 0
            }
        },
        'zxcvbn': {
            'chips': 990,
            'stage_bets': 0,
            'round_bets': 10,
            'cards': [8♣, 5♦],
            'hand_type': '85o',
            'combo': None,
            'last_action': None
        },
        'qwerty': {
            'chips': 840,
            'stage_bets': 100,
            'round_bets': 160,
            'cards': [7♥, 5♥],
            'hand_type': '75s',
            'combo': None,
            'last_action': {
                'kind': 'raise',
                'bet': 100
            }
        }
    }
}

>>> game.action(Player.Action.FOLD)
{
    'success': True,
    'description': 'Redy to start new round.',
    'point': 'round_needed',
    'last_action': {
        'identifier': 'asdfgh',
        'kind': 'fold',
        'bet': 0
    },
    'state': 'fold',
    'table': [T♠, 8♠, J♦],
    'stage': {
        'name': 'flop',
        'depth': 1
    },
    'bank': 230,
    'result': {
        'winners': {
            'qwerty': 230
        },
        'loosers': {
            'zxcvbn': 10,
            'asdfgh': 60
        }
    },
    'players': {
        'asdfgh': {
            'chips': 940,
            'stage_bets': 0,
            'round_bets': 60,
            'cards': [2♥, 2♠],
            'hand_type': '22',
            'combo': None,
            'last_action': {
                'kind': 'fold',
                'bet': 0
            }
        },
        'zxcvbn': {
            'chips': 990,
            'stage_bets': 0,
            'round_bets': 10,
            'cards': [8♣, 5♦],
            'hand_type': '85o',
            'combo': None,
            'last_action': None
        },
        'qwerty': {
            'chips': 1070,
            'stage_bets': 100,
            'round_bets': 160,
            'cards': [7♥, 5♥],
            'hand_type': '75s',
            'combo': None,
            'last_action': {
                'kind': 'raise',
                'bet': 100
            }
        }
    }
}

>>> game.new_round()
{
    'success': True,
    'description': 'Redy to accept action.',
    'point': 'action_needed',
    'last_action': {
        'identifier': 'asdfgh',
        'kind': 'blind_bet',
        'bet': 20
    },
    'state': 'normal',
    'table': [],
    'stage': {
        'name': 'pre_flop',
        'depth': 0
    },
    'bank': 30,
    'result': None,
    'current_player': 'zxcvbn',
    'players': {
        'zxcvbn': {
            'chips': 990,
            'stage_bets': 0,
            'round_bets': 0,
            'dif': 20,
            'abilities': {
                'raise': {
                    'min': 21,
                    'max': 990
                },
                'call': 20,
                'check': False
            },
            'cards': [3♠, 3♥],
            'hand_type': '33',
            'combo': None,
            'last_action': None
        },
        'qwerty': {
            'chips': 1060,
            'stage_bets': 10,
            'round_bets': 10,
            'cards': [J♣, 7♠],
            'hand_type': 'J7o',
            'combo': None,
            'last_action': {
                'kind': 'blind_bet',
                'bet': 10
            }
        },
        'asdfgh': {
            'chips': 920,
            'stage_bets': 20,
            'round_bets': 20,
            'cards': [K♣, 6♣],
            'hand_type': 'K6s',
            'combo': None,
            'last_action': {
                'kind': 'blind_bet',
                'bet': 20
            }
        }
    }
}

>>> #and so forth
```

## License
[Apache License](https://choosealicense.com/licenses/apache-2.0/)
