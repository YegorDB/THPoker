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
            return f"{self.kind} {self.bet or ''}".strip()


    def __init__(self, identifier):
        self.identifier = identifier
        self.chips = 0
        self.round_bets = 0
        self.stage_bets = 0
        self.last_action = None
        self.abilities = {
            self.Action.RAISE: 0,
            self.Action.CALL: 0,
            self.Action.CHECK: False,
        }
        self.has_ability = {
            self.Action.RAISE: lambda bet: self.abilities[self.Action.RAISE] >= bet,
            self.Action.CALL: lambda: self.abilities[self.Action.CALL] > 0,
            self.Action.CHECK: lambda: self.abilities[self.Action.CHECK],
        }
        self.dif = 0 # difference beetwen player's round bets and max bets of current round
        self.combo = None
        self.hand = Hand()
        self.with_allin = False

    def get_chips(self, chips):
        self.chips += chips

    def get_combo(self, table):
        self.combo = Combo(table=table, hand=self.hand)
        return self.combo

    def new_round(self):
        self.round_bets = 0
        self.combo = None
        self.hand.clean()
        self.with_allin = False

    def new_stage(self):
        self.stage_bets = 0
        self.dif = 0
        self.refresh_last_action()

    def refresh_last_action(self):
        self.last_action = None

    def get_abilities(self):
        self.abilities[self.Action.RAISE] = self.chips if self.chips > self.dif else 0
        if self.dif:
            self.abilities[self.Action.CALL] = self.chips if self.dif >= self.chips else self.dif
            self.abilities[self.Action.CHECK] = False
        else:
            self.abilities[self.Action.CALL] = 0
            self.abilities[self.Action.CHECK] = True

    def get_dif(self, max_round_bets):
        self.dif = max_round_bets - self.round_bets

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

    def _with_bet_action(bet, action_kind):
        if self.chips > bet:
            self.last_action = self.Action(action_kind, bet)
            self._betting(bet)
        else:
            self._all_in()

    def _raise(self, bet):
        self._with_bet_action(bet, self.Action.RAISE)

    def _call(self):
        self._with_bet_action(self.dif, self.Action.CALL)

    def _check(self):
        self.last_action = self.Action(self.Action.CHECK)

    def _blind_bet(self, bet):
        self._with_bet_action(bet, self.Action.BLIND_BET)

    def _fold(self):
        self.last_action = self.Action(self.Action.FOLD)

    def _all_in(self):
        self.last_action = self.Action(self.Action.ALL_IN, self.chips)
        self._betting(self.chips)
        self.with_allin = True


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
            self._order = self._get_order(len(players))
            self._involved_order = self._order[:]
            self._curent_index = 0 # active player's index
            for player in self:
                player.get_chips(chips)

        def __getitem__(self, key):
            return self._scroll[self._involved_order[key]]

        def _get_order(self, players_count):
            return random.sample(range(players_count), players_count)

        def new_round(self):
            for player in self:
                player.new_round()

        def new_stage(self):
            for player in self:
                player.new_stage()
            self._curent_index = 0

        def action(self, kind, bet):
            for player in self:
                player.refresh_last_action() # really need?
            return self.current.action(kind, bet)

        @property
        def current(self): # active player
            return self[self._curent_index]

        def _get_next_index(self):
            return self._curent_index + 1 if self._curent_index < len(self._involved_order) - 1 else 0

        def next_player(self): # transition move rights
            self._curent_index = self._get_next_index()
            return self._curent_index

        def change_order(self):
            self._order = self._order[1:] + self._order[0]
            self._involved_order = self._order[:]

        def get_dif(self):
            max_round_bets = max([player.round_bets for player in self])
            self.current.get_dif(max_round_bets)

        @property
        def have_dif(self):
            max_round_bets = max([player.round_bets for player in self])
            next_index = self._get_next_index()
            self[next_index].get_dif(max_round_bets)
            if self[next_index].dif and self[next_index].chips:
                return True
            for index in self._involved_order:
                if index in (self._curent_index, next_index):
                    continue
                self[index].get_dif(max_round_bets)
                if self[index].dif and self[index].chips:
                    return True
            return False

        @property
        def current_is_last(self):
            return self._get_next_index() == 0

        def get_cards(self, deck):
            for player in self:
                player.hand.pull(deck)

        @property
        def bank(self):
            return sum((player.round_bets for player in self))

        @property
        def max_opponents_chips(self):
            max_chips = 0
            for index in self._involved_order:
                if index == self._curent_index:
                    continue
                if self[index].chips > max_chips:
                    max_chips = self[index].chips
            return max_chips

        @property
        def involved_count(self):
            return len(self._involved_order)

        @property
        def with_allin_count(self):
            return len(tuple(filter(lambda p: p.with_allin, self)))

        def get_fold(self):
            self._involved_order.pop(self._curent_index)
            if len(self._involved_order) == 1:
                self[self._involved_order[0]].get_chips(self.bank)

        def _get_result_rank(self, table):
            rank = {"winners": [], "loosers": []}
            best_combo = None
            for player in self:
                combo = player.combo or player.get_combo(table)
                if best_combo:
                    if combo > best_combo:
                        best_combo = combo
                        rank["loosers"] += rank["winners"]
                        rank["winners"] = [player]
                    elif combo == best_combo:
                        rank["winners"].append(player)
                    else:
                        rank["loosers"].append(player)
                else:
                    best_combo = combo
                    rank["winners"] = [player]
            return rank

        def _get_result_data(self, winners, loosers):
            data = {"winners": {}, "loosers": {}}
            winners_bets = sum((p.round_bets for p in winners))
            all_bets = self.bank
            for looser in loosers:
                data["loosers"][looser.identifier] = looser.round_bets
                if looser.round_bets > winners_bets:
                    over_bet = looser.round_bets - winners_bets
                    all_bets -= over_bet
                    looser.get_chips(over_bet)
                    data["loosers"][looser.identifier] -= over_bet
            gain_bets = all_bets - winners_bets
            for winner in winners:
                gain = winner.round_bets + int(gain_bets * winner.round_bets / winners_bets)
                winner.get_chips(gain)
                data["winners"][winner.identifier] = gain
            getted_gain = sum(data["winners"].values())
            if getted_gain < gain_bets:
                for i in range(gain_bets - getted_gain):
                    winners[i].get_chips(1)
                    data["winners"][winners[i].identifier] += 1
            return data

        def get_result(self, table):
            return self._get_result_data(**self._get_result_rank(table))


    class Stage:
        PRE_FLOP = 'pre_flop'
        FLOP = 'flop'
        TURN = 'turn'
        RIVER = 'river'
        ALL = (PRE_FLOP, FLOP, TURN, RIVER)

        def __init__(self):
            self._started = False
            self._index = 0 # current stage index
            self._depth = 0 # players moves count per stage

        @property
        def name(self):
            return self.ALL[self._index]

        @property
        def table_size(self):
            return self._index + 2 if self._index else 0

        @property
        def depth_count(self):
            return self._depth

        def next(self):
            if self._started:
                self._index += 1
                self._depth = 0
            else:
                self._started = True

        def depth_increase(self):
            self._depth += 1


    def __init__(self, settings, *players):
        self._players_count = len(players)
        self._players = self.Players(settings["chips"], *players)
        self._blindes = settings["blindes"]
        self._state = self.NORMAL
        self._table = Table()
        self._deck = Deck()
        self._result = None

    @property
    def global_allin(self):
        return self._players.involved_count <= self._players.with_allin_count + 1

    def new_round(self):
        if self._state == self.THE_END:
            return Context(success=False, description="Game over.", **self._get_context_data(self.THE_END))
        self._players.new_round()
        self._table.clean()
        self._deck.refresh()
        self._state = self.NORMAL
        self._stage = self.Stage()
        self._result = None
        return Context(
            success=True,
            description="Redy to start new stage.",
            **self._get_context_data(self.STAGE_NEEDED))

    def new_stage(self):
        if self._state in (self.SHOW_DOWN, self.FOLD):
            return Context(success=False, description="Round over.", **self._get_context_data(self.ROUND_NEEDED))
        self._stage.next()
        self._players.new_stage()
        if self._players_count == 2 and self._stage.name == self.Stage.FLOP:
            self._players.change_order()
        self._distribution()
        if self._state != self.ALL_IN or \
            self._stage.name == self.Stage.PRE_FLOP and \
                self._players.current.chips and \
                    self._players.current.stage_bets < self._players.max_opponents_chips:
            self._players.get_dif()
            return Context(
                success=True,
                description="Redy to accept action.",
                **self._get_context_data(self.ACTION_NEEDED, True))
        elif self._stage.name == self.Stage.RIVER:
            return self._show_down()
        return self._stage_end()

    def _distribution(self):
        if self._stage.name == self.Stage.PRE_FLOP:
            self._get_blindes()
            self._players.get_cards(self._deck)
        else:
            self._table.pull_to(self._deck, self._stage.table_size)

    def _get_blindes(self):
        for bet, index in zip(self._blindes, (-2, -1)):
            player = self._players[index]
            player.action(Player.Action.BLIND_BET, bet)
            if player.last_action.kind == Player.Action.ALL_IN and self.global_allin:
                self._state = self.ALL_IN

    def action(self, kind, bet=0):
        action_result = self._players.action(kind, bet)
        if not action_result.success:
            return action_result
        if self._players.current.last_action.kind == Player.Action.FOLD:
            self._state = self.FOLD
            self._players.get_fold()
            if self._players.involved_count == 1:
                return self._stage_end()
        if self._players.current.last_action.kind == Player.Action.ALL_IN and self.global_allin:
            self._state = self.ALL_IN
        if self._players.have_dif or not self._players.current_is_last and self._stage.depth_count == 0:
            current_index = self._players.next_player()
            if current_index == 0:
                self._stage.depth_increase()
            self._players.current.get_abilities()
            return Context(
                success=True,
                description="Redy to accept action.",
                **self._get_context_data(self.ACTION_NEEDED, True))
        elif self._stage.name == self.Stage.RIVER:
            return self._show_down()
        return self._stage_end()

    def _show_down(self):
        self._result = self._players.get_result(self._table)
        self._state = self.THE_END if self._the_end else self.SHOW_DOWN
        return self._stage_end()

    def _stage_end(self):
        if self._stage.name == self.Stage.PRE_FLOP and self._state == self.FOLD:
            self._players.change_order()
        if self._state == self.THE_END:
            point = self.THE_END
            description = "Game has been ended."
        elif self._state in (self.SHOW_DOWN, self.FOLD):
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
        for player in self._players:
            if player.chips == 0:
                return True
        return False

    def _get_context_data(self, point, additional=False):
        data = {"point": point}
        if additional:
            data.update({
                "table": self._table.items[:],
                "state": self._state,
                "stage_name": self._stage.name,
                "stage_depth": self._stage.depth_count,
                "bank": self._players.bank,
                "result": self._result,
                "players": {
                    "current": {
                        "identifier": self._players.current.identifier,
                        "chips": self._players.current.chips,
                        "stage_bets": self._players.current.stage_bets,
                        "round_bets": self._players.current.round_bets,
                        "dif": self._players.current.dif,
                        "abilities": self._players.current.abilities,
                        "cards": self._players.current.hand.items[:],
                        "hand_type": self._players.current.hand.type,
                        "combo": self._players.current.combo,
                        "last_action": self._players.current.last_action,
                    },
                    "opponent": {
                        "identifier": self._players.opponent.identifier,
                        "chips": self._players.opponent.chips,
                        "stage_bets": self._players.opponent.stage_bets,
                        "cards": self._players.opponent.hand.items[:],
                        "combo": self._players.opponent.combo,
                        "last_action": self._players.opponent.last_action,
                    },
                }
            })
        return data
