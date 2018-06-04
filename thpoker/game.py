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


import random

from thpoker.core import Deck, Table, Hand, Combo


class Player():

    class Action():
        ALL_IN = 'all-in'
        BLIND_BET = 'blind_bet'
        CALL = 'call'
        CHECK = 'check'
        FOLD = 'fold'
        RAISE = 'raise'

        OUTSIDE_AVAILABLE = (BLIND_BET, CALL, CHECK, FOLD, RAISE)
        ALLWAYS_ACCEPTED = (BLIND_BET, FOLD)
        WITH_BET = (BLIND_BET, RAISE)

        def __init__(self, kind, bet=0):
            self.kind = kind
            self.bet = bet


    def __init__(self, identifier):
        self.identifier = identifier
        self.chips = 0
        self.round_bets = 0
        self.stage_bets = 0
        self.last_action = None
        self.abilities = {
            self.Action.RAISE: 0,
            self.Action.CALL: 0,
            self.Action.CHECK: False}
        self.has_ability = {
            self.Action.RAISE: lambda bet: self.abilities[self.Action.RAISE] >= bet,
            self.Action.CALL: lambda: self.abilities[self.Action.CALL] > 0,
            self.Action.CHECK: lambda: self.abilities[self.Action.CHECK]}
        self.dif = 0 # difference beetwen player's round bets and max bets of current round
        self.combo = None
        self.hand = Hand()

    def get_chips(self, chips):
        self.chips += chips

    def get_combo(self, table):
        self.combo = Combo(table=table, hand=self.hand)
        return self.combo

    def new_round(self):
        self.round_bets = 0
        self.hand.clean()

    def new_stage(self):
        self.stage_bets = 0
        self.dif = 0
        self.last_action = None

    def _get_abilities(self):
        self.abilities[self.Action.RAISE] = self.chips if self.chips > self.dif else 0
        if self.dif:
            self.abilities[self.Action.CALL] = self.chips if self.dif >= self.chips else self.dif
            self.abilities[self.Action.CHECK] = False
        else:
            self.abilities[self.Action.CALL] = 0
            self.abilities[self.Action.CHECK] = True

    def get_dif(self, max_round_bets):
        self.dif = max_round_bets - self.round_bets
        self._get_abilities()

    def action(self, kind, bet):
        if kind not in self.Action.OUTSIDE_AVAILABLE:
            return {"success": False, "description": "Wrong move kind."}
        args = [bet] if kind in self.Action.WITH_BET else []
        if kind not in self.Action.ALLWAYS_ACCEPTED and not self.has_ability[kind](*args):
            return {"success": False, "description": "Illegal move."}

        getattr(self, f"_{kind}")(*args)
        return {"success": True, "description": "Successfully moved."}

    def _betting(self, bet):
        self.chips -= bet
        self.round_bets += bet
        self.stage_bets += bet

    def _raise(self, bet):
        if self.chips > bet:
            self.last_action = self.Action(self.Action.RAISE, bet)
            self._betting(bet)
        else:
            self._all_in()

    def _call(self):
        if self.chips > self.dif:
            self.last_action = self.Action(self.Action.CALL, self.dif)
            self._betting(self.dif)
        else:
            self._all_in()

    def _check(self):
        self.last_action = self.Action(self.Action.CHECK)

    def _blind_bet(self, bet):
        if self.chips > bet:
            self.last_action = self.Action(self.Action.BLIND_BET, bet)
            self._betting(bet)
        else:
            self._all_in()

    def _fold(self):
        self.last_action = self.Action(self.Action.FOLD)

    def _all_in(self):
        self.last_action = self.Action(self.Action.ALL_IN, self.chips)
        self._betting(self.chips)


