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


class Context:
    def __init__(self, success, description, **data):
        self.success = success
        self.description = description
        self.add_data(**data)

    def add_data(self, **data):
        for attr, value in data.items():
            setattr(self, attr, value)


class Player:

    class Action:
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

        def __str__(self):
            return f"{self.kind}{self.bet or ''}"

        def __repr__(self):
            return f"{self.kind}{self.bet or ''}"


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
        self.refresh_last_action()

    def refresh_last_action(self):
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
            return Context(success=False, description="Wrong move kind.")
        args = [bet] if kind in self.Action.WITH_BET else []
        if kind not in self.Action.ALLWAYS_ACCEPTED and not self.has_ability[kind](*args):
            return Context(success=False, description="Illegal move.")

        getattr(self, f"_{kind}")(*args)
        return Context(success=True, description="Successfully moved.")

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
class Game:
    NORMAL = 'normal'
    FOLD = 'fold'
    ALL_IN = 'all-in'
    SHOW_DOWN = 'show_down'
    THE_END = 'the_end'
    ACTION_NEEDED = 'action_needed'
    STAGE_NEEDED = 'stage_needed'
    ROUND_NEEDED = 'round_needed'

    class Players:
        def __init__(self, chips, *players):
            self._scroll = players
            self._order = random.choice(([0, 1], [1, 0]))
            self._curent_index = 0 # active player's index
            for player in self:
                player.get_chips(chips)

        def __getitem__(self, key):
            return self._scroll[self._order[key]]

        def new_round(self):
            for player in self:
                player.new_round()

        def new_stage(self):
            for player in self:
                player.new_stage()
            self._curent_index = 0

        def action(self, kind, bet):
            self.opponent.refresh_last_action()
            return self.current.action(kind, bet)

        @property
        def current(self): # active player
            return self[self._curent_index]

        @property
        def opponent(self): # active player's opponent
            return self[abs(self._curent_index - 1)]

        def next_player(self): # transition move rights
            self._curent_index = abs(self._curent_index - 1)

        def change_order(self):
            self._order.reverse()

        def get_dif(self):
            max_round_bets = max([player.round_bets for player in self])
            self.current.get_dif(max_round_bets)

        def get_cards(self, deck):
            for player in self:
                player.hand.pull(deck)

        @property
        def bank(self):
            return sum((player.round_bets for player in self))

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
            return {
                "winners": [p.identifier for p in winners],
                "loosers": [p.identifier for p in loosers],
            }


    class Stage:
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
        self.state = self.NORMAL
        self.table = Table()
        self.deck = Deck()
        self.result = None

    def new_round(self):
        if self.state == self.THE_END:
            return Context(success=False, description="Game over.", **self._get_context_data(self.THE_END))
        self.players.new_round()
        self.table.clean()
        self.deck.refresh()
        self.state = self.NORMAL
        self.point = self.ROUND_NEEDED
        self.stage = self.Stage()
        self.result = None
        return Context(
            success=True,
            description="Redy to start new stage.",
            **self._get_context_data(self.STAGE_NEEDED))

    def new_stage(self):
        if self.state in (self.SHOW_DOWN, self.FOLD):
            return Context(success=False, description="Round over.", **self._get_context_data(self.ROUND_NEEDED))
        self.stage.next()
        self.players.new_stage()
        if self.stage.name == self.Stage.FLOP:
            self.players.change_order()
        self._distribution()
        if self.state != self.ALL_IN or \
            self.stage.name == self.Stage.PRE_FLOP and \
                self.players.current.chips and \
                    self.players.current.stage_bets < self.players.opponent.chips:
            self.players.get_dif()
            return Context(
                success=True,
                description="Redy to accept action.",
                **self._get_context_data(self.ACTION_NEEDED, True))
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
                self.state = self.ALL_IN

    def action(self, kind, bet=0):
        result = self.players.action(kind, bet)
        if not result.success:
            return result

        action_kind = self.players.current.last_action.kind
        if action_kind == Player.Action.FOLD:
            self.state = self.FOLD
            self.players.get_fold()
            return self._stage_end()
        else:
            if action_kind == Player.Action.ALL_IN:
                self.state = self.ALL_IN
            if self.players.opponent.chips and \
                (action_kind == Player.Action.RAISE or \
                    action_kind == Player.Action.ALL_IN and self.players.opponent.stage_bets < self.players.current.stage_bets or \
                        action_kind in (Player.Action.CALL, Player.Action.CHECK) and not self.stage.depth):
                self.players.next_player()
                self.stage.depth_increase()
                self.players.get_dif()
                return Context(
                    success=True,
                    description="Redy to accept action.",
                    **self._get_context_data(self.ACTION_NEEDED, True))
            elif self.stage.name == self.Stage.RIVER:
                return self._show_down()
            return self._stage_end()

    def _show_down(self):
        self.result = self.players.get_result(self.table)
        self.state = self.THE_END if self._the_end else self.SHOW_DOWN
        return self._stage_end()

    def _stage_end(self):
        if self.stage.name == self.Stage.PRE_FLOP and self.state == self.FOLD:
            self.players.change_order()
        if self.state == self.THE_END:
            point = self.THE_END
            description = "Game has been ended."
        elif self.state in (self.SHOW_DOWN, self.FOLD):
            point = self.ROUND_NEEDED
            description = "Round has been ended."
        else:
            point = self.STAGE_NEEDED
            description = "Stage has been ended."
        return Context(
            success=True,
            description=description,
            **self._get_context_data(point, True))

    @property
    def _the_end(self):
        for player in self.players:
            if player.chips == 0:
                return True
        return False

    def _get_context_data(self, point, additional=False):
        data = {"point": point}
        if additional:
            data.update({
                "table": self.table.items[:],
                "state": self.state,
                "stage_name": self.stage.name,
                "stage_depth": self.stage.depth,
                "bank": self.players.bank,
                "result": self.result,
                "players": {
                    "current": {
                        "identifier": self.players.current.identifier,
                        "chips": self.players.current.chips,
                        "stage_bets": self.players.current.stage_bets,
                        "round_bets": self.players.current.round_bets,
                        "dif": self.players.current.dif,
                        "abilities": self.players.current.abilities,
                        "cards": self.players.current.hand.items[:],
                        "hand_type": self.players.current.hand.type,
                        "combo": self.players.current.combo,
                        "last_action": self.players.current.last_action,
                    },
                    "opponent": {
                        "identifier": self.players.opponent.identifier,
                        "chips": self.players.opponent.chips,
                        "stage_bets": self.players.opponent.stage_bets,
                        "cards": self.players.opponent.hand.items[:],
                        "combo": self.players.opponent.combo,
                        "last_action": self.players.opponent.last_action,
                    },
                }
            })
        return data
