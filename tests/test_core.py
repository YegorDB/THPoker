# Copyright 2018-2021 Yegor Bitensky

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

from thpoker.core import Cards, Table, Hand, Combo

from utils import get_parameters


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
        {'table': 'As/Ks/Qs', 'hand': 'Js/Ts', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('As/Ks/Qs/Js/Ts').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': 'Ks/Js/Ts/9s', 'hand': 'Qd/Qs', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('Ks/Qs/Js/Ts/9s').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': 'Qs/Js/Ts/9s/8s', 'hand': 'Tc/2c', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('Qs/Js/Ts/9s/8s').items, 'ratio_value': Combo.Ratio.MISS},
        {'table': 'Qh/Js/Ts/9s/7s', 'hand': '8s/7h', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('Js/Ts/9s/8s/7s').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': 'Ts/9s/8s/7s/5d', 'hand': 'Ac/6s', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('Ts/9s/8s/7s/6s').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': '9s/8s/7s/6s/5s', 'hand': '5d/7h', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('9s/8s/7s/6s/5s').items, 'ratio_value': Combo.Ratio.MISS},
        {'table': 'Qc/7s/6s/4s/2h', 'hand': '8s/5s', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('8s/7s/6s/5s/4s').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': 'Ah/7s/5s/4s/3s', 'hand': '6s/2h', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('7s/6s/5s/4s/3s').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': '6s/5s/4s/3s/2s', 'hand': 'Js/Ts', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('6s/5s/4s/3s/2s').items, 'ratio_value': Combo.Ratio.MISS},
        {'table': 'Ac/5s/4s/3s/2s', 'hand': 'As/6d', 'combo_type': Combo.STRAIGHT_FLUSH, 'cards_items': Cards('5s/4s/3s/2s/1s').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': 'Ks/Kh/Kc', 'hand': 'As/Kd', 'combo_type': Combo.FOUR_OF_A_KIND, 'cards_items': Cards('Ks/Kd/Kh/Kc/As').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': 'Qs/Qd/Qh/Qc', 'hand': 'Ks/As', 'combo_type': Combo.FOUR_OF_A_KIND, 'cards_items': Cards('Qs/Qd/Qh/Qc/As').items, 'ratio_value': Combo.Ratio.MISS},
        {'table': 'Js/Ks/Jd/Kd/Jh', 'hand': 'Kh/Jc', 'combo_type': Combo.FOUR_OF_A_KIND, 'cards_items': Cards('Js/Jd/Jc/Jh/Ks').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': 'Ts/Th/Tc/Td/Jh', 'hand': 'As/5d', 'combo_type': Combo.FOUR_OF_A_KIND, 'cards_items': Cards('Ts/Th/Tc/Td/As').items, 'ratio_value': Combo.Ratio.MISS},
        {'table': 'As/Ad/Ah', 'hand': 'Kc/Kd', 'combo_type': Combo.FULL_HOUSE, 'cards_items': Cards('As/Ad/Ah/Kc/Kd').items, 'ratio_value': Combo.Ratio.HALF},
        {'table': 'As/Kc/Qd/Qh', 'hand': 'Kd/Qs', 'combo_type': Combo.FULL_HOUSE, 'cards_items': Cards('Qs/Qd/Qh/Kc/Kd').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': 'Kc/Js/Jd/Kd/Jh', 'hand': 'Ks/5d', 'combo_type': Combo.FULL_HOUSE, 'cards_items': Cards('Kc/Kd/Ks/Js/Jd').items, 'ratio_value': Combo.Ratio.HALF},
        {'table': 'Tc/Js/Jd/Td/Ts', 'hand': '8h/8d', 'combo_type': Combo.FULL_HOUSE, 'cards_items': Cards('Tc/Td/Ts/Js/Jd').items, 'ratio_value': Combo.Ratio.MISS},
        {'table': 'Js/5c/Jd/Jh/5s', 'hand': '9d/5d', 'combo_type': Combo.FULL_HOUSE, 'cards_items': Cards('Js/Jd/Jh/5c/5s').items, 'ratio_value': Combo.Ratio.HALF},
        {'table': 'As/Ks/9s', 'hand': 'Qs/Js', 'combo_type': Combo.FLUSH, 'cards_items': Cards('As/Ks/Qs/Js/9s').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': 'Ts/9s/5s/2s', 'hand': 'Ah/Ks', 'combo_type': Combo.FLUSH, 'cards_items': Cards('Ks/Ts/9s/5s/2s').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': 'Ts/9s/7s/5s/2s', 'hand': 'Kd/7h', 'combo_type': Combo.FLUSH, 'cards_items': Cards('Ts/9s/7s/5s/2s').items, 'ratio_value': Combo.Ratio.MISS},
        {'table': '9s/8s/7s/5s/4s', 'hand': '3s/2s', 'combo_type': Combo.FLUSH, 'cards_items': Cards('9s/8s/7s/5s/4s').items, 'ratio_value': Combo.Ratio.MISS},
        {'table': '7s/5s/4s/3s/2s', 'hand': 'Qh/2c', 'combo_type': Combo.FLUSH, 'cards_items': Cards('7s/5s/4s/3s/2s').items, 'ratio_value': Combo.Ratio.MISS},
        {'table': 'As/Kh/Qc', 'hand': 'Jd/Th', 'combo_type': Combo.STRAIGHT, 'cards_items': Cards('As/Kh/Qc/Jd/Th').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': 'Qc/Jd/Ts/8c', 'hand': 'Th/9s', 'combo_type': Combo.STRAIGHT, 'cards_items': Cards('Qc/Jd/Ts/9s/8c').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': 'Ts/9s/8c/7d/6s', 'hand': '5s/2h', 'combo_type': Combo.STRAIGHT, 'cards_items': Cards('Ts/9s/8c/7d/6s').items, 'ratio_value': Combo.Ratio.MISS},
        {'table': '8c/7d/4c/3d/2h', 'hand': '6h/5s', 'combo_type': Combo.STRAIGHT, 'cards_items': Cards('8c/7d/6h/5s/4c').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': '6s/5c/4d/3c/2h', 'hand': 'Js/Jh', 'combo_type': Combo.STRAIGHT, 'cards_items': Cards('6s/5c/4d/3c/2h').items, 'ratio_value': Combo.Ratio.MISS},
        {'table': 'Ac/5c/2h', 'hand': '4d/3c', 'combo_type': Combo.STRAIGHT, 'cards_items': Cards('5c/4d/3c/2h/1c').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': 'Ad/Qs/Qh', 'hand': 'Qc/7d', 'combo_type': Combo.THREE_OF_A_KIND, 'cards_items': Cards('Qs/Qh/Qc/Ad/7d').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': 'Js/Jh/Jc/9d', 'hand': 'Kd/Qd', 'combo_type': Combo.THREE_OF_A_KIND, 'cards_items': Cards('Js/Jh/Jc/Kd/Qd').items, 'ratio_value': Combo.Ratio.MISS},
        {'table': '7s/3s/3h/3c/2d', 'hand': '5d/4d', 'combo_type': Combo.THREE_OF_A_KIND, 'cards_items': Cards('3s/3h/3c/7s/5d').items, 'ratio_value': Combo.Ratio.MISS},
        {'table': 'Ad/Kc/Kh', 'hand': 'Qh/Qd', 'combo_type': Combo.TWO_PAIRS, 'cards_items': Cards('Kc/Kh/Qh/Qd/Ad').items, 'ratio_value': Combo.Ratio.HALF},
        {'table': 'Kd/Jc/Tc/9d', 'hand': 'Jh/9h', 'combo_type': Combo.TWO_PAIRS, 'cards_items': Cards('Jc/Jh/9h/9d/Kd').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': 'Tc/Ts/7s/5c/5h', 'hand': '9h/9d', 'combo_type': Combo.TWO_PAIRS, 'cards_items': Cards('Tc/Ts/9h/9d/7s').items, 'ratio_value': Combo.Ratio.HALF},
        {'table': '5c/5h/4h/4d/2s', 'hand': '3c/3s', 'combo_type': Combo.TWO_PAIRS, 'cards_items': Cards('5c/5h/4h/4d/3c').items, 'ratio_value': Combo.Ratio.MISS},
        {'table': 'Jh/Jd/Ts', 'hand': 'Ks/Qd', 'combo_type': Combo.ONE_PAIR, 'cards_items': Cards('Jh/Jd/Ks/Qd/Ts').items, 'ratio_value': Combo.Ratio.MISS},
        {'table': 'Ah/Jd/8c/6h', 'hand': 'Ts/8h', 'combo_type': Combo.ONE_PAIR, 'cards_items': Cards('8h/8c/Ah/Jd/Ts').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': 'Kc/Qh/Jd/5c/5h', 'hand': 'Ts/6h', 'combo_type': Combo.ONE_PAIR, 'cards_items': Cards('5c/5h/Kc/Qh/Jd').items, 'ratio_value': Combo.Ratio.MISS},
        {'table': 'Ks/Td/8h', 'hand': '6h/2c', 'combo_type': Combo.HIGH_CARD, 'cards_items': Cards('Ks/Td/8h/6h/2c').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': 'Ts/9h/4h/3c', 'hand': '7d/5s', 'combo_type': Combo.HIGH_CARD, 'cards_items': Cards('Ts/9h/7d/5s/4h').items, 'ratio_value': Combo.Ratio.REAL},
        {'table': 'Ks/Qd/9s/7h/5d', 'hand': '2h/4c', 'combo_type': Combo.HIGH_CARD, 'cards_items': Cards('Ks/Qd/9s/7h/5d').items, 'ratio_value': Combo.Ratio.MISS},
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
        assert not combo.ratio.is_checked

    @pytest.mark.parametrize("values", combo_variants)
    @get_parameters
    def test_cards_result(self, init_cards, combo_type, cards_items):
        combo = Combo(cards=Cards(init_cards))
        assert combo.type == combo_type
        assert combo.cards.items == cards_items
        assert not combo.ratio.is_checked

    @pytest.mark.parametrize("values", with_hand_variants)
    @get_parameters
    def test_table_hand_nominal_result(self, table, hand, combo_type, cards_items, ratio_value):
        combo = Combo(table=Table(table), hand=Hand(hand), ratio_check=True)
        assert combo.type == combo_type
        assert combo.cards.items == cards_items
        assert combo.ratio._value == ratio_value
        assert combo.ratio.is_checked

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
