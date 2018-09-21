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


import pytest

from thpoker.core import Card, Deck, Table, Hand, Combo
from thpoker.game import Player, Game
from thpoker import exceptions

from utils import get_parameters


class TestPlayerAction:
    def test_validation(self):
        with pytest.raises(exceptions.PlayerActionKindError):
            Player.Action(kind="wait")
        with pytest.raises(exceptions.PlayerActionKindError):
            Player.Action(kind=15)
        with pytest.raises(exceptions.PlayerActionBetError):
            Player.Action(kind=Player.Action.CHECK, bet="123")
        with pytest.raises(exceptions.PlayerActionBetError):
            Player.Action(kind=Player.Action.CALL, bet=-123)


class TestPlayer:
    def test_initial(self):
        player = Player("Johny")
        assert player.identifier == "Johny"
        assert player.chips == 0
        assert player.round_bets == 0
        assert player.stage_bets == 0
        assert player.last_action == None
        assert player.abilities[Player.Action.RAISE]["min"] == 0
        assert player.abilities[Player.Action.RAISE]["max"] == 0
        assert player.abilities[Player.Action.CALL] == 0
        assert player.abilities[Player.Action.CHECK] == False
        assert player.dif == 0
        assert player.combo == None
        assert player.with_allin == False

    def test_get_chips(self):
        player = Player("Johny")
        assert player.chips == 0
        player.get_chips(50)
        assert player.chips == 50
        player.get_chips(100)
        assert player.chips == 150
        player.get_chips(250)
        assert player.chips == 400

    def test_get_cards(self):
        player = Player("Johny")
        deck = Deck()
        assert len(player.hand.items) == 0
        assert len(deck.cards) == 52
        player.get_cards(deck)
        assert len(player.hand.items) == 2
        assert len(deck.cards) == 50

    def test_get_combo(self):
        player = Player("Johny")
        player.hand = Hand("Ac/Kc")
        table = Table("Qc/Jc/Tc")
        combo = player.get_combo(table)
        assert combo.type == Combo.STRAIGHT_FLUSH
        assert player.combo.type == Combo.STRAIGHT_FLUSH

    def test_abilities(self):
        player = Player("Johny")
        player.get_chips(500)
        player.get_dif(max_round_bet=100)
        assert player.dif == 100
        player.get_abilities()
        assert player.abilities[Player.Action.RAISE]["min"] == 101
        assert player.abilities[Player.Action.RAISE]["max"] == 500
        assert player.abilities[Player.Action.CALL] == 100
        assert player.abilities[Player.Action.CHECK] == False
        assert not player.has_ability[Player.Action.RAISE](50)
        assert not player.has_ability[Player.Action.RAISE](100)
        assert player.has_ability[Player.Action.RAISE](101)
        assert player.has_ability[Player.Action.RAISE](217)
        assert player.has_ability[Player.Action.RAISE](500)
        assert not player.has_ability[Player.Action.RAISE](501)
        assert not player.has_ability[Player.Action.RAISE](673)
        assert player.has_ability[Player.Action.CALL]()
        assert not player.has_ability[Player.Action.CHECK]()

    def test_raise(self):
        player = Player("Johny")
        player.get_chips(300)
        player.get_abilities()
        context = player.action(Player.Action.RAISE, 175)
        assert context.success
        assert player.chips == 125
        assert player.stage_bets == 175
        assert player.round_bets == 175
        player.get_abilities()
        context = player.action(Player.Action.RAISE, 240)
        assert not context.success
        player.get_chips(500)
        player.get_dif(max_round_bet=420)
        player.get_abilities()
        context = player.action(Player.Action.RAISE, 240)
        assert not context.success
        context = player.action(Player.Action.RAISE, 425)
        assert context.success
        assert player.chips == 200
        assert player.stage_bets == 600
        assert player.round_bets == 600
        player.get_dif(max_round_bet=990)
        player.get_abilities()
        context = player.action(Player.Action.RAISE, 200)
        assert not context.success
        player.get_dif(max_round_bet=700)
        player.get_abilities()
        context = player.action(Player.Action.RAISE, 200)
        assert context.success
        assert player.chips == 0
        assert player.stage_bets == 800
        assert player.round_bets == 800
        assert player.with_allin

    def test_call(self):
        player = Player("Johny")
        player.get_chips(800)
        player.get_dif(max_round_bet=280)
        player.get_abilities()
        context = player.action(Player.Action.CALL)
        assert context.success
        assert player.chips == 520
        assert player.stage_bets == 280
        assert player.round_bets == 280
        player.get_dif(max_round_bet=1000)
        player.get_abilities()
        context = player.action(Player.Action.CALL)
        assert context.success
        assert player.chips == 0
        assert player.stage_bets == 800
        assert player.round_bets == 800
        assert player.with_allin
        player.get_abilities()
        context = player.action(Player.Action.CALL)
        assert not context.success

    def test_check(self):
        player = Player("Johny")
        player.get_chips(100)
        player.stage_bets = 200
        player.round_bets = 300
        player.get_dif(max_round_bet=300)
        player.get_abilities()
        context = player.action(Player.Action.CHECK)
        assert context.success
        assert player.chips == 100
        assert player.stage_bets == 200
        assert player.round_bets == 300
        player.get_dif(max_round_bet=350)
        player.get_abilities()
        context = player.action(Player.Action.CHECK)
        assert not context.success

    def test_fold(self):
        player = Player("Johny")
        player.get_chips(700)
        player.stage_bets = 140
        player.round_bets = 270
        player.get_abilities()
        context = player.action(Player.Action.FOLD)
        assert context.success
        assert player.chips == 700
        player.get_dif(max_round_bet=350)
        player.get_abilities()
        context = player.action(Player.Action.FOLD)
        assert context.success
        assert player.chips == 700
        player.get_dif(max_round_bet=1350)
        player.get_abilities()
        context = player.action(Player.Action.FOLD)
        assert context.success
        assert player.chips == 700

    def test_blind_bet(self):
        player = Player("Johny")
        player.get_chips(100)
        context = player.action(Player.Action.BLIND_BET, 40)
        assert context.success
        assert player.chips == 60
        assert player.stage_bets == 40
        assert player.round_bets == 40
        player.stage_bets = 0
        player.round_bets = 0
        context = player.action(Player.Action.BLIND_BET, 200)
        assert context.success
        assert player.chips == 0
        assert player.stage_bets == 60
        assert player.round_bets == 60
        assert player.with_allin


