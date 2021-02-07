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
            self._after_pull()

    def clean(self):
        super().clean()
        self.type = ''
        self.is_pair = False

    def pull(self, deck):
        super().pull(deck=deck, count=2)
        self._after_pull()

    def _after_pull(self):
        for card in self.items:
            card.in_hand = True
        self._typing()

    def _typing(self):
        self.items.sort()
        self.items.reverse()
        self.type = self.items[0].weight.symbol + self.items[1].weight.symbol
        if self.items[0] == self.items[1]:
            self.is_pair = True
        else:
            self.type += 's' if self.items[0].suit == self.items[1].suit else 'o'


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

        FIVE_OR_MORE_IN_A_ROW = 'five_or_more_in_a_row'
        FOUR_OR_LESS_IN_A_ROW = 'four_or_less_in_a_row'

        def __init__(self):
            self.state = self.FOUR_OR_LESS_IN_A_ROW
            self.cards = []
            self.order_cards = []  # 5 cards sequence
            self.max_in_a_row = 0

        def find(self, cards):
            self.cards = cards
            self._add_one_more_ace()
            rank = self._get_rank()
            base = 0
            cards_in_a_row = 0
            for i, card in enumerate(rank):
                if not card:
                    base = i + 1
                    cards_in_a_row = 0
                    continue
                cards_in_a_row += 1
                if cards_in_a_row > self.max_in_a_row:
                    self.max_in_a_row = cards_in_a_row
                if cards_in_a_row == 5:
                    self.order_cards = rank[base:base + 5]
                    self.state = self.FIVE_OR_MORE_IN_A_ROW
                    break

        def _add_one_more_ace(self):
            """Add an ace with weight 1 if an real ace is in cards."""

            for card in self.cards:
                if card == Card('A'): break
            else:
                return
            new_ace = Card(f'1{card.suit.symbol}')
            new_ace.in_hand = card.in_hand
            self.cards.insert(0, new_ace)

        def _get_rank(self):
            rank = [None] * 14
            for card in self.cards:
                rank[card.weight.number] = card
            rank.reverse()
            return rank


    class Repeats:
        '''Weights and suits repeats'''

        FOUR_WEIGHT_REPEATS = 'four_weigh_repeats'
        THREE_TWO_WEIGHT_REPEATS = 'three_two_weigh_repeats'
        FIVE_OR_MORE_SUIT_REPEATS = 'five_or_more_suit_repeats'
        THREE_OR_LESS_WEIGHT_REPEATS = 'three_or_less_weigh_repeats'

        class BaseRepeats:

            def __init__(self, repeats):
                self._repeats = repeats
                self.card_counts = {}
                self.included_cards = []
                self.repeat_counts = {}
                self.all = {}
                self.max = 0

            def add(self, card):
                self.card_counts[card] = self.card_counts.get(card, 0) + 1
                if self.card_counts[card] == 1:
                    self.included_cards.append(card)

            def find(self):
                for card in self.included_cards:
                    count = self.card_counts[card]
                    if (repeat := self.all.get(count)):
                        repeat.append(card)
                    else:
                        self.all[count] = [card]
                    if count > self.max:
                        self.max = count
                    self.repeat_counts[count] = self.repeat_counts.get(count, 0) + 1


        class WeightRepeats(BaseRepeats):

            FOUR = 'four'
            DOUBLE_THREE = 'double_three'
            THREE_AND_TWO = 'three_and_two'
            THREE = 'three'
            TRIPLE_TWO = 'triple_two'
            DOUBLE_TWO = 'double_two'
            TWO = 'two'
            NO = 'no'

            def __init__(self, repeats):
                super().__init__(repeats)
                self.state = None
                self.cards = None

            def find(self):
                super().find()
                getattr(self, f'_get_{self.max}')()

            def _get_4(self):
                self.state = self.FOUR
                self.cards = {
                    4: self.all[4][0],
                }
                self._repeats.state = self._repeats.FOUR_WEIGHT_REPEATS

            def _get_3(self):
                getattr(self, f'_get_3_with_{self.repeat_counts[3]}_rep_and_2_with_{self.repeat_counts.get(2, 0)}_rep')()

            def _get_3_with_2_rep_and_2_with_0_rep(self):
                self.state = self.DOUBLE_THREE
                self.cards = {
                    3: self.all[3][1],
                    2: self.all[3][0],
                }
                self._repeats.state = self._repeats.THREE_TWO_WEIGHT_REPEATS

            def _get_3_with_1_rep_and_2_with_2_rep(self):
                self._get_3_with_1_rep_and_2_with_1_rep()

            def _get_3_with_1_rep_and_2_with_1_rep(self):
                self.state = self.THREE_AND_TWO
                self.cards = {
                    3: self.all[3][0],
                    2: self.all[2][-1],
                }
                self._repeats.state = self._repeats.THREE_TWO_WEIGHT_REPEATS

            def _get_3_with_1_rep_and_2_with_0_rep(self):
                self.state = self.THREE
                self.cards = {
                    3: self.all[3][0],
                }
                self._repeats.state = self._repeats.THREE_OR_LESS_WEIGHT_REPEATS

            def _get_2(self):
                getattr(self, f'_get_2_with_{self.repeat_counts[2]}_rep')()
                self._repeats.state = self._repeats.THREE_OR_LESS_WEIGHT_REPEATS

            def _get_2_with_3_rep(self):
                self._get_2_with_2_rep()
                self.state = self.TRIPLE_TWO

            def _get_2_with_2_rep(self):
                self.state = self.DOUBLE_TWO
                self.cards = {
                    22: self.all[2][-1],
                    21: self.all[2][-2],
                }

            def _get_2_with_1_rep(self):
                self.state = self.TWO
                self.cards = {
                    2: self.all[2][0],
                }

            def _get_1(self):
                self.state = self.NO
                self._repeats.state = self._repeats.THREE_OR_LESS_WEIGHT_REPEATS


        class SuitRepeats(BaseRepeats):

            def __init__(self, repeats):
                super().__init__(repeats)
                self.five_or_more = False
                self.flush_card = None

            def find(self):
                super().find()
                if (five_or_more := self.max >= 5):
                    self.flush_card = self.all[self.max][0]
                    self._repeats.state = self._repeats.FIVE_OR_MORE_SUIT_REPEATS
                else:
                    self.flush_card = None
                self.five_or_more = five_or_more


        def __init__(self):
            self.weight = self.WeightRepeats(self)
            self.suit = self.SuitRepeats(self)
            self.state = self.THREE_OR_LESS_WEIGHT_REPEATS

        def find(self, cards):
            for card in cards:
                self.weight.add(Card(card.weight.symbol))
                self.suit.add(Card(card.suit.symbol))
            self.weight.find()
            self.suit.find()


    class Cards:
        """
        Combination cards.
        Allows to compare similar type combinations.
        """

        def __init__(self):
            self.items = []

        def __str__(self):
            return f"({', '.join(map(str, self.items))})"

        def __repr__(self):
            return repr(self.items)

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
            three = list(filter(lambda c: c == self._combo.repeats.weight.cards[3], self._combo.init_cards))
            two = list(filter(lambda c: c == self._combo.repeats.weight.cards[2], self._combo.init_cards))
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
        self.repeats = self.Repeats()
        self.sequence = self.Sequence()
        self.ratio = self.Ratio(self)
        self.type = None

        self._find()
        if ratio_check_needed:
            self.ratio.check()

    @property
    def name(self):
        return self.TYPE_NAMES[self.type]

    @property
    def short_name(self):
        return self.SHORT_TYPE_NAMES[self.type]

    def __str__(self):
        return  f"{self.name} {self.cards}"

    def __repr__(self):
        return repr([self.type] + self.cards.items)

    def __lt__(self, other):
        return (self.type, self.cards) < (other.type, other.cards)

    def __gt__(self, other):
        return (self.type, self.cards) > (other.type, other.cards)

    def __eq__(self, other):
        return (self.type, self.cards) == (other.type, other.cards)

    def __ne__(self, other):
        return (self.type, self.cards) != (other.type, other.cards)

    def _find(self):
        self.init_cards.sort()
        self.repeats.find(self.init_cards)
        getattr(self, f'_find_with_{self.repeats.state}')()

    def _find_with_four_weigh_repeats(self):
        self.type = self.FOUR_OF_A_KIND
        four = list(filter(lambda card: card == self.repeats.weight.cards[4], self.init_cards))
        self.cards.add_cards(four)
        self.cards.get_other_cards(self.init_cards)

    def _find_with_three_two_weigh_repeats(self):
        self.type = self.FULL_HOUSE
        the_set = list(filter(lambda card: card == self.repeats.weight.cards[3], self.init_cards))
        pair = list(filter(lambda card: card == self.repeats.weight.cards[2], self.init_cards))[:2]
        self.cards.add_cards(the_set + pair)

    def _find_with_five_or_more_suit_repeats(self):
        cards = list(filter(lambda card: card == self.repeats.suit.flush_card, self.init_cards))
        self.sequence.find(cards)
        getattr(self, f'_get_flush_with_{self.sequence.state}')()

    def _get_flush_with_five_or_more_in_a_row(self):
        self.type = self.STRAIGHT_FLUSH
        self.cards.add_cards(self.sequence.order_cards)

    def _get_flush_with_four_or_less_in_a_row(self):
        self.type = self.FLUSH
        cards = self.sequence.cards[-5:]
        cards.reverse()
        self.cards.add_cards(cards)

    def _find_with_three_or_less_weigh_repeats(self):
        self.sequence.find(self.init_cards[:])
        getattr(self, f'_get_combo_with_{self.sequence.state}')()

    def _get_combo_with_five_or_more_in_a_row(self):
        self.type = self.STRAIGHT
        self.cards.add_cards(self.sequence.order_cards)

    def _get_combo_with_four_or_less_in_a_row(self):
        getattr(self, f'_get_{self.repeats.weight.state}_weigh_repeats')()

    def _get_three_weigh_repeats(self):
        self.type = self.THREE_OF_A_KIND
        three = list(filter(lambda card: card == self.repeats.weight.cards[3], self.init_cards))
        self.cards.add_cards(three)
        self.cards.get_other_cards(self.init_cards)

    def _get_triple_two_weigh_repeats(self):
        self._get_double_two_weigh_repeats()

    def _get_double_two_weigh_repeats(self):
        self.type = self.TWO_PAIRS
        high_pair = list(filter(lambda card: card == self.repeats.weight.cards[22], self.init_cards))
        low_pair = list(filter(lambda card: card == self.repeats.weight.cards[21], self.init_cards))
        self.cards.add_cards(high_pair + low_pair)
        self.cards.get_other_cards(self.init_cards)

    def _get_two_weigh_repeats(self):
        self.type = self.ONE_PAIR
        pair = list(filter(lambda card: card == self.repeats.weight.cards[2], self.init_cards))
        self.cards.add_cards(pair)
        self.cards.get_other_cards(self.init_cards)

    def _get_no_weigh_repeats(self):
        self.type = self.HIGH_CARD
        top_five_cards = self.init_cards[-5:]
        top_five_cards.reverse()
        self.cards.add_cards(top_five_cards)
