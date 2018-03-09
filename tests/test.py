# Copyright 2018 Yegor Bitensky

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import pytest

from core import Card, Deck, Cards, Table, Hand, Combo
from hardcore import card, cards, combo, ccombo, hcombo, chcombo
from exceptions import CardWeightSymbolError, CardSuitSymbolError, CardEmptySymbolError, DeckCountTypeError, DeckCountNumberError, \
    CardsStringTypeError


def get_parameters(func):
    def wrap(self, values):
        return func(self, **values)
    return wrap


class TestCard:
    def test_validation(self):
        with pytest.raises(CardWeightSymbolError):
            Card("Xd")
        with pytest.raises(CardSuitSymbolError):
            Card("Ty")
        with pytest.raises(CardSuitSymbolError):
            Card("0")
        with pytest.raises(CardSuitSymbolError):
            Card("")
        with pytest.raises(CardEmptySymbolError):
            Card()

    def test_name(self):
        assert Card("Td").name == "Ten of diamonds"
        assert Card("2h").name == "Two of hearts"
        assert Card("A").name == "Ace"
        assert Card("7").name == "Seven"
        assert Card("c").name == "clubs"
        assert Card("s").name == "spades"

    def test_comparative(self):
        assert Card("Ks") == Card("Kc")
        assert Card("6d") != Card("Ts")
        assert Card("8h") == Card("8")
        assert Card("4") != Card("Q")
        assert Card("Jd") > Card("5s")
        assert Card("3h") < Card("7c")
        assert Card("2") < Card("A")
        assert Card("9") > Card("3")
        assert Card("Ac") == Card("c")
        assert Card("5d") != Card("s")


class TestDeck:
    def test_validation(self):
        with pytest.raises(DeckCountTypeError):
            list(Deck().push_cards("3"))
        with pytest.raises(DeckCountNumberError):
            list(Deck().push_cards(53))

    def test_count(self):
        assert len(Deck().cards) == 52
        assert len(list(Deck().push_cards(2))) == 2


class TestCards:
    def test_validation(self):
        with pytest.raises(CardsStringTypeError):
            Cards(123)

    def test_items(self):
        assert Cards().items == []
        assert Cards("As/Ac/Ah/Ad").items == [Card("As"), Card("Ac"), Card("Ah"), Card("Ad")]

    def test_contains(self):
        assert Card('Ks') in Cards("As/Ks/Qs/Js/Ts")
        assert not Card('8h') in Cards("As/Ks/Qs/Js/Ts")

    def test_cards_count(self):
        deck = Deck()
        cards = Cards()
        cards.get_cards(deck, 3)
        assert len(cards.items) == 3


class TestHand:
    def test_type(self):
        assert Hand("Kd/8s").type == "K8o"
        assert Hand("Tc/4c").type == "T4s"
        assert Hand("3d/3h").type == "33"

    def test_is_pair(self):
        assert Hand("Qs/Qc").is_pair
        assert not Hand("Ad/6h").is_pair