# two players game yet
class Game():
    # AGRESSIVE = {
    #     Player.Action.RAISE: 1,
    #     Player.Action.CALL: 0.5,
    #     Player.Action.CHECK: 0.5,
    #     Player.Action.FOLD: 0,
    #     Player.Action.BLIND_BET: None,
    # }

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

        def get_cards(self, deck):
            for player in self:
                player.hand.pull(deck)

        @property
        def bank(self):
            return sum([player.round_bets for player in self])

        def get_fold(self):
            self.opponent.get_chips(self.bank)

        def get_result(self, table):
            winners = []
            loosers = []
            best_combo = None
            for player in self:
                combo = player.combo or player.get_combo(table)
                if best_combo:
                    if combo > best_combo:
                        best_combo = combo
                        loosers += winners
                        winners = [player]
                    elif combo == best_combo:
                        winners.append(player)
                    else:
                        loosers.append(player)
                else:
                    best_combo = combo
                    winners = [player]
            winners_bets = sum((p.round_bets for p in winners))
            all_bets = self.bank
            for looser in loosers:
                if looser.round_bets > winners_bets:
                    over_bet = looser.round_bets - winners_bets
                    all_bets -= over_bet
                    looser.get_chips(over_bet)
            gain_bets = all_bets - winners_bets
            for winner in winners:
                winner.get_chips(winner.round_bets + int(gain_bets * winner.round_bets / winners_bets))


    class State():
        ALL_IN = 'all-in'
        THE_END = 'the_end'
        FOLD = 'fold'
        NORMAL = 'normal'
        SHOW_DOWN = 'show_down'

        def __init__(self):
            self.refresh()

        def refresh(self):
            self.kind = self.NORMAL


    class Stage():
        PRE_FLOP = 'pre_flop'
        FLOP = 'flop'
        TURN = 'turn'
        RIVER = 'river'
        ALL = (PRE_FLOP, FLOP, TURN, RIVER)

        def __init__(self):
            self.started = False
            self.index = 0 # current stage index
            self.depth = 0 # players moves count per stage

        @property
        def name(self):
            return self.ALL[self.index]

        @property
        def table_size(self):
            return self.index + 2 if self.index else 0

        def next(self):
            if self.started:
                self.index += 1
                self.depth = 0
            else:
                self.started = True

        def depth_increase(self):
            self.depth += 1


    def __init__(self, settings, *players):
        self.players = self.Players(settings["chips"], *players)
        self.blindes = settings["blindes"]
        self.state = self.State()
        self.table = Table()
        self.deck = Deck()

    def new_round(self):
        if self.state.kind == self.State.THE_END:
            return {"success": False, "description": "Game over."}
        self.players.new_round()
        self.table.clean()
        self.deck.refresh()
        self.state.refresh()
        self.stage = self.Stage()
        return {"success": True, "description": "Redy to start new stage."}

    def new_stage(self):
        if self.state.kind in (self.State.SHOW_DOWN, self.State.FOLD):
            return {"success": False,
                "description": "Round over.",
                "the_end": False,
                "round_end": True,
                "stage_end": True}
        self.stage.next()
        self.players.new_stage()
        if self.stage.name == self.Stage.FLOP:
            self.players.change_order()
        self._distribution()
        if self.state.kind != self.State.ALL_IN or \
            self.stage.name == self.Stage.PRE_FLOP and \
                self.players.current.chips and \
                    self.players.current.stage_bets < self.players.opponent.chips:
            self.players.get_dif()
            return {
                "success": True,
                "description": "Redy to accept action.",
                "the_end": False,
                "round_end": False,
                "stage_end": False}
        elif self.stage.name == self.Stage.RIVER:
            return self._show_down()
        return self._stage_end()

    def _distribution(self):
        if self.stage.name == self.Stage.PRE_FLOP:
            self._get_blindes()
            self.players.get_cards(self.deck)
        else:
            self.table.pull_to(self.deck, self.stage.table_size)

    def _get_blindes(self):
        for bet, index in zip(self.blindes, (0, 1)):
            player = self.players[index]
            player.action(Player.Action.BLIND_BET, bet)
            if player.last_action.kind == Player.Action.ALL_IN:
                self.state.kind = self.State.ALL_IN

    def action(self, kind, bet=0):
        result = self.players.current.action(kind, bet)
        if not result["success"]:
            result.update({"the_end": False, "round_end": False, "stage_end": False})
            return result

        # agressive = self.AGRESSIVE[kind]

        action_kind = self.players.current.last_action.kind
        if action_kind == Player.Action.FOLD:
            self.state.kind = self.State.FOLD
            self.players.get_fold()
            return self._stage_end()
        else:
            if action_kind == Player.Action.ALL_IN:
                self.state.kind = self.State.ALL_IN
            if self.players.opponent.chips and \
                (action_kind == Player.Action.RAISE or \
                    action_kind == Player.Action.ALL_IN and self.players.opponent.stage_bets < self.players.current.stage_bets or \
                        action_kind in (Player.Action.CALL, Player.Action.CHECK) and not self.stage.depth):
                self.players.next_player()
                self.stage.depth_increase()
                self.players.get_dif()
                return {
                    "success": True,
                    "the_end": False,
                    "round_end": False,
                    "stage_end": False,
                    "description": "Redy to accept action."}
            elif self.stage.name == self.Stage.RIVER:
                return self._show_down()
            return self._stage_end()

    def _show_down(self):
        self.players.get_result(self.table)
        self.state.kind = self.State.THE_END if self._the_end else self.State.SHOW_DOWN
        return self._stage_end()

    def _stage_end(self):
        if self.stage.name == self.Stage.PRE_FLOP and self.state.kind == self.State.FOLD:
            self.players.change_order()
        return {
            "success": True,
            "the_end": self.state.kind == self.State.THE_END,
            "round_end": self.state.kind in (self.State.SHOW_DOWN, self.State.FOLD, self.State.THE_END),
            "stage_end": True,
            "description": "Stage has been ended."}

    @property
    def _the_end(self):
        for player in self.players:
            if player.chips == 0:
                return True
        return False