class TestGamePlayers:
    def get_players(test_method):
        def wrap(self):
            first = Player("first")
            second = Player("second")
            third = Player("third")
            fourth = Player("fourth")
            players = Game.Players(1000, first, second, third, fourth)
            test_method(self, players, first, second, third, fourth)
        return wrap

    def test_validation(self):
        with pytest.raises(exceptions.GamePlayersChipsError):
            Game.Players("1000", Player("Johny"), Player("Harry"))
        with pytest.raises(exceptions.GamePlayersChipsError):
            Game.Players(-1000, Player("Johny"), Player("Harry"))
        with pytest.raises(exceptions.GamePlayersPlayersError):
            Game.Players(1000, Player("Johny"))
        with pytest.raises(exceptions.GamePlayersPlayersError):
            Game.Players(1000, *(Player(i) for i in range(11)))

    def test_initial(self):
        players = Game.Players(1000, Player("Johny"), Player("Harry"))
        assert players._order in ([0, 1], [1, 0])
        assert players._order == players._involved_order
        assert players._current_index == 0
        assert players._max_round_bet == 0
        for player in players:
            assert player.chips == 1000

    @get_players
    def test_order(self, players, first, second, third, fourth):
        players._order = [0, 1, 2, 3]
        players._involved_order = players._order[:]
        assert players.current is first
        assert players.next_player() == 1
        assert players.current is second
        assert players.next_player() == 2
        assert players.current is third
        assert players.next_player() == 3
        assert players.current is fourth
        assert players.current_is_last
        assert players.next_player() == 0
        players.change_order()
        assert players._current_index == 0
        assert players.current is second

    @get_players
    def test_get_blindes(self, players, first, second, third, fourth):
        players._order = [0, 1, 2, 3]
        players._involved_order = players._order[:]
        context = players.get_blindes(10, 20)
        assert context.success
        assert first.stage_bets == 0
        assert first.round_bets == 0
        assert second.stage_bets == 0
        assert second.round_bets == 0
        assert third.stage_bets == 10
        assert third.round_bets == 10
        assert fourth.stage_bets == 20
        assert fourth.round_bets == 20
        assert players._current_index == 0

    @get_players
    def test_action(self, players, first, second, third, fourth):
        players._order = [0, 1, 2, 3]
        players._involved_order = [0, 1, 2, 3]
        assert not players.have_dif
        assert players.bank == 0
        assert players.rolling_count == 4
        assert players.involved_count == 4
        for i in range(3):
            players.get_current_dif()
            assert players.current.dif == i * 20
            players.get_current_abilities()
            assert players.current.abilities[Player.Action.RAISE]["min"] == i * 20 + 1
            assert players.current.abilities[Player.Action.RAISE]["max"] == 1000
            assert players.current.abilities[Player.Action.CALL] == i * 20
            if i:
                assert players.current.abilities[Player.Action.CHECK] == False
            context = players.action(Player.Action.RAISE, (i + 1) * 20)
            assert context.success
            assert players.next_player() == i + 1
        assert players.have_dif
        assert players.bank == 120
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.CALL)
        assert context.success
        assert players.next_player() == 0
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.FOLD)
        assert context.success
        assert players.next_player(after_fold=True) == 0
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.FOLD)
        assert context.success
        assert players.next_player(after_fold=True) == 0
        assert players.rolling_count == 4
        assert players.involved_count == 2
        assert players.bank == 180

    @get_players
    def test_global_allin(self, players, first, second, third, fourth):
        assert not players.global_allin
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.RAISE, 1000)
        assert context.success
        assert not players.global_allin
        players.next_player()
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.FOLD)
        assert context.success
        assert not players.global_allin
        players.next_player(after_fold=True)
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.CALL)
        assert context.success
        assert not players.global_allin
        players.next_player()
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.CALL)
        assert context.success
        assert players.global_allin

    @get_players
    def test_get_result_rank(self, players, first, second, third, fourth):
        first.hand.items = [Card("Ac"), Card("Ad")]
        second.hand.items = [Card("6s"), Card("7s")]
        third.hand.items = [Card("Tc"), Card("6d")]
        fourth.hand.items = [Card("Qs"), Card("8d")]
        table = Table("5s/Qd/7d/8c/4s")
        winners, loosers = players._get_result_rank(table)
        assert first in loosers
        assert second in winners
        assert third in winners
        assert fourth in loosers

    @get_players
    def test_get_result(self, players, first, second, third, fourth):
        first.chips = 1200
        second.chips = 500
        third.chips = 800
        fourth.chips = 1500
        players._order = [0, 1, 2, 3]
        players._involved_order = [0, 1, 2, 3]
        first.hand.items = [Card("5c"), Card("2h")]
        second.hand.items = [Card("8h"), Card("Kh")]
        third.hand.items = [Card("5d"), Card("2d")]
        fourth.hand.items = [Card("5s"), Card("2c")]
        table = Table("3d/7h/Ad/4s/Jc")
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.RAISE, 200)
        assert context.success
        players.next_player()
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.CALL)
        assert context.success
        players.next_player()
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.RAISE, 800)
        assert context.success
        players.next_player()
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.CALL)
        assert context.success
        players.next_player()
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.CALL)
        assert context.success
        players.next_player()
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.CALL)
        assert context.success
        data = players.get_result(table)
        assert data["winners"]["first"] == 967
        assert data["loosers"]["second"] == 500
        assert data["winners"]["third"] == 967
        assert data["winners"]["fourth"] == 966
        assert players._order == [0, 2, 3]
        assert first.chips == 1367
        assert second.chips == 0
        assert third.chips == 967
        assert fourth.chips == 1666

    @get_players
    def test_get_result_with_fold_and_across_allin(self, players, first, second, third, fourth):
        first.chips = 750
        second.chips = 1100
        third.chips = 400
        fourth.chips = 1750
        players._order = [0, 1, 2, 3]
        players._involved_order = [0, 1, 2, 3]
        first.hand.items = [Card("Qs"), Card("Td")]
        second.hand.items = [Card("Th"), Card("4d")]
        third.hand.items = [Card("Tc"), Card("7c")]
        fourth.hand.items = [Card("Ad"), Card("As")]
        table = Table("Qh/3s/Ah/Jh/Kh")
        assert players._current_index == 0
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.RAISE, 100)
        assert context.success
        players.next_player()
        assert players._current_index == 1
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.FOLD)
        assert context.success
        players.next_player(after_fold=True)
        assert players._current_index == 1
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.RAISE, 400)
        assert context.success
        print(players.current.identifier)
        print(players.current.with_allin)
        print(players.current.chips)
        players.next_player()
        assert players._current_index == 2
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.CALL)
        assert context.success
        players.next_player()
        assert players._current_index == 0
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.RAISE, 650)
        assert context.success
        players.next_player()
        assert players._current_index == 2
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.CALL)
        assert context.success
        data = players.get_result(table)
        assert data["winners"]["first"] == 1240
        assert data["winners"]["third"] == 660
        assert data["loosers"]["fourth"] == 750
        assert first.chips == 1240
        assert second.chips == 1100
        assert third.chips == 660
        assert fourth.chips == 1000


class TestGameStage:
    def test_complex(self):
        stage = Game.Stage()
        assert stage.name == Game.Stage.PRE_FLOP
        assert stage.table_size == 0
        assert stage.depth_count == 0
        stage.next()
        assert stage.name == Game.Stage.FLOP
        assert stage.table_size == 3
        stage.depth_increase()
        assert stage.depth_count == 1
        stage.next()
        assert stage.name == Game.Stage.TURN
        assert stage.table_size == 4
        assert stage.depth_count == 0
        stage.next()
        assert stage.name == Game.Stage.RIVER
        assert stage.table_size == 5
        stage.depth_increase()
        assert stage.depth_count == 1