class TestCombo:
    combo_variants = [
        {'init_cards': 'As/Ks/Qs/Js/Ts', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('As/Ks/Qs/Js/Ts').items},
        {'init_cards': 'Ks/Qd/Qs/Js/Ts/9s', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('Ks/Qs/Js/Ts/9s').items},
        {'init_cards': 'Qs/Js/Tc/Ts/9s/8s/2c', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('Qs/Js/Ts/9s/8s').items},
        {'init_cards': 'Qh/Js/Ts/9s/8s/7h/7s', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('Js/Ts/9s/8s/7s').items},
        {'init_cards': 'Ac/Ts/9s/8s/7s/6s/5d', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('Ts/9s/8s/7s/6s').items},
        {'init_cards': '9s/8s/7s/7h/6s/5d/5s', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('9s/8s/7s/6s/5s').items},
        {'init_cards': 'Qc/8s/7s/6s/5s/4s/2h', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('8s/7s/6s/5s/4s').items},
        {'init_cards': 'Ah/7s/6s/5s/4s/3s/2h', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('7s/6s/5s/4s/3s').items},
        {'init_cards': 'Js/Ts/6s/5s/4s/3s/2s', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('6s/5s/4s/3s/2s').items},
        {'init_cards': 'Ac/As/6d/5s/4s/3s/2s', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('5s/4s/3s/2s/1s').items},
        {'init_cards': 'As/Ad/Ah/Ac', 'combo_type': Combo.FOUR_OF_A_KIND, 'cards_items': Cards('As/Ad/Ah/Ac').items},
        {'init_cards': 'Ks/As/Kd/Kh/Kc', 'combo_type': Combo.FOUR_OF_A_KIND, 'cards_items': Cards('Ks/Kd/Kh/Kc/As').items},
        {'init_cards': 'Qs/Ks/As/Qd/Qh/Qc', 'combo_type': Combo.FOUR_OF_A_KIND, 'cards_items': Cards('Qs/Qd/Qh/Qc/As').items},
        {'init_cards': 'Js/Ks/Jd/Kh/Jc/Kd/Jh', 'combo_type': Combo.FOUR_OF_A_KIND, 'cards_items': Cards('Js/Jd/Jc/Jh/Ks').items},
        {'init_cards': 'Ts/As/5d/Th/Tc/Td/Jh', 'combo_type': Combo.FOUR_OF_A_KIND, 'cards_items': Cards('Ts/Th/Tc/Td/As').items},
        {'init_cards': 'As/Ad/Ah/Kc/Kd', 'combo_type': Combo.FULL_HOUSE, 'cards_items': Cards('As/Ad/Ah/Kc/Kd').items},
        {'init_cards': 'As/Kc/Kd/Qs/Qd/Qh', 'combo_type': Combo.FULL_HOUSE, 'cards_items': Cards('Qs/Qd/Qh/Kc/Kd').items},
        {'init_cards': 'Kc/Js/Jd/Kd/Jh/Ks/5d', 'combo_type': Combo.FULL_HOUSE, 'cards_items': Cards('Kc/Kd/Ks/Js/Jd').items},
        {'init_cards': 'Tc/Js/Jd/Td/8h/Ts/8d', 'combo_type': Combo.FULL_HOUSE, 'cards_items': Cards('Tc/Td/Ts/Js/Jd').items},
        {'init_cards': 'Js/5c/Jd/9d/Jh/5s/5d', 'combo_type': Combo.FULL_HOUSE, 'cards_items': Cards('Js/Jd/Jh/5c/5s').items},
        {'init_cards': 'As/Ks/Qs/Js/9s', 'combo_type': Combo.FLUSH, 'cards_items': Cards('As/Ks/Qs/Js/9s').items},
        {'init_cards': 'Ah/Ks/Ts/9s/5s/2s', 'combo_type': Combo.FLUSH, 'cards_items': Cards('Ks/Ts/9s/5s/2s').items},
        {'init_cards': 'Kd/Ts/9s/7h/7s/5s/2s', 'combo_type': Combo.FLUSH, 'cards_items': Cards('Ts/9s/7s/5s/2s').items},
        {'init_cards': '9s/8s/7s/5s/4s/3s/2s', 'combo_type': Combo.FLUSH, 'cards_items': Cards('9s/8s/7s/5s/4s').items},
        {'init_cards': 'Qh/7s/5s/4s/3s/2s/2c', 'combo_type': Combo.FLUSH, 'cards_items': Cards('7s/5s/4s/3s/2s').items},
        {'init_cards': 'As/Kh/Qc/Jd/Th', 'combo_type': Combo.STRAIGHT, 'cards_items': Cards('As/Kh/Qc/Jd/Th').items},
        {'init_cards': 'Qc/Jd/Ts/Th/9s/8c', 'combo_type': Combo.STRAIGHT, 'cards_items': Cards('Qc/Jd/Ts/9s/8c').items},
        {'init_cards': 'Ts/9s/8c/7d/6s/5s/2h', 'combo_type': Combo.STRAIGHT, 'cards_items': Cards('Ts/9s/8c/7d/6s').items},
        {'init_cards': '8c/7d/6h/5s/4c/3d/2h', 'combo_type': Combo.STRAIGHT, 'cards_items': Cards('8c/7d/6h/5s/4c').items},
        {'init_cards': 'Js/Jh/6s/5c/4d/3c/2h', 'combo_type': Combo.STRAIGHT, 'cards_items': Cards('6s/5c/4d/3c/2h').items},
        {'init_cards': 'Ac/5c/4d/3c/2h', 'combo_type': Combo.STRAIGHT, 'cards_items': Cards('5c/4d/3c/2h/1c').items},
        {'init_cards': 'As/Ah/Ac', 'combo_type': Combo.THREE_OF_A_KIND, 'cards_items': Cards('As/Ah/Ac').items},
        {'init_cards': 'Ks/Kh/Kc/4d', 'combo_type': Combo.THREE_OF_A_KIND, 'cards_items': Cards('Ks/Kh/Kc/4d').items},
        {'init_cards': 'Ad/Qs/Qh/Qc/7d', 'combo_type': Combo.THREE_OF_A_KIND, 'cards_items': Cards('Qs/Qh/Qc/Ad/7d').items},
        {'init_cards': 'Kd/Qd/Js/Jh/Jc/9d', 'combo_type': Combo.THREE_OF_A_KIND, 'cards_items': Cards('Js/Jh/Jc/Kd/Qd').items},
        {'init_cards': '7s/5d/4d/3s/3h/3c/2d', 'combo_type': Combo.THREE_OF_A_KIND, 'cards_items': Cards('3s/3h/3c/7s/5d').items},
        {'init_cards': 'As/Ah/Kc/Kh', 'combo_type': Combo.TWO_PAIRS, 'cards_items': Cards('As/Ah/Kc/Kh').items},
        {'init_cards': 'Ad/Kc/Kh/Qh/Qd', 'combo_type': Combo.TWO_PAIRS, 'cards_items': Cards('Kc/Kh/Qh/Qd/Ad').items},
        {'init_cards': 'Kd/Jc/Jh/Tc/9h/9d', 'combo_type': Combo.TWO_PAIRS, 'cards_items': Cards('Jc/Jh/9h/9d/Kd').items},
        {'init_cards': 'Tc/Ts/9h/9d/7s/5c/5h', 'combo_type': Combo.TWO_PAIRS, 'cards_items': Cards('Tc/Ts/9h/9d/7s').items},
        {'init_cards': '5c/5h/4h/4d/3c/3s/2s', 'combo_type': Combo.TWO_PAIRS, 'cards_items': Cards('5c/5h/4h/4d/3c').items},
        {'init_cards': 'As/Kd/Kh', 'combo_type': Combo.ONE_PAIR, 'cards_items': Cards('Kd/Kh/As').items},
        {'init_cards': 'Ks/Qd/Jh/Jd/Ts', 'combo_type': Combo.ONE_PAIR, 'cards_items': Cards('Jh/Jd/Ks/Qd/Ts').items},
        {'init_cards': 'Ah/Jd/Ts/8h/8c/6h', 'combo_type': Combo.ONE_PAIR, 'cards_items': Cards('8h/8c/Ah/Jd/Ts').items},
        {'init_cards': 'Kc/Qh/Jd/Ts/6h/5c/5h', 'combo_type': Combo.ONE_PAIR, 'cards_items': Cards('5c/5h/Kc/Qh/Jd').items},
        {'init_cards': 'Qd/5h/3d', 'combo_type': Combo.HIGH_CARD, 'cards_items': Cards('Qd/5h/3d').items},
        {'init_cards': 'Jd/Th/9c/8s', 'combo_type': Combo.HIGH_CARD, 'cards_items': Cards('Jd/Th/9c/8s').items},
        {'init_cards': 'Ks/Td/8h/6h/2c', 'combo_type': Combo.HIGH_CARD, 'cards_items': Cards('Ks/Td/8h/6h/2c').items},
        {'init_cards': 'Ts/9h/7d/5s/4h/3c', 'combo_type': Combo.HIGH_CARD, 'cards_items': Cards('Ts/9h/7d/5s/4h').items},
        {'init_cards': 'Ks/Qd/9s/7h/5d/4c/2h', 'combo_type': Combo.HIGH_CARD, 'cards_items': Cards('Ks/Qd/9s/7h/5d').items},
    ]

    with_hand_variants = [
        {'table': 'As/Ks/Qs', 'hand': 'Js/Ts', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('As/Ks/Qs/Js/Ts').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': 'Ks/Js/Ts/9s', 'hand': 'Qd/Qs', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('Ks/Qs/Js/Ts/9s').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': 'Qs/Js/Ts/9s/8s', 'hand': 'Tc/2c', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('Qs/Js/Ts/9s/8s').items, 'is_real': False, 'is_nominal': True, 'is_half_nominal': False},
        {'table': 'Qh/Js/Ts/9s/7s', 'hand': '8s/7h', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('Js/Ts/9s/8s/7s').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': 'Ts/9s/8s/7s/5d', 'hand': 'Ac/6s', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('Ts/9s/8s/7s/6s').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': '9s/8s/7s/6s/5s', 'hand': '5d/7h', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('9s/8s/7s/6s/5s').items, 'is_real': False, 'is_nominal': True, 'is_half_nominal': False},
        {'table': 'Qc/7s/6s/4s/2h', 'hand': '8s/5s', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('8s/7s/6s/5s/4s').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': 'Ah/7s/5s/4s/3s', 'hand': '6s/2h', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('7s/6s/5s/4s/3s').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': '6s/5s/4s/3s/2s', 'hand': 'Js/Ts', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('6s/5s/4s/3s/2s').items, 'is_real': False, 'is_nominal': True, 'is_half_nominal': False},
        {'table': 'Ac/5s/4s/3s/2s', 'hand': 'As/6d', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('5s/4s/3s/2s/1s').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': 'Ks/Kh/Kc', 'hand': 'As/Kd', 'combo_type': Combo.FOUR_OF_A_KIND, 'cards_items': Cards('Ks/Kd/Kh/Kc/As').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': 'Qs/Qd/Qh/Qc', 'hand': 'Ks/As', 'combo_type': Combo.FOUR_OF_A_KIND, 'cards_items': Cards('Qs/Qd/Qh/Qc/As').items, 'is_real': False, 'is_nominal': True, 'is_half_nominal': False},
        {'table': 'Js/Ks/Jd/Kd/Jh', 'hand': 'Kh/Jc', 'combo_type': Combo.FOUR_OF_A_KIND, 'cards_items': Cards('Js/Jd/Jc/Jh/Ks').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': 'Ts/Th/Tc/Td/Jh', 'hand': 'As/5d', 'combo_type': Combo.FOUR_OF_A_KIND, 'cards_items': Cards('Ts/Th/Tc/Td/As').items, 'is_real': False, 'is_nominal': True, 'is_half_nominal': False},
        {'table': 'As/Ad/Ah', 'hand': 'Kc/Kd', 'combo_type': Combo.FULL_HOUSE, 'cards_items': Cards('As/Ad/Ah/Kc/Kd').items, 'is_real': False, 'is_nominal': False, 'is_half_nominal': True},
        {'table': 'As/Kc/Qd/Qh', 'hand': 'Kd/Qs', 'combo_type': Combo.FULL_HOUSE, 'cards_items': Cards('Qs/Qd/Qh/Kc/Kd').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': 'Kc/Js/Jd/Kd/Jh', 'hand': 'Ks/5d', 'combo_type': Combo.FULL_HOUSE, 'cards_items': Cards('Kc/Kd/Ks/Js/Jd').items, 'is_real': False, 'is_nominal': False, 'is_half_nominal': True},
        {'table': 'Tc/Js/Jd/Td/Ts', 'hand': '8h/8d', 'combo_type': Combo.FULL_HOUSE, 'cards_items': Cards('Tc/Td/Ts/Js/Jd').items, 'is_real': False, 'is_nominal': True, 'is_half_nominal': False},
        {'table': 'Js/5c/Jd/Jh/5s', 'hand': '9d/5d', 'combo_type': Combo.FULL_HOUSE, 'cards_items': Cards('Js/Jd/Jh/5c/5s').items, 'is_real': False, 'is_nominal': False, 'is_half_nominal': True},
        {'table': 'As/Ks/9s', 'hand': 'Qs/Js', 'combo_type': Combo.FLUSH, 'cards_items': Cards('As/Ks/Qs/Js/9s').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': 'Ts/9s/5s/2s', 'hand': 'Ah/Ks', 'combo_type': Combo.FLUSH, 'cards_items': Cards('Ks/Ts/9s/5s/2s').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': 'Ts/9s/7s/5s/2s', 'hand': 'Kd/7h', 'combo_type': Combo.FLUSH, 'cards_items': Cards('Ts/9s/7s/5s/2s').items, 'is_real': False, 'is_nominal': True, 'is_half_nominal': False},
        {'table': '9s/8s/7s/5s/4s', 'hand': '3s/2s', 'combo_type': Combo.FLUSH, 'cards_items': Cards('9s/8s/7s/5s/4s').items, 'is_real': False, 'is_nominal': True, 'is_half_nominal': False},
        {'table': '7s/5s/4s/3s/2s', 'hand': 'Qh/2c', 'combo_type': Combo.FLUSH, 'cards_items': Cards('7s/5s/4s/3s/2s').items, 'is_real': False, 'is_nominal': True, 'is_half_nominal': False},
        {'table': 'As/Kh/Qc', 'hand': 'Jd/Th', 'combo_type': Combo.STRAIGHT, 'cards_items': Cards('As/Kh/Qc/Jd/Th').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': 'Qc/Jd/Ts/8c', 'hand': 'Th/9s', 'combo_type': Combo.STRAIGHT, 'cards_items': Cards('Qc/Jd/Ts/9s/8c').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': 'Ts/9s/8c/7d/6s', 'hand': '5s/2h', 'combo_type': Combo.STRAIGHT, 'cards_items': Cards('Ts/9s/8c/7d/6s').items, 'is_real': False, 'is_nominal': True, 'is_half_nominal': False},
        {'table': '8c/7d/4c/3d/2h', 'hand': '6h/5s', 'combo_type': Combo.STRAIGHT, 'cards_items': Cards('8c/7d/6h/5s/4c').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': '6s/5c/4d/3c/2h', 'hand': 'Js/Jh', 'combo_type': Combo.STRAIGHT, 'cards_items': Cards('6s/5c/4d/3c/2h').items, 'is_real': False, 'is_nominal': True, 'is_half_nominal': False},
        {'table': 'Ac/5c/2h', 'hand': '4d/3c', 'combo_type': Combo.STRAIGHT, 'cards_items': Cards('5c/4d/3c/2h/1c').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': 'Ad/Qs/Qh', 'hand': 'Qc/7d', 'combo_type': Combo.THREE_OF_A_KIND, 'cards_items': Cards('Qs/Qh/Qc/Ad/7d').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': 'Js/Jh/Jc/9d', 'hand': 'Kd/Qd', 'combo_type': Combo.THREE_OF_A_KIND, 'cards_items': Cards('Js/Jh/Jc/Kd/Qd').items, 'is_real': False, 'is_nominal': True, 'is_half_nominal': False},
        {'table': '7s/3s/3h/3c/2d', 'hand': '5d/4d', 'combo_type': Combo.THREE_OF_A_KIND, 'cards_items': Cards('3s/3h/3c/7s/5d').items, 'is_real': False, 'is_nominal': True, 'is_half_nominal': False},
        {'table': 'Ad/Kc/Kh', 'hand': 'Qh/Qd', 'combo_type': Combo.TWO_PAIRS, 'cards_items': Cards('Kc/Kh/Qh/Qd/Ad').items, 'is_real': False, 'is_nominal': False, 'is_half_nominal': True},
        {'table': 'Kd/Jc/Tc/9d', 'hand': 'Jh/9h', 'combo_type': Combo.TWO_PAIRS, 'cards_items': Cards('Jc/Jh/9h/9d/Kd').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': 'Tc/Ts/7s/5c/5h', 'hand': '9h/9d', 'combo_type': Combo.TWO_PAIRS, 'cards_items': Cards('Tc/Ts/9h/9d/7s').items, 'is_real': False, 'is_nominal': False, 'is_half_nominal': True},
        {'table': '5c/5h/4h/4d/2s', 'hand': '3c/3s', 'combo_type': Combo.TWO_PAIRS, 'cards_items': Cards('5c/5h/4h/4d/3c').items, 'is_real': False, 'is_nominal': True, 'is_half_nominal': False},
        {'table': 'Jh/Jd/Ts', 'hand': 'Ks/Qd', 'combo_type': Combo.ONE_PAIR, 'cards_items': Cards('Jh/Jd/Ks/Qd/Ts').items, 'is_real': False, 'is_nominal': True, 'is_half_nominal': False},
        {'table': 'Ah/Jd/8c/6h', 'hand': 'Ts/8h', 'combo_type': Combo.ONE_PAIR, 'cards_items': Cards('8h/8c/Ah/Jd/Ts').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': 'Kc/Qh/Jd/5c/5h', 'hand': 'Ts/6h', 'combo_type': Combo.ONE_PAIR, 'cards_items': Cards('5c/5h/Kc/Qh/Jd').items, 'is_real': False, 'is_nominal': True, 'is_half_nominal': False},
        {'table': 'Ks/Td/8h', 'hand': '6h/2c', 'combo_type': Combo.HIGH_CARD, 'cards_items': Cards('Ks/Td/8h/6h/2c').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': 'Ts/9h/4h/3c', 'hand': '7d/5s', 'combo_type': Combo.HIGH_CARD, 'cards_items': Cards('Ts/9h/7d/5s/4h').items, 'is_real': True, 'is_nominal': False, 'is_half_nominal': False},
        {'table': 'Ks/Qd/9s/7h/5d', 'hand': '2h/4c', 'combo_type': Combo.HIGH_CARD, 'cards_items': Cards('Ks/Qd/9s/7h/5d').items, 'is_real': False, 'is_nominal': True, 'is_half_nominal': False},
    ]

    equal_values = [
        {'init_cards1': 'As/Ks/Qs/Js/Ts', 'init_cards2': 'Tc/Jc/Qc/Kc/Ac'},
        {'init_cards1': 'As/2s/3s/4s/5s', 'init_cards2': '5c/4c/3c/2c/Ac'},
        {'init_cards1': 'As/Ad/Ah/Ac/5d', 'init_cards2': '5c/Ac/Ah/Ad/As'},
        {'init_cards1': '6s/6d/6h/6c/Qd', 'init_cards2': 'Qc/6c/6h/6d/6s'},
        {'init_cards1': '3s/3d/7h/7c/7d', 'init_cards2': '7c/3c/7h/3d/7s'},
        {'init_cards1': 'Ts/Td/Th/Kc/Kd', 'init_cards2': 'Kc/Tc/Th/Td/Ks'},
        {'init_cards1': 'As/Js/8s/5s/2s', 'init_cards2': '2c/5c/8c/Jc/Ac'},
        {'init_cards1': 'Qs/Ts/8s/6s/4s', 'init_cards2': '4c/6c/8c/Tc/Qc'},
        {'init_cards1': 'As/Kh/Qc/Jd/Ts', 'init_cards2': 'Td/Jh/Qs/Kc/Ac'},
        {'init_cards1': 'Ac/2d/3s/4h/5s', 'init_cards2': '5c/4s/3h/2d/Ac'},
        {'init_cards1': 'Ac/Ad/As/9h/7s', 'init_cards2': '7c/As/Ah/Ad/9c'},
        {'init_cards1': '5c/5d/Js/Qh/5s', 'init_cards2': 'Jc/Qs/5h/5d/5c'},
        {'init_cards1': 'Kc/Kd/6s/6h/4s', 'init_cards2': '6c/6s/Kh/4d/Kc'},
        {'init_cards1': '8c/2d/Ts/2h/8s', 'init_cards2': 'Tc/2s/2h/8d/8c'},
        {'init_cards1': 'Jc/Jd/Ks/Qh/4s', 'init_cards2': 'Qc/4s/Kh/Jd/Jc'},
        {'init_cards1': '3c/5d/9s/3h/As', 'init_cards2': '9c/3s/Ah/3d/5c'},
        {'init_cards1': '7c/Jd/2s/9h/Ks', 'init_cards2': 'Kc/Js/9h/7d/2c'},
        {'init_cards1': '4c/Qd/Ts/6h/3s', 'init_cards2': '6c/Ts/4h/3d/Qc'},
    ]

    greater_values = [
        {'init_cards1': 'As/Ks/Qs/Js/Ts', 'init_cards2': '9c/Tc/Jc/Qc/Kc'},
        {'init_cards1': '2s/3s/4s/5s/6s', 'init_cards2': '5c/4c/3c/2c/Ac'},
        {'init_cards1': 'As/Ad/Ah/Ac/5d', 'init_cards2': '5c/Kc/Kh/Kd/Ks'},
        {'init_cards1': '6s/6d/6h/6c/Qd', 'init_cards2': 'Jc/6c/6h/6d/6s'},
        {'init_cards1': '3s/3d/7h/7c/7d', 'init_cards2': '7c/2c/7h/2d/7s'},
        {'init_cards1': 'Ts/Td/Th/Kc/Kd', 'init_cards2': 'Kc/9c/9h/9d/Ks'},
        {'init_cards1': 'As/Js/8s/5s/2s', 'init_cards2': '2c/5c/7c/Jc/Ac'},
        {'init_cards1': 'Qs/Ts/8s/6s/4s', 'init_cards2': '3c/6c/8c/Tc/Qc'},
        {'init_cards1': 'As/Kh/Qc/Jd/Ts', 'init_cards2': '9c/Td/Jh/Qs/Kc'},
        {'init_cards1': '2d/3s/4h/5s/6c', 'init_cards2': '5c/4s/3h/2d/Ac'},
        {'init_cards1': 'Ac/Ad/As/9h/7s', 'init_cards2': '7c/Ks/Kh/Kd/9c'},
        {'init_cards1': '5c/5d/Js/Qh/5s', 'init_cards2': 'Tc/Qs/5h/5d/5c'},
        {'init_cards1': 'Kc/Kd/6s/6h/4s', 'init_cards2': '6c/6s/Qh/4d/Qc'},
        {'init_cards1': '8c/2d/Ts/2h/8s', 'init_cards2': '9c/2s/2h/8d/8c'},
        {'init_cards1': 'Jc/Jd/Ks/Qh/4s', 'init_cards2': 'Qc/4s/Kh/Td/Tc'},
        {'init_cards1': '3c/5d/9s/3h/As', 'init_cards2': '9c/3s/Kh/3d/5c'},
        {'init_cards1': '7c/Jd/2s/9h/Ks', 'init_cards2': 'Kc/Js/8h/7d/2c'},
        {'init_cards1': '4c/Qd/Ts/6h/3s', 'init_cards2': '5c/Ts/4h/3d/Qc'},
    ]

    smaller_values = [
        {'init_cards1': 'Ks/Qs/Js/Ts/9s', 'init_cards2': 'Tc/Jc/Qc/Kc/Ac'},
        {'init_cards1': 'As/2s/3s/4s/5s', 'init_cards2': '6c/5c/4c/3c/2c'},
        {'init_cards1': '9s/9d/9h/9c/5d', 'init_cards2': '5c/Ac/Ah/Ad/As'},
        {'init_cards1': '6s/6d/6h/6c/4d', 'init_cards2': 'Qc/6c/6h/6d/6s'},
        {'init_cards1': '3s/3d/5h/5c/5d', 'init_cards2': '7c/3c/7h/3d/7s'},
        {'init_cards1': 'Ts/Td/Th/6c/6d', 'init_cards2': 'Kc/Tc/Th/Td/Ks'},
        {'init_cards1': 'As/Ts/8s/5s/2s', 'init_cards2': '2c/5c/8c/Jc/Ac'},
        {'init_cards1': 'Qs/Ts/7s/6s/4s', 'init_cards2': '4c/6c/8c/Tc/Qc'},
        {'init_cards1': 'Kh/Qc/Jd/Ts/9s', 'init_cards2': 'Td/Jh/Qs/Kc/Ac'},
        {'init_cards1': 'Ac/2d/3s/4h/5s', 'init_cards2': '6d/5c/4s/3h/2d'},
        {'init_cards1': '2c/2d/2s/9h/7s', 'init_cards2': '7c/As/Ah/Ad/9c'},
        {'init_cards1': '5c/5d/Js/8h/5s', 'init_cards2': 'Jc/Qs/5h/5d/5c'},
        {'init_cards1': 'Jc/Jd/6s/6h/4s', 'init_cards2': '6c/6s/Kh/4d/Kc'},
        {'init_cards1': '8c/2d/5s/2h/8s', 'init_cards2': 'Tc/2s/2h/8d/8c'},
        {'init_cards1': '7c/7d/Ks/Qh/4s', 'init_cards2': 'Qc/4s/Kh/Jd/Jc'},
        {'init_cards1': '3c/5d/9s/3h/4s', 'init_cards2': '9c/3s/Ah/3d/5c'},
        {'init_cards1': '7c/5d/2s/9h/Ks', 'init_cards2': 'Kc/Js/9h/7d/2c'},
        {'init_cards1': '4c/Qd/Ts/2h/3s', 'init_cards2': '6c/Ts/4h/3d/Qc'},
    ]

    @pytest.mark.parametrize("values", combo_variants)
    @get_parameters
    def test_cards_string_result(self, init_cards, combo_type, cards_items):
        combo = Combo(cards_string=init_cards)
        assert combo.type == combo_type
        assert combo.cards.items == cards_items

    @pytest.mark.parametrize("values", combo_variants)
    @get_parameters
    def test_cards_result(self, init_cards, combo_type, cards_items):
        combo = Combo(cards=Cards(init_cards))
        assert combo.type == combo_type
        assert combo.cards.items == cards_items

    @pytest.mark.parametrize("values", with_hand_variants)
    @get_parameters
    def test_table_hand_nominal_result(self, table, hand, combo_type, cards_items, is_real, is_nominal, is_half_nominal):
        combo = Combo(table=Table(table), hand=Hand(hand), nominal_check=True)
        assert combo.type == combo_type
        assert combo.cards.items == cards_items
        assert combo.is_real == is_real
        assert combo.is_nominal == is_nominal
        assert combo.is_half_nominal == is_half_nominal

    @pytest.mark.parametrize("values", equal_values)
    @get_parameters
    def test_cards_string_equal(self, init_cards1, init_cards2):
        assert Combo(cards_string=init_cards1) == Combo(cards_string=init_cards2)

    @pytest.mark.parametrize("values", equal_values)
    @get_parameters
    def test_cards_equal(self, init_cards1, init_cards2):
        assert Combo(cards=Cards(init_cards1)) == Combo(cards=Cards(init_cards2))

    @pytest.mark.parametrize("values", greater_values)
    @get_parameters
    def test_cards_string_greater(self, init_cards1, init_cards2):
        assert Combo(cards_string=init_cards1) > Combo(cards_string=init_cards2)

    @pytest.mark.parametrize("values", greater_values)
    @get_parameters
    def test_cards_greater(self, init_cards1, init_cards2):
        assert Combo(cards=Cards(init_cards1)) > Combo(cards=Cards(init_cards2))

    @pytest.mark.parametrize("values", smaller_values)
    @get_parameters
    def test_cards_string_smaller(self, init_cards1, init_cards2):
        assert Combo(cards_string=init_cards1) < Combo(cards_string=init_cards2)

    @pytest.mark.parametrize("values", smaller_values)
    @get_parameters
    def test_cards_smaller(self, init_cards1, init_cards2):
        assert Combo(cards=Cards(init_cards1)) < Combo(cards=Cards(init_cards2))


class TestHardCard:
    def test_create(self):
        assert card('As') == 144
        assert card('Jc') == 111
        assert card('7h') == 73
        assert card('2d') == 22


class TestHardCombo:
    combo_variants = [
        {'cards_string': 'As/Ks/Qs/Js/Ts', 'value': (9, 14)},
        {'cards_string': 'Ks/Qd/Qs/Js/Ts/9s', 'value': (9, 13)},
        {'cards_string': 'Qs/Js/Tc/Ts/9s/8s/2c', 'value': (9, 12)},
        {'cards_string': 'Qh/Js/Ts/9s/8s/7h/7s', 'value': (9, 11)},
        {'cards_string': 'Ac/Ts/9s/8s/7s/6s/5d', 'value': (9, 10)},
        {'cards_string': '9s/8s/7s/7h/6s/5d/5s', 'value': (9, 9)},
        {'cards_string': 'Qc/8s/7s/6s/5s/4s/2h', 'value': (9, 8)},
        {'cards_string': 'Ah/7s/6s/5s/4s/3s/2h', 'value': (9, 7)},
        {'cards_string': 'Js/Ts/6s/5s/4s/3s/2s', 'value': (9, 6)},
        {'cards_string': 'Ac/As/6d/5s/4s/3s/2s', 'value': (9, 5)},
        {'cards_string': 'As/Ad/Ah/Ac', 'value': (8, 14)},
        {'cards_string': 'Ks/As/Kd/Kh/Kc', 'value': (8, 13, 14)},
        {'cards_string': 'Qs/Ks/As/Qd/Qh/Qc', 'value': (8, 12, 14)},
        {'cards_string': 'Js/Ks/Jd/Kh/Jc/Kd/Jh', 'value': (8, 11, 13)},
        {'cards_string': 'Ts/As/5d/Th/Tc/Td/Jh', 'value': (8, 10, 14)},
        {'cards_string': 'As/Ad/Ah/Kc/Kd', 'value': (7, 14, 13)},
        {'cards_string': 'As/Kc/Kd/Qs/Qd/Qh', 'value': (7, 12, 13)},
        {'cards_string': 'Kc/Js/Jd/Kd/Jh/Ks/5d', 'value': (7, 13, 11)},
        {'cards_string': 'Tc/Js/Jd/Td/8h/Ts/8d', 'value': (7, 10, 11)},
        {'cards_string': 'Js/5c/Jd/9d/Jh/5s/5d', 'value': (7, 11, 5)},
        {'cards_string': 'As/Ks/Qs/Js/9s', 'value': (6, 14, 13, 12, 11, 9)},
        {'cards_string': 'Ah/Ks/Ts/9s/5s/2s', 'value': (6, 13, 10, 9, 5, 2)},
        {'cards_string': 'Kd/Ts/9s/7h/7s/5s/2s', 'value': (6, 10, 9, 7, 5, 2)},
        {'cards_string': '9s/8s/7s/5s/4s/3s/2s', 'value': (6, 9, 8, 7, 5, 4)},
        {'cards_string': 'Qh/7s/5s/4s/3s/2s/2c', 'value': (6, 7, 5, 4, 3, 2)},
        {'cards_string': 'As/Kh/Qc/Jd/Th', 'value': (5, 14)},
        {'cards_string': 'Qc/Jd/Ts/Th/9s/8c', 'value': (5, 12)},
        {'cards_string': 'Ts/9s/8c/7d/6s/5s/2h', 'value': (5, 10)},
        {'cards_string': '8c/7d/6h/5s/4c/3d/2h', 'value': (5, 8)},
        {'cards_string': 'Js/Jh/6s/5c/4d/3c/2h', 'value': (5, 6)},
        {'cards_string': 'Ac/5c/4d/3c/2h', 'value': (5, 5)},
        {'cards_string': 'As/Ah/Ac', 'value': (4, 14)},
        {'cards_string': 'Ks/Kh/Kc/4d', 'value': (4, 13, 4)},
        {'cards_string': 'Ad/Qs/Qh/Qc/7d', 'value': (4, 12, 14, 7)},
        {'cards_string': 'Kd/Qd/Js/Jh/Jc/9d', 'value': (4, 11, 13, 12)},
        {'cards_string': '7s/5d/4d/3s/3h/3c/2d', 'value': (4, 3, 7, 5)},
        {'cards_string': 'As/Ah/Kc/Kh', 'value': (3, 14, 13)},
        {'cards_string': 'Ad/Kc/Kh/Qh/Qd', 'value': (3, 13, 12, 14)},
        {'cards_string': 'Kd/Jc/Jh/Tc/9h/9d', 'value': (3, 11, 9, 13)},
        {'cards_string': 'Tc/Ts/9h/9d/7s/5c/5h', 'value': (3, 10, 9, 7)},
        {'cards_string': '5c/5h/4h/4d/3c/3s/2s', 'value': (3, 5, 4, 3)},
        {'cards_string': 'As/Ah', 'value': (2, 14)},
        {'cards_string': 'As/Kd/Kh', 'value': (2, 13, 14)},
        {'cards_string': 'Ks/Qd/Qh/Jd', 'value': (2, 12, 13, 11)},
        {'cards_string': 'Ks/Qd/Jh/Jd/Ts', 'value': (2, 11, 13, 12, 10)},
        {'cards_string': 'Ah/Jd/Ts/8h/8c/6h', 'value': (2, 8, 14, 11, 10)},
        {'cards_string': 'Kc/Qh/Jd/Ts/6h/5c/5h', 'value': (2, 5, 13, 12, 11)},
        {'cards_string': '4s', 'value': (1, 4)},
        {'cards_string': 'Ac/7d', 'value': (1, 14, 7)},
        {'cards_string': 'Qd/5h/3d', 'value': (1, 12, 5, 3)},
        {'cards_string': 'Jd/Th/9c/8s', 'value': (1, 11, 10, 9, 8)},
        {'cards_string': 'Ks/Td/8h/6h/2c', 'value': (1, 13, 10, 8, 6, 2)},
        {'cards_string': 'Ts/9h/7d/5s/4h/3c', 'value': (1, 10, 9, 7, 5, 4)},
        {'cards_string': 'Ks/Qd/9s/7h/5d/4c/2h', 'value': (1, 13, 12, 9, 7, 5)},
    ]

    with_hand_variants = [
        {'table': 'Js/Ts/9s/8s/2c', 'hand': 'Qs/Tc', 'kind': 2},
        {'table': 'Ts/9s/8s/7s/6s', 'hand': 'Ac/5d', 'kind': 0},
        {'table': 'Ks/Kd/Kh/Kc/7s', 'hand': 'As/2d', 'kind': 0},
        {'table': 'Ks/As/Qh/Qc/2d', 'hand': 'Qs/Qd', 'kind': 2},
        {'table': 'Jd/Kd/Jh/Ks/5d', 'hand': 'Kc/Js', 'kind': 2},
        {'table': 'Js/Jd/Td/Ts/8d', 'hand': 'Tc/8h', 'kind': 1},
        {'table': 'Js/5c/Jd/5s/5d', 'hand': '9d/Ks', 'kind': 0},
        {'table': '7s/5s/4s/3s/2s', 'hand': '9s/8s', 'kind': 2},
        {'table': '7s/5s/4s/3s/2s', 'hand': 'Qh/2c', 'kind': 0},
        {'table': '6h/5s/4c/3d/2h', 'hand': '8c/7d', 'kind': 2},
        {'table': '6s/5c/4d/3c/2h', 'hand': 'Js/Jh', 'kind': 0},
        {'table': 'Qd/Jh/Jc/9d/5d', 'hand': 'Kd/Js', 'kind': 2},
        {'table': '4d/3s/3h/3c/2d', 'hand': '7s/5d', 'kind': 0},
        {'table': 'Jh/Kd/Tc/9d/3s', 'hand': 'Jc/9h', 'kind': 2},
        {'table': 'Ts/9h/9d/7s/5h', 'hand': 'Tc/5c', 'kind': 1},
        {'table': '5c/5h/4h/4d/3c', 'hand': '3s/2s', 'kind': 0},
        {'table': 'Ah/Jd/Ts/6h/4h', 'hand': '8h/8c', 'kind': 2},
        {'table': 'Jd/Ts/6h/5c/5h', 'hand': 'Kc/Qh', 'kind': 0},
        {'table': 'Ks/Qd/9s/7h/2h', 'hand': '5d/4c', 'kind': 2},
        {'table': 'Ac/Ts/9h/7d/5s', 'hand': '4h/3c', 'kind': 0},
    ]

    @pytest.mark.parametrize("values", combo_variants)
    @get_parameters
    def test_hard_cards_string_combo(self, cards_string, value):
        assert combo(cards_string) == value

    @pytest.mark.parametrize("values", combo_variants)
    @get_parameters
    def test_hard_cards_combo(self, cards_string, value):
        assert ccombo(cards(cards_string)) == value

    @pytest.mark.parametrize("values", with_hand_variants)
    @get_parameters
    def test_hard_hand_string_combo(self, table, hand, kind):
        assert hcombo(table, hand)[1] == kind

    @pytest.mark.parametrize("values", with_hand_variants)
    @get_parameters
    def test_hard_hand_combo(self, table, hand, kind):
        assert chcombo(cards(table) + cards(hand, 1))[1] == kind
