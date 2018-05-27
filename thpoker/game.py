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


from thpoker.core import Hand


class Action():
    ALL_IN = 'all-in'
    BLIND_BET = 'blind_bet'
    CALL = 'call'
    CHECK = 'check'
    FOLD = 'fold'
    RAISE = 'raise'
    HOLD = 'hold'

    def __init__(self, kind, bet=0, agressive=None):
        self.kind = kind
        self.bet = bet
        self.agressive = agressive


class Player():
    def __init__(self, identifier):
        self.identifier = identifier
        self.chips = 0
        self.round_bets = 0
        self.stage_bets = 0
        self.action = None
        self.dif = 0 # difference beetwen player's round bets and max bets of current round
        self.combo = None
        self.hand = Hand()

    def get_chips(self, chips):
        self.chips += chips

    def new_round(self):
        self.round_bets = 0
        self.hand.cleaning()

    def new_stage(self):
        self.stage_bets = 0
        self.dif = 0

    def get_dif(self, max_round_bets):
        self.dif = max_round_bets - self.round_bets

    def betting(self, bet):
        self.chips -= bet
        self.round_bets += bet
        self.stage_bets += bet

    def raising(self, bet):
        agressive = 1
        if self.chips > bet:
            self.action = Action(Action.RAISE, bet, agressive)
            self.betting(bet)
        else:
            self.all_in(agressive)

    def call_check(self):
        agressive = 0.5
        if self.dif: # there is greater round bets than player made
            if self.chips > self.dif:
                bet = self.dif
                self.action = Action(Action.CALL, bet, agressive)
                self.betting(bet)
            else:
                self.all_in(agressive)
        else:
            self.action = Action(Action.CHECK, agressive=agressive)

    def blind_bet(self, blind):
        if self.chips > blind:
            bet = blind
            self.action = Action(Action.BLIND_BET, bet)
            self.betting(bet)
        else:
            self.all_in()

    def fold(self):
        self.action = Action(Action.FOLD, agressive=0)

    def hold(self):
        self.action = Action(Action.HOLD)

    def all_in(self, agressive=None):
        self.action = Action(Action.ALL_IN, self.chips, agressive)
        self.betting(self.chips)


class Game():
    class Players():
        def __init__(self, chips, *players):
            self.scroll = players
            self.order = random.choice(([0, 1], [1, 0]))
            self.curent_index = 0 # active player's index
            for player in self:
                player.get_chips(chips)

        def __getitem__(self, key):
            return self.scroll[self.order[key]]

        def new_round(self):
            for player in self:
                player.new_round()

        def new_stage(self):
            for player in self:
                player.new_stage()
            self.curent_index = 0

        @property
        def current(self): # active player
            return self[self.curent_index]

        @property
        def opponent(self): # active player's opponent
            return self[abs(self.curent_index - 1)]

        def next_player(self): # transition move rights
            self.curent_index = abs(self.curent_index - 1)

        def change_order(self):
            self.order.reverse()

        def get_dif(self):
            max_round_bets = max([player.round_bets for player in self])
            for player in self:
                player.get_dif(max_round_bets)

        @property
        def bank(self):
            return sum([player.round_bets for player in self])
