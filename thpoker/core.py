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


# -*- coding: utf-8 -*-

import random

from agstuff.cards.core import Card, Cards as BaseCards
from thpoker.exceptions import ComboCardsTypeError, ComboArgumentsError


class Cards(BaseCards):
    """Several cards."""

    def __init__(self, cards_string=None, cards=None):
        super().__init__(cards_string=cards_string, cards=cards, max_count=7)


class Table(BaseCards):
    """Table cards."""

    def __init__(self, cards_string=None, cards=None):
        super().__init__(cards_string=cards_string, cards=cards, max_count=5)


class Hand(BaseCards):
    """Player's hand cards."""

    def __init__(self, cards_string=None, cards=None):
        self.type = ''
        self.is_pair = False
        super().__init__(cards_string=cards_string, cards=cards, max_count=2)
        if self.items:
            self.after_pull()

    def pull(self, deck):
        super().pull(deck=deck, count=2)
        self.after_pull()

    def after_pull(self):
        for card in self.items:
            card.in_hand = True
        self.typing()

    def typing(self):
        self.items.sort()
        self.items.reverse()
        self.type = self.items[0].weight.symbol + self.items[1].weight.symbol
        if self.items[0] == self.items[1]:
            self.is_pair = True
        else:
            self.type += 's' if self.items[0].suit == self.items[1].suit else 'o'

    def clean(self):
        super().clean()
        self.type = ''
        self.is_pair = False


