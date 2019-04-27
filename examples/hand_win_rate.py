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


from thpoker.hardcore import chcombo, wght, hdeck


def get_first_hand(h1):
    w1, w2 = (wght[w] for w in h1[:2])
    try:
        if h1[2] == "s":
            return (w1 + 1, w2 + 1), {1: 1}, [2, 3, 4]
    except IndexError:
        pass
    return (w1 + 1, w2 + 2), {1: 1, 2: 2}, [3, 4]


def get_pure_second_hands(h2, deck):
    w3, w4 = (wght[w] for w in h2[:2])
    if w3 == w4:
        cards = tuple(filter(lambda c: c // 10 * 10 in (w3, w4), deck))
        cards_len = len(cards)
        for a in range(cards_len - 1):
            for b in range(a + 1, cards_len):
                yield (cards[a], cards[b])
    else:
        third_cards = filter(lambda c: c // 10 * 10 == w3, deck)
        fourth_cards = tuple(filter(lambda c: c // 10 * 10 == w4, deck))
        if h2[2] == "o":
            for card3 in third_cards:
                for card4 in fourth_cards:
                    yield (card3, card4)
        else:
            for card3 in third_cards:
                for card4 in fourth_cards:
                    if card3 % 10 == card4 % 10:
                        yield (card3, card4)


def normalize_cards(suits, free_numbers, *cards):
    for card in cards:
        s = card % 10
        if s not in suits:
            suits[s] = free_numbers.pop(0)
        yield card // 10 * 10 + suits[s]


def get_norm_second_hands(deck, suits, free_numbers, h2):
    for hand in get_pure_second_hands(h2, deck):
        local_numbers = free_numbers[:]
        local_suit = suits.copy()
        yield tuple(normalize_cards(local_suit, local_numbers, *hand)), local_suit, local_numbers


def get_second_hands(deck, suits, free_numbers, h2):
    hands_data = {}
    for hand, local_suit, local_numbers in get_norm_second_hands(deck, suits, free_numbers, h2):
        if hand in hands_data:
            hands_data[hand]["rate"] += 1
        else:
            hands_data[hand] = {
                "rate": 1,
                "suits": local_suit,
                "free_numbers": free_numbers,
            }
    for value in hands_data.items():
        yield value


# def flop_tables_factory(deck, suits, free_numbers):
#     for a in range(46):
#         for b in range(a + 1, 47):
#             for c in range(b + 1, 48):
#                 yield tuple(normalize_cards(suits.copy(), free_numbers[:], deck[a], deck[b], deck[c]))


# def turn_tables_factory(deck, suits, free_numbers):
#     for a in range(45):
#         for b in range(a + 1, 46):
#             for c in range(b + 1, 47):
#                 for d in range(c + 1, 48):
#                     yield tuple(normalize_cards(suits.copy(), free_numbers[:], deck[a], deck[b], deck[c], deck[d]))


def river_tables_factory(deck, suits, free_numbers):
    for a in range(44):
        for b in range(a + 1, 45):
            for c in range(b + 1, 46):
                for d in range(c + 1, 47):
                    for e in range(d + 1, 48):
                        yield tuple(normalize_cards(suits.copy(), free_numbers[:], deck[a], deck[b], deck[c], deck[d], deck[e]))


def get_combos(h1, h2):
    deck = hdeck()
    hand1, suits, free_numbers = get_first_hand(h1)
    for card in hand1:
        del deck[deck.index(card)]
    for hand2, data in get_second_hands(deck, suits, free_numbers, h2):
        local_deck = deck[:]
        for card in hand2:
            del local_deck[local_deck.index(card)]
        for table in river_tables_factory(local_deck, data["suits"], data["free_numbers"]):
            yield chcombo(list(hand1 + table)), chcombo(list(hand2 + table)), data["rate"]


def get_result(h1, h2):
    points = [0, 0, 0]
    for combo1, combo2, rate in get_combos(h1, h2):
        # win
        if combo1 > combo2:
            points[2] += rate
        # lose
        elif combo1 < combo2:
            points[0] += rate
        # draw
        else:
            points[1] += rate
    print(points)
    return (points[2] + points[1] / 2) / sum(points)


if __name__ == "__main__":
    print('get_result("AA", "89s")', get_result("AA", "89s"))
