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
