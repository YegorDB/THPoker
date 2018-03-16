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

all_weights = '23456789TJQKA'
all_suits = 'cdhs'
wght = {all_weights[i]: (i + 2) * 10 for i in range(13)}
suit = {all_suits[i]: (i + 1) for i in range(4)}


def card(sign):
    return wght[sign[0]] + suit[sign[1]]


def new_deck():
    return [card(w + s) for w in all_weights for s in all_suits]


def cards(cards_string, in_hand=0):
    return [1000 * in_hand + card(sign) for sign in cards_string.split('/')]


def get_sf(weights, index):
    return (9, weights[index])


def get_fk(wr):
    del wr[0][wr[0].index(wr[4][0])]
    return (8, wr[4][0]) + tuple(wr[0][-1:])


def get_fh(wr):
    try:
        return (7, wr[3][-1], wr[2][-1])
    except KeyError:
        return (7, wr[3][-1], wr[3][-2])


def get_fl(weights):
    weights.reverse()
    return (6,) + tuple(weights)


def get_st(weights, index):
    return (5, weights[index])


def get_tk(wr):
    del wr[0][wr[0].index(wr[3][0])]
    wr[0].reverse()
    return (4, wr[3][0]) + tuple(wr[0][:2])


def get_tp(wr):
    del wr[0][wr[0].index(wr[2][-1])]
    del wr[0][wr[0].index(wr[2][-2])]
    return (3, wr[2][-1], wr[2][-2]) + tuple(wr[0][-1:])


def get_op(wr):
    del wr[0][wr[0].index(wr[2][0])]
    wr[0].reverse()
    return (2, wr[2][0]) + tuple(wr[0][:3])


def get_hc(wr):
    wr[0].reverse()
    return (1,) + tuple(wr[0][:5])


def repetitions(cards):
    wr = {0: []}  # weight repeats, 0 - all weights
    sr = {0: []}  # suit repeats, 0 - all suits
    a_wghts = [c // 10 for c in cards] # abstract weight cards
    a_suits = [c % 10 for c in cards] # abstract suit cards
    for (a_cards, rep) in ((a_wghts, wr), (a_suits, sr)):
        for c in a_cards:
            if c not in rep[0]:
                cnt = a_cards.count(c)
                try:
                    rep[cnt].append(c)
                except KeyError:
                    rep[cnt] = [c]
                rep[0].append(c)

    return wr, sr


def get_str_index(weights):
    if 14 in weights:  # add 1 if there are an Ace
        weights.insert(0, 1)

    rank = ['0'] * 14
    for w in weights:
        rank[w - 1] = '1'
    rank = ''.join(rank)

    if not '11111' in rank:
       return 0

    i = rank.rfind('11111')
    index = rank[:i].count('1') + 4
    return index


def find_combo(cards, nedded_data=False):
    cards.sort()

    value = 0
    str_index = 0
    weights = None
    wr, sr = repetitions(cards=cards)

    max_sr = max(sr)  # maximal suit repeats
    if max_sr < 5:
        if 4 in wr:
            value = get_fk(wr=wr)
        elif 3 in wr and 2 in wr or 3 in wr and len(wr[3]) == 2:
            value = get_fh(wr=wr)
        if not value:
            weights = wr[0][:]
            str_index = get_str_index(weights=weights)
            if str_index:
                value = get_st(weights, str_index)
            elif 3 in wr:
                value = get_tk(wr=wr)
            elif 2 in wr and len(wr[2]) > 1:
                value = get_tp(wr=wr)
            elif 2 in wr:
                value = get_op(wr=wr)
            else:
                value = get_hc(wr=wr)
    else:
        fl_suit = sr[max_sr][0]
        cards = list(filter(lambda c: c % 10 == fl_suit, cards))
        weights = [c // 10 for c in cards]
        str_index = get_str_index(weights=weights)
        value = get_sf(weights, str_index) if str_index else get_fl(weights=weights[-5:])

    if nedded_data:
        return (
            value,
            {
                'cards': cards,
                'str_index': str_index,
                'wr': wr,
                'weights': weights,
            },
        )

    return value


def combo(cards_string):
    return find_combo(cards(cards_string))


def ccombo(cards):
    return find_combo(cards)


def half_nominal_finder(cards, w1, w2):
    hits = 0
    for w in (w1, w2):
        for c in cards:
            if c // 1000 and c % 1000 // 10 == w:
                hits += 1
                break

    return hits


def repeat_nominal_finder(cards, w):
    for c in cards:
        if c // 1000 and c % 1000 // 10 == w:
            return 2
    
    return 0


def pure_nominal_finder(cards):
    for c in cards:
        if c // 1000:
            return 2

    return 0


def sequence_nominal_finder(cards, strt_wghts):
    for c in cards:
        if c // 1000 and c % 1000 // 10 in strt_wghts:
            return 2

    return 0


def get_sf_nominal(cards, strt_wghts):
    return sequence_nominal_finder(cards, strt_wghts)


def get_fk_nominal(cards, wr):
    return repeat_nominal_finder(cards, wr[4][0])


def get_fh_nominal(cards, wr):
    return half_nominal_finder(cards, wr[3][-1], wr[2][-1] if 2 in wr else wr[3][-2])


def get_fl_nominal(cards):
    return pure_nominal_finder(cards[-5:])


def get_st_nominal(cards, strt_wghts):
    return sequence_nominal_finder(cards, strt_wghts)


def get_tk_nominal(cards, wr):
    return repeat_nominal_finder(cards, wr[3][0])


def get_tp_nominal(cards, wr):
    return half_nominal_finder(cards, wr[2][-1], wr[2][-2])


def get_op_nominal(cards, wr):
    return repeat_nominal_finder(cards, wr[2][0])


def get_hc_nominal(cards):
    return pure_nominal_finder(cards[-5:])


def sort_rcards(rcards, cards):
    result = cards[:]

    for c in filter(lambda c: c // 1000, rcards):
        try:
            result[result.index(c % 1000)] = c
        except ValueError:
            pass

    return result


nominal_values = {
    9: get_sf_nominal,
    8: get_fk_nominal,
    7: get_fh_nominal,
    6: get_fl_nominal,
    5: get_st_nominal,
    4: get_tk_nominal,
    3: get_tp_nominal,
    2: get_op_nominal,
    1: get_hc_nominal,
}


def find_ratio_combo(rcards):
    cards = [c % 1000 for c in rcards]
    value, data = find_combo(cards, nedded_data=True)

    kind_args = {'cards': sort_rcards(rcards, data['cards'])}

    if data['str_index']:
        kind_args['strt_wghts'] = data['weights'][(data['str_index'] - 4):(data['str_index'] + 1)]
        if kind_args['strt_wghts'][0] == 1:
            kind_args['strt_wghts'][0] = 14

    if value[0] in (8, 7, 4, 3, 2):
        kind_args['wr'] = data['wr']

    kind = nominal_values[value[0]](**kind_args)

    return value, kind


def hcombo(table_string, hand_string):
    return find_ratio_combo(cards(table_string) + cards(hand_string, 1))


def chcombo(hcards):
    return find_ratio_combo(hcards)
