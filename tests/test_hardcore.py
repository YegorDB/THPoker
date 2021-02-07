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

from thpoker.hardcore import hcard, hcards, hcombo, chcombo, rhcombo

from utils import get_parameters


class TestHardCard:
    def test_create(self):
        assert hcard('As') == 144
        assert hcard('Jc') == 111
        assert hcard('7h') == 73
        assert hcard('2d') == 22


class TestHardCombo:
    combo_variants = [
        {'cards_string': 'As/Ks/Qs/Js/Ts', 'value': [9, 14]},
        {'cards_string': 'Ks/Qd/Qs/Js/Ts/9s', 'value': [9, 13]},
        {'cards_string': 'Qs/Js/Tc/Ts/9s/8s/2c', 'value': [9, 12]},
        {'cards_string': 'Qh/Js/Ts/9s/8s/7h/7s', 'value': [9, 11]},
        {'cards_string': 'Ac/Ts/9s/8s/7s/6s/5d', 'value': [9, 10]},
        {'cards_string': '9s/8s/7s/7h/6s/5d/5s', 'value': [9, 9]},
        {'cards_string': 'Qc/8s/7s/6s/5s/4s/2h', 'value': [9, 8]},
        {'cards_string': 'Ah/7s/6s/5s/4s/3s/2h', 'value': [9, 7]},
        {'cards_string': 'Js/Ts/6s/5s/4s/3s/2s', 'value': [9, 6]},
        {'cards_string': 'Ac/As/6d/5s/4s/3s/2s', 'value': [9, 5]},
        {'cards_string': 'As/Ad/Ah/Ac', 'value': [8, 14]},
        {'cards_string': 'Ks/As/Kd/Kh/Kc', 'value': [8, 13, 14]},
        {'cards_string': 'Qs/Ks/As/Qd/Qh/Qc', 'value': [8, 12, 14]},
        {'cards_string': 'Js/Ks/Jd/Kh/Jc/Kd/Jh', 'value': [8, 11, 13]},
        {'cards_string': 'Ts/As/5d/Th/Tc/Td/Jh', 'value': [8, 10, 14]},
        {'cards_string': 'As/Ad/Ah/Kc/Kd', 'value': [7, 14, 13]},
        {'cards_string': 'As/Kc/Kd/Qs/Qd/Qh', 'value': [7, 12, 13]},
        {'cards_string': 'Kc/Js/Jd/Kd/Jh/Ks/5d', 'value': [7, 13, 11]},
        {'cards_string': 'Tc/Js/Jd/Td/8h/Ts/8d', 'value': [7, 10, 11]},
        {'cards_string': 'Js/5c/Jd/9d/Jh/5s/5d', 'value': [7, 11, 5]},
        {'cards_string': 'As/Ks/Qs/Js/9s', 'value': [6, 14, 13, 12, 11, 9]},
        {'cards_string': 'Ah/Ks/Ts/9s/5s/2s', 'value': [6, 13, 10, 9, 5, 2]},
        {'cards_string': 'Kd/Ts/9s/7h/7s/5s/2s', 'value': [6, 10, 9, 7, 5, 2]},
        {'cards_string': '9s/8s/7s/5s/4s/3s/2s', 'value': [6, 9, 8, 7, 5, 4]},
        {'cards_string': 'Qh/7s/5s/4s/3s/2s/2c', 'value': [6, 7, 5, 4, 3, 2]},
        {'cards_string': 'As/Kh/Qc/Jd/Th', 'value': [5, 14]},
        {'cards_string': 'Qc/Jd/Ts/Th/9s/8c', 'value': [5, 12]},
        {'cards_string': 'Ts/9s/8c/7d/6s/5s/2h', 'value': [5, 10]},
        {'cards_string': '8c/7d/6h/5s/4c/3d/2h', 'value': [5, 8]},
        {'cards_string': 'Js/Jh/6s/5c/4d/3c/2h', 'value': [5, 6]},
        {'cards_string': 'Ac/5c/4d/3c/2h', 'value': [5, 5]},
        {'cards_string': 'As/Ah/Ac', 'value': [4, 14]},
        {'cards_string': 'Ks/Kh/Kc/4d', 'value': [4, 13, 4]},
        {'cards_string': 'Ad/Qs/Qh/Qc/7d', 'value': [4, 12, 14, 7]},
        {'cards_string': 'Kd/Qd/Js/Jh/Jc/9d', 'value': [4, 11, 13, 12]},
        {'cards_string': '7s/5d/4d/3s/3h/3c/2d', 'value': [4, 3, 7, 5]},
        {'cards_string': 'As/Ah/Kc/Kh', 'value': [3, 14, 13]},
        {'cards_string': 'Ad/Kc/Kh/Qh/Qd', 'value': [3, 13, 12, 14]},
        {'cards_string': 'Kd/Jc/Jh/Tc/9h/9d', 'value': [3, 11, 9, 13]},
        {'cards_string': 'Tc/Ts/9h/9d/7s/5c/5h', 'value': [3, 10, 9, 7]},
        {'cards_string': '5c/5h/4h/4d/3c/3s/2s', 'value': [3, 5, 4, 3]},
        {'cards_string': 'As/Ah', 'value': [2, 14]},
        {'cards_string': 'As/Kd/Kh', 'value': [2, 13, 14]},
        {'cards_string': 'Ks/Qd/Qh/Jd', 'value': [2, 12, 13, 11]},
        {'cards_string': 'Ks/Qd/Jh/Jd/Ts', 'value': [2, 11, 13, 12, 10]},
        {'cards_string': 'Ah/Jd/Ts/8h/8c/6h', 'value': [2, 8, 14, 11, 10]},
        {'cards_string': 'Kc/Qh/Jd/Ts/6h/5c/5h', 'value': [2, 5, 13, 12, 11]},
        {'cards_string': '4s', 'value': [1, 4]},
        {'cards_string': 'Ac/7d', 'value': [1, 14, 7]},
        {'cards_string': 'Qd/5h/3d', 'value': [1, 12, 5, 3]},
        {'cards_string': 'Jd/Th/9c/8s', 'value': [1, 11, 10, 9, 8]},
        {'cards_string': 'Ks/Td/8h/6h/2c', 'value': [1, 13, 10, 8, 6, 2]},
        {'cards_string': 'Ts/9h/7d/5s/4h/3c', 'value': [1, 10, 9, 7, 5, 4]},
        {'cards_string': 'Ks/Qd/9s/7h/5d/4c/2h', 'value': [1, 13, 12, 9, 7, 5]},
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
        assert hcombo(cards_string) == value

    @pytest.mark.parametrize("values", combo_variants)
    @get_parameters
    def test_hard_cards_combo(self, cards_string, value):
        assert chcombo(hcards(cards_string)) == value

    @pytest.mark.parametrize("values", with_hand_variants)
    @get_parameters
    def test_hard_hand_combo(self, table, hand, kind):
        assert rhcombo(hcards(table), hcards(hand, True))[1] == kind
