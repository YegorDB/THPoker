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


from cthpoker import findCombo, findRatioCombo


all_weights = '23456789TJQKA'
all_suits = 'cdhs'
wght = {all_weights[i]: (i + 2) * 10 for i in range(13)}
suit = {all_suits[i]: (i + 1) for i in range(4)}


def hcard(sign):
    return wght[sign[0]] + suit[sign[1]]


def hdeck():
    return [hcard(w + s) for w in all_weights for s in all_suits]


def hcards(cards_string, in_hand=0):
    return [1000 * in_hand + hcard(sign) for sign in cards_string.split('/')]


def hcombo(cards_string):
    return findCombo(hcards(cards_string))


def chcombo(cards):
    return findCombo(cards)


def rhcombo(table, hand):
    return findRatioCombo(table + hand)