class Combo:
    '''
    Cards combination.

    One of high card, one pair, two pairs, three of a kind, straight, flush, full house, four of a kind, straight flush.

    Takes arguments (cards_string, cards, table, hand, ratio_check)
    For example:
        Combo(cards_string='6s/Jc/Ah/9h/3d/Jd') or Combo('6s/Jc/Ah/9h/3d/Jd')
    or
        Combo(cards=Cards('6s/Jc/Ah/9h/3d/Jd'))
    or
        Combo(table=Table('6s/Jc/Ah/9h'), hand=Hand('3d/Jd'))
    or
        Combo(table=Table('6s/Jc/Ah/9h'), hand=Hand('3d/Jd'), ratio_check=True)
    '''

    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIRS = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9

    TYPE_NAMES = {
        HIGH_CARD: "high card",
        ONE_PAIR: "one pair",
        TWO_PAIRS: "two pairs",
        THREE_OF_A_KIND: "three of a kind",
        STRAIGHT: "straight",
        FLUSH: "flush",
        FULL_HOUSE: "full house",
        FOUR_OF_A_KIND: "four of a kind",
        STRAIGHT_FLUSH: "straight flush"
    }

    SHORT_TYPE_NAMES = {
        HIGH_CARD: "hc",
        ONE_PAIR: "op",
        TWO_PAIRS: "tp",
        THREE_OF_A_KIND: "tk",
        STRAIGHT: "st",
        FLUSH: "fl",
        FULL_HOUSE: "fh",
        FOUR_OF_A_KIND: "fk",
        STRAIGHT_FLUSH: "sf"
    }


    class Sequence:
        """Cards sequence."""

        def __init__(self, cards):
            self.order_cards = None  # 5 cards sequence
            self.five_in_a_row = False
            self.max_in_a_row = 0
            self.cards = cards
            if Card('A') in self.cards:
                self.one_more_ace()
            self.find_order()

        def one_more_ace(self):
            """Add Ace wich weight is 1."""
            ace = list(filter(lambda card: card == Card('A'), self.cards))[-1]
            self.cards.insert(0, Card('1' + ace.suit.symbol))
            self.cards[0].in_hand = ace.in_hand

        def get_rank(self):
            rank = [Card(w) for w in Card.Weight.symbols]  # abstract cards
            for card in self.cards:
                rank[card.weight.number] = card  # change abstract cards to real
            rank.reverse()
            return rank

        def find_order(self):
            base = 0
            cards_in_a_row = 0
            history = []
            rank = self.get_rank()
            for i in range(14):
                if rank[i].suit:
                    cards_in_a_row += 1
                    history.append(cards_in_a_row)
                    if cards_in_a_row == 5:
                        self.five_in_a_row = True
                        self.order_cards = rank[base:base+5]
                        break
                else:
                    base = i+1
                    cards_in_a_row = 0
            self.max_in_a_row = max(history)


    class Repeats:
        '''Weights and suits repeats'''


        class BaseRepeats:

            def __init__(self):
                self.cards = []
                self.all = {}

            def __getitem__(self, key):
                return self.all[key]

            def __setitem__(self, key, value):
                self.all[key] = value

            def __contains__(self, item):
                return item in self.all

            def count(self, number):
                return len(self.all[number])


        class WeightRepeats(BaseRepeats):

            def __init__(self):
                super().__init__()
                self.four = None
                self.three = None
                self.double_three = False
                self.two = None
                self.double_two = None
                self.triple_two = False

            def get_repeat_kind(self):
                if 4 in self.all:
                    self.four = self.all[4][0] # four of a kind
                elif 3 in self.all:
                    self.three = self.all[3][-1] # three of a kind
                    if 2 in self.all:
                        self.two = self.all[2][-1] # full house
                    if self.count(3) == 2:
                        self.two = self.all[3][-2] # full house
                        self.double_three = True
                elif 2 in self.all:
                    if self.count(2) > 1:
                        self.double_two = self.all[2][-2:] # two pairs
                        if self.count(2) == 3:
                            self.triple_two = True
                    else:
                        self.two = self.all[2][-1] # pair


        class SuitRepeats(BaseRepeats):

            def __init__(self):
                super().__init__()
                self.max_repeats = 0
                self.five_or_more = False
                self.flush_card = None

            def flush_or_not(self):
                self.max_repeats = max(self.all) # max suit repeats
                self.five_or_more = self.max_repeats >= 5
                self.flush_card = self.all[self.max_repeats][0]

        def __init__(self, cards):
            self.weight = self.WeightRepeats()
            self.suit = self.SuitRepeats()
            self.cards = cards
            self.get_all_repeats()
            self.weight.get_repeat_kind()
            self.suit.flush_or_not()

        def get_all_repeats(self):
            for card in self.cards:
                w_card = Card(card.weight.symbol) # abstract weight card
                s_card = Card(card.suit.symbol) # abstract suit card
                for (card, repeats) in ((w_card, self.weight), (s_card, self.suit)):
                    if card not in repeats.cards:
                        cnt = self.cards.count(card) # repeats count
                        try:
                            repeats[cnt].append(card)
                        except KeyError:
                            repeats[cnt] = [card]
                        repeats.cards.append(card)


    class Cards:
        """
        Combination cards.
        Allows to compare similar type combinations.
        """

        def __init__(self):
            self.items = []

        def __str__(self):
            return f"({', '.join(self.items)})"

        def __repr__(self):
            return str(self.items)

        def __lt__(self, other):
            return self._compare(other, '__lt__', False)

        def __gt__(self, other):
            return self._compare(other, '__gt__', False)

        def __eq__(self, other):
            return self._compare(other, '__eq__', True)

        def __ne__(self, other):
            return self._compare(other, '__ne__', False)

        def __getitem__(self, key):
            return self.items[key]

        def __contains__(self, item):
            return item in self.items

        def __len__(self):
            return len(self.items)

        def _compare(self, other, method, even):
            for card1, card2 in zip(self.items, other.items):
                if card1 != card2:
                    return getattr(card1, method)(card2)
            else:
                return even

        def add_card(self, card):
            self.items.append(card)

        def add_cards(self, cards):
            self.items.extend(cards)

        def get_other_cards(self, all_cards):  # add cards to main combination
            cards_to_add = list(filter(lambda card: card not in self, all_cards))
            if not cards_to_add: return
            cards_to_add.reverse()
            free_places = 5 - len(self)
            self.add_cards(cards_to_add[:free_places])


    class Ratio:
        """
        Combination ratio.
        Shows whether combination base cards inlude hand cards or not.
        """

        REAL = "real" # combo base cards inlude hand cards
        HALF = "half" # half combo base cards inlude hand cards
        MISS = "miss" # combo base cards don't inlude hand cards

        def __init__(self, combo):
            self._combo = combo
            self._value = None

        @property
        def is_real(self):
            return self._value == self.REAL

        @property
        def is_half(self):
            return self._value == self.HALF

        @property
        def is_miss(self):
            return self._value == self.MISS

        @property
        def is_checked(self):
            return not self._value is None

        def check(self):
            suffix = Combo.SHORT_TYPE_NAMES[self._combo.type]
            getattr(self, f'_check_{suffix}')()

        def _check_hc(self):
            self._check_all_cards()

        def _check_op(self):
            self._find(self._combo.cards[:2])

        def _check_tp(self):
            pair1 = self._combo.cards[:2]
            pair2 = self._combo.cards[2:4]
            self._find_with_half((pair1, pair2))

        def _check_tk(self):
            self._find(self._combo.cards[:3])

        def _check_st(self):
            self._check_all_cards()

        def _check_fl(self):
            self._check_all_cards()

        def _check_fh(self):
            three = list(filter(lambda c: c == self._combo.repeats.weight.three, self._combo.init_cards))
            two = list(filter(lambda c: c == self._combo.repeats.weight.two, self._combo.init_cards))
            self._find_with_half((three, two))

        def _check_fk(self):
            self._find(self._combo.cards[:4])

        def _check_sf(self):
            self._check_all_cards()

        def _check_all_cards(self):
            self._find(self._combo.cards[:])

        def _find(self, cards):
            for card in cards:
                if card.in_hand:
                    self._value = self.REAL
                    break
            else:
                self._value = self.MISS

        def _find_with_half(self, cards_set):
            combo_cards_in_hand = 0
            for cards in cards_set:
                for card in cards:
                    if card.in_hand:
                        combo_cards_in_hand += 1
                        break
            self._value = {
                2: self.REAL,
                1: self.HALF,
                0: self.MISS,
            }[combo_cards_in_hand]


    def __init__(self, cards_string=None, cards=None, table=None, hand=None, ratio_check=False):
        ratio_check_needed = False
        if cards_string:
            self.init_cards = Cards(cards_string).items
        elif cards:
            cards_type = type(cards)
            if not cards_type is Cards:
                raise ComboCardsTypeError(cards_type, Cards, 'cards')
            self.init_cards = cards.items
        elif table and hand:
            table_type = type(table)
            if not table_type is Table:
                raise ComboCardsTypeError(table_type, Table, 'table')
            hand_type = type(hand)
            if not hand_type is Hand:
                raise ComboCardsTypeError(hand_type, Hand, 'hand')
            self.init_cards = table.items + hand.items
            if ratio_check:
                ratio_check_needed = True
        else:
            raise ComboArgumentsError()

        self.cards = self.Cards()
        self.repeats = None
        self.sequence = None
        self.type = None
        self.ratio = self.Ratio(self)

        self.find_combo()
        if ratio_check_needed:
            self.ratio.check()

    @property
    def name(self):
        return self.TYPE_NAMES[self.type]

    @property
    def short_name(self):
        return self.SHORT_TYPE_NAMES[self.type]

    @property
    def is_real(self):
        return self.ratio.is_real

    @property
    def is_half_nominal(self):
        return self.ratio.is_half

    @property
    def is_nominal(self):
        return self.ratio.is_miss

    def __str__(self):
        return  f"{self.name} {self.cards}"

    def __repr__(self):
        return str([self.type] + self.cards.items)

    def __lt__(self, other):
        return (self.type, self.cards) < (other.type, other.cards)

    def __gt__(self, other):
        return (self.type, self.cards) > (other.type, other.cards)

    def __eq__(self, other):
        return (self.type, self.cards) == (other.type, other.cards)

    def __ne__(self, other):
        return (self.type, self.cards) != (other.type, other.cards)

    def find_combo(self):
        self.init_cards.sort()
        self.repeats = self.Repeats(cards=self.init_cards)
        if not self.repeats.suit.five_or_more:
            self.sequence = self.Sequence(cards=self.init_cards[:])
            if self.repeats.weight.four:
                self.get_four_of_a_kind()
            elif self.repeats.weight.three and self.repeats.weight.two:
                self.get_full_house()
            elif self.sequence.five_in_a_row:
                self.get_straight()
            elif self.repeats.weight.three:
                self.get_three_of_a_kind()
            elif self.repeats.weight.double_two:
                self.get_two_pairs()
            elif self.repeats.weight.two:
                self.get_one_pair()
            else:
                self.get_high_card()
        else:
            cards = list(filter(lambda card: card == self.repeats.suit.flush_card, self.init_cards))
            self.sequence = self.Sequence(cards=cards)
            if self.sequence.five_in_a_row:
                self.get_straight_flush()
            else:
                self.get_flush()

    def get_straight_flush(self):
        self.type = self.STRAIGHT_FLUSH
        self.cards.add_cards(self.sequence.order_cards)

    def get_four_of_a_kind(self):
        self.type = self.FOUR_OF_A_KIND
        four = list(filter(lambda card: card == self.repeats.weight.four, self.init_cards))
        self.cards.add_cards(four)
        self.cards.get_other_cards(self.init_cards)

    def get_full_house(self):
        self.type = self.FULL_HOUSE
        the_set = list(filter(lambda card: card == self.repeats.weight.three, self.init_cards))
        pair = list(filter(lambda card: card == self.repeats.weight.two, self.init_cards))[:2]
        self.cards.add_cards(the_set + pair)

    def get_flush(self):
        self.type = self.FLUSH
        cards = self.sequence.cards[-5:]
        cards.reverse()
        self.cards.add_cards(cards)

    def get_straight(self):
        self.type = self.STRAIGHT
        self.cards.add_cards(self.sequence.order_cards)

    def get_three_of_a_kind(self):
        self.type = self.THREE_OF_A_KIND
        three = list(filter(lambda card: card == self.repeats.weight.three, self.init_cards))
        self.cards.add_cards(three)
        self.cards.get_other_cards(self.init_cards)

    def get_two_pairs(self):
        self.type = self.TWO_PAIRS
        pairs = list(filter(lambda card: card in self.repeats.weight.double_two, self.init_cards))
        self.cards.add_cards(pairs[2:]+pairs[:2])
        self.cards.get_other_cards(self.init_cards)

    def get_one_pair(self):
        self.type = self.ONE_PAIR
        pair = list(filter(lambda card: card == self.repeats.weight.two, self.init_cards))
        self.cards.add_cards(pair)
        self.cards.get_other_cards(self.init_cards)

    def get_high_card(self):
        self.type = self.HIGH_CARD
        top_five_cards = self.init_cards[-5:]
        top_five_cards.reverse()
        self.cards.add_cards(top_five_cards)
