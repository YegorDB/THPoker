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
        assert players.next_player() == (1, True)
        assert players.current is second
        assert players.next_player() == (2, True)
        assert players.current is third
        assert players.next_player() == (3, True)
        assert players.current is fourth
        assert players.next_player() == (0, True)
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
            assert players.next_player() == (i + 1, True)
        assert players.have_dif
        assert players.bank == 120
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.CALL)
        assert context.success
        assert players.next_player() == (0, True)
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.FOLD)
        assert context.success
        assert players.next_player() == (0, False)
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.FOLD)
        assert context.success
        assert players.next_player() == (0, False)
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
        players.next_player()
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
        assert players.active_count == 3
        players.remove_inactive()
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
        players.next_player()
        assert players._current_index == 1
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.RAISE, 400)
        assert context.success
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
        assert data["winners"]["first"] == 1300
        assert data["winners"]["third"] == 600
        assert data["loosers"]["fourth"] == 750
        assert first.chips == 1300
        assert second.chips == 1100
        assert third.chips == 600
        assert fourth.chips == 1000

    @get_players
    def test_get_result_with_overbet(self, players, first, second, third, fourth):
        first.chips = 300
        second.chips = 600
        third.chips = 1400
        fourth.chips = 1700
        players._order = [0, 1, 2, 3]
        players._involved_order = [0, 1, 2, 3]
        first.hand.items = [Card("Qh"), Card("Ah")]
        second.hand.items = [Card("9d"), Card("Ts")]
        third.hand.items = [Card("Tc"), Card("Js")]
        fourth.hand.items = [Card("Ad"), Card("2d")]
        table = Table("Ks/6c/6h/Td/2c")
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.RAISE, 300)
        assert context.success
        players.next_player()
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.RAISE, 600)
        assert context.success
        players.next_player()
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.RAISE, 1400)
        assert context.success
        players.next_player()
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.RAISE, 1700)
        assert context.success
        data = players.get_result(table)
        assert data["loosers"]["first"] == 300
        assert data["winners"]["second"] == 1050
        assert data["winners"]["third"] == 2650
        assert data["loosers"]["fourth"] == 1400
        assert players.active_count == 3
        players.remove_inactive()
        assert players._order == [1, 2, 3]
        assert first.chips == 0
        assert second.chips == 1050
        assert third.chips == 2650
        assert fourth.chips == 300

    @get_players
    def test_get_result_with_one_winner(self, players, first, second, third, fourth):
        first.chips = 1500
        second.chips = 800
        third.chips = 400
        fourth.chips = 1300
        players._order = [0, 1, 2, 3]
        players._involved_order = [0, 1, 2, 3]
        first.hand.items = [Card("Js"), Card("Jd")]
        second.hand.items = [Card("6h"), Card("7h")]
        third.hand.items = [Card("Kd"), Card("7c")]
        fourth.hand.items = [Card("7s"), Card("2c")]
        table = Table("9d/Jc/8d/8s/Tc")
        players.get_current_dif()
        players.get_current_abilities()
        context = players.action(Player.Action.RAISE, 1500)
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
        assert data["winners"]["first"] == 4000
        assert data["loosers"]["second"] == 800
        assert data["loosers"]["third"] == 400
        assert data["loosers"]["fourth"] == 1300
        assert players.active_count == 1
        players.remove_inactive()
        assert players._order == [0]
        assert first.chips == 4000
        assert second.chips == 0
        assert third.chips == 0
        assert fourth.chips == 0


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


class TestGame:
    def test_validation(self):
        players_box = (Player(1), Player(2))
        with pytest.raises(exceptions.GameMissedSettingsError):
            Game({"chips": 1000}, *players_box)
        with pytest.raises(exceptions.GameMissedSettingsError):
            Game({"blindes": [10, 20]}, *players_box)
        with pytest.raises(exceptions.GameWrongBlindesSettingError):
            Game({"chips": 1000, "blindes": (10, 20)}, *players_box)
        with pytest.raises(exceptions.GameWrongBlindesSettingError):
            Game({"chips": 1000, "blindes": [10, 20, 30]}, *players_box)
        with pytest.raises(exceptions.GameWrongBlindesSettingError):
            Game({"chips": 1000, "blindes": ["10", 20]}, *players_box)
        with pytest.raises(exceptions.GameWrongBlindesSettingError):
            Game({"chips": 1000, "blindes": [10, "20"]}, *players_box)
        with pytest.raises(exceptions.GameWrongBlindesSettingError):
            Game({"chips": 1000, "blindes": [-10, 20]}, *players_box)
        with pytest.raises(exceptions.GameWrongBlindesSettingError):
            Game({"chips": 1000, "blindes": [10, -20]}, *players_box)
        with pytest.raises(exceptions.GameWrongBlindesSettingError):
            Game({"chips": 1000, "blindes": [20, 10]}, *players_box)

    def test_play(self):
        game = Game(
            {"chips": 1000, "blindes": [10, 20]},
            *(Player(i) for i in range(4)),
        )
        game._players._order = [3, 0, 1, 2]
        game._players._involved_order = [3, 0, 1, 2]
        assert not game.new_stage().success
        assert not game.action(Player.Action.CALL).success

        context = game.new_round()
        assert game._players._order == [0, 1, 2, 3]
        assert game._players._involved_order == [0, 1, 2, 3]
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 0
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.PRE_FLOP, "depth": 0}
        assert context.bank == 30
        assert context.result == None
        assert context.last_action == {"identifier": 3, "kind": Player.Action.BLIND_BET, "bet": 20}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 1000
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 0
        assert context.players[0]["dif"] == 20
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 21, "max": 1000},
            Player.Action.CALL: 20,
            Player.Action.CHECK: False,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[1]["chips"] == 1000
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 0
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 990
        assert context.players[2]["stage_bets"] == 10
        assert context.players[2]["round_bets"] == 10
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 10}

        assert context.players[3]["chips"] == 980
        assert context.players[3]["stage_bets"] == 20
        assert context.players[3]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[3]["dif"]
        with pytest.raises(KeyError):
            context.players[3]["abilities"]
        assert len(context.players[3]["cards"]) == 2
        assert context.players[3]["combo"] is None
        assert context.players[3]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 20}

        #####################################################
        #####################################################
        #####################################################

        game._players[0].hand.items = [Card("As"), Card("Ad")]
        game._players[1].hand.items = [Card("3c"), Card("9h")]
        game._players[2].hand.items = [Card("7d"), Card("8d")]
        game._players[3].hand.items = [Card("Js"), Card("Tc")]

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.RAISE, 80)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 0
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.PRE_FLOP, "depth": 0}
        assert context.bank == 110
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.RAISE, "bet": 80}
        assert context.current_player == 1

        assert context.players[0]["chips"] == 920
        assert context.players[0]["stage_bets"] == 80
        assert context.players[0]["round_bets"] == 80
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.RAISE, "bet": 80}

        assert context.players[1]["chips"] == 1000
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 0
        assert context.players[1]["dif"] == 80
        assert context.players[1]["abilities"] == {
            Player.Action.RAISE: {"min": 81, "max": 1000},
            Player.Action.CALL: 80,
            Player.Action.CHECK: False,
        }
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 990
        assert context.players[2]["stage_bets"] == 10
        assert context.players[2]["round_bets"] == 10
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 10}

        assert context.players[3]["chips"] == 980
        assert context.players[3]["stage_bets"] == 20
        assert context.players[3]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[3]["dif"]
        with pytest.raises(KeyError):
            context.players[3]["abilities"]
        assert len(context.players[3]["cards"]) == 2
        assert context.players[3]["combo"] is None
        assert context.players[3]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 20}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.FOLD)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 0
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.PRE_FLOP, "depth": 0}
        assert context.bank == 110
        assert context.result == None
        assert context.last_action == {"identifier": 1, "kind": Player.Action.FOLD, "bet": 0}
        assert context.current_player == 2

        assert context.players[0]["chips"] == 920
        assert context.players[0]["stage_bets"] == 80
        assert context.players[0]["round_bets"] == 80
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.RAISE, "bet": 80}

        assert context.players[2]["chips"] == 990
        assert context.players[2]["stage_bets"] == 10
        assert context.players[2]["round_bets"] == 10
        assert context.players[2]["dif"] == 70
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 71, "max": 990},
            Player.Action.CALL: 70,
            Player.Action.CHECK: False,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 10}

        assert context.players[3]["chips"] == 980
        assert context.players[3]["stage_bets"] == 20
        assert context.players[3]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[3]["dif"]
        with pytest.raises(KeyError):
            context.players[3]["abilities"]
        assert len(context.players[3]["cards"]) == 2
        assert context.players[3]["combo"] is None
        assert context.players[3]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 20}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 0
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.PRE_FLOP, "depth": 0}
        assert context.bank == 180
        assert context.result == None
        assert context.last_action == {"identifier": 2, "kind": Player.Action.CALL, "bet": 70}
        assert context.current_player == 3

        assert context.players[0]["chips"] == 920
        assert context.players[0]["stage_bets"] == 80
        assert context.players[0]["round_bets"] == 80
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.RAISE, "bet": 80}

        assert context.players[2]["chips"] == 920
        assert context.players[2]["stage_bets"] == 80
        assert context.players[2]["round_bets"] == 80
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.CALL, "bet": 70}

        assert context.players[3]["chips"] == 980
        assert context.players[3]["stage_bets"] == 20
        assert context.players[3]["round_bets"] == 20
        assert context.players[3]["dif"] == 60
        assert context.players[3]["abilities"] == {
            Player.Action.RAISE: {"min": 61, "max": 980},
            Player.Action.CALL: 60,
            Player.Action.CHECK: False,
        }
        assert len(context.players[3]["cards"]) == 2
        assert context.players[3]["combo"] is None
        assert context.players[3]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 20}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.STAGE_NEEDED
        assert context.last_action == {"identifier": 3, "kind": Player.Action.CALL, "bet": 60}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.action(Player.Action.CALL).success
        context = game.new_stage()
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 3
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.FLOP, "depth": 0}
        assert context.bank == 240
        assert context.result == None
        assert context.last_action == {"identifier": 3, "kind": Player.Action.CALL, "bet": 60}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 920
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 80
        assert context.players[0]["dif"] == 0
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 920},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[2]["chips"] == 920
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 80
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] is None

        assert context.players[3]["chips"] == 920
        assert context.players[3]["stage_bets"] == 0
        assert context.players[3]["round_bets"] == 80
        with pytest.raises(KeyError):
            context.players[3]["dif"]
        with pytest.raises(KeyError):
            context.players[3]["abilities"]
        assert len(context.players[3]["cards"]) == 2
        assert context.players[3]["combo"] is None
        assert context.players[3]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        game._table.items = [Card("Jd"), Card("8s"), Card("3d")]

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CHECK)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 3
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.FLOP, "depth": 0}
        assert context.bank == 240
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.CHECK, "bet": 0}
        assert context.current_player == 2

        assert context.players[0]["chips"] == 920
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 80
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[2]["chips"] == 920
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 80
        assert context.players[2]["dif"] == 0
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 920},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] is None

        assert context.players[3]["chips"] == 920
        assert context.players[3]["stage_bets"] == 0
        assert context.players[3]["round_bets"] == 80
        with pytest.raises(KeyError):
            context.players[3]["dif"]
        with pytest.raises(KeyError):
            context.players[3]["abilities"]
        assert len(context.players[3]["cards"]) == 2
        assert context.players[3]["combo"] is None
        assert context.players[3]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CHECK)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 3
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.FLOP, "depth": 0}
        assert context.bank == 240
        assert context.result == None
        assert context.last_action == {"identifier": 2, "kind": Player.Action.CHECK, "bet": 0}
        assert context.current_player == 3

        assert context.players[0]["chips"] == 920
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 80
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[2]["chips"] == 920
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 80
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[3]["chips"] == 920
        assert context.players[3]["stage_bets"] == 0
        assert context.players[3]["round_bets"] == 80
        assert context.players[3]["dif"] == 0
        assert context.players[3]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 920},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[3]["cards"]) == 2
        assert context.players[3]["combo"] is None
        assert context.players[3]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.RAISE, 180)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 3
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.FLOP, "depth": 1}
        assert context.bank == 420
        assert context.result == None
        assert context.last_action == {"identifier": 3, "kind": Player.Action.RAISE, "bet": 180}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 920
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 80
        assert context.players[0]["dif"] == 180
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 181, "max": 920},
            Player.Action.CALL: 180,
            Player.Action.CHECK: False,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[2]["chips"] == 920
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 80
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[3]["chips"] == 740
        assert context.players[3]["stage_bets"] == 180
        assert context.players[3]["round_bets"] == 260
        with pytest.raises(KeyError):
            context.players[3]["dif"]
        with pytest.raises(KeyError):
            context.players[3]["abilities"]
        assert len(context.players[3]["cards"]) == 2
        assert context.players[3]["combo"] is None
        assert context.players[3]["last_action"] == {"kind": Player.Action.RAISE, "bet": 180}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 3
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.FLOP, "depth": 1}
        assert context.bank == 600
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.CALL, "bet": 180}
        assert context.current_player == 2

        assert context.players[0]["chips"] == 740
        assert context.players[0]["stage_bets"] == 180
        assert context.players[0]["round_bets"] == 260
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.CALL, "bet": 180}

        assert context.players[2]["chips"] == 920
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 80
        assert context.players[2]["dif"] == 180
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 181, "max": 920},
            Player.Action.CALL: 180,
            Player.Action.CHECK: False,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[3]["chips"] == 740
        assert context.players[3]["stage_bets"] == 180
        assert context.players[3]["round_bets"] == 260
        with pytest.raises(KeyError):
            context.players[3]["dif"]
        with pytest.raises(KeyError):
            context.players[3]["abilities"]
        assert len(context.players[3]["cards"]) == 2
        assert context.players[3]["combo"] is None
        assert context.players[3]["last_action"] == {"kind": Player.Action.RAISE, "bet": 180}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.STAGE_NEEDED
        assert context.last_action == {"identifier": 2, "kind": Player.Action.CALL, "bet": 180}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.action(Player.Action.CALL).success
        context = game.new_stage()
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 4
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.TURN, "depth": 0}
        assert context.bank == 780
        assert context.result == None
        assert context.last_action == {"identifier": 2, "kind": Player.Action.CALL, "bet": 180}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 740
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 260
        assert context.players[0]["dif"] == 0
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 740},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[2]["chips"] == 740
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 260
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] is None

        assert context.players[3]["chips"] == 740
        assert context.players[3]["stage_bets"] == 0
        assert context.players[3]["round_bets"] == 260
        with pytest.raises(KeyError):
            context.players[3]["dif"]
        with pytest.raises(KeyError):
            context.players[3]["abilities"]
        assert len(context.players[3]["cards"]) == 2
        assert context.players[3]["combo"] is None
        assert context.players[3]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        game._table.items = [Card("Jd"), Card("8s"), Card("3d"), Card("Td")]

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CHECK)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 4
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.TURN, "depth": 0}
        assert context.bank == 780
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.CHECK, "bet": 0}
        assert context.current_player == 2

        assert context.players[0]["chips"] == 740
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 260
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[2]["chips"] == 740
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 260
        assert context.players[2]["dif"] == 0
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 740},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] is None

        assert context.players[3]["chips"] == 740
        assert context.players[3]["stage_bets"] == 0
        assert context.players[3]["round_bets"] == 260
        with pytest.raises(KeyError):
            context.players[3]["dif"]
        with pytest.raises(KeyError):
            context.players[3]["abilities"]
        assert len(context.players[3]["cards"]) == 2
        assert context.players[3]["combo"] is None
        assert context.players[3]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CHECK)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 4
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.TURN, "depth": 0}
        assert context.bank == 780
        assert context.result == None
        assert context.last_action == {"identifier": 2, "kind": Player.Action.CHECK, "bet": 0}
        assert context.current_player == 3

        assert context.players[0]["chips"] == 740
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 260
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[2]["chips"] == 740
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 260
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[3]["chips"] == 740
        assert context.players[3]["stage_bets"] == 0
        assert context.players[3]["round_bets"] == 260
        assert context.players[3]["dif"] == 0
        assert context.players[3]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 740},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[3]["cards"]) == 2
        assert context.players[3]["combo"] is None
        assert context.players[3]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.RAISE, 400)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 4
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.TURN, "depth": 1}
        assert context.bank == 1180
        assert context.result == None
        assert context.last_action == {"identifier": 3, "kind": Player.Action.RAISE, "bet": 400}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 740
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 260
        assert context.players[0]["dif"] == 400
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 401, "max": 740},
            Player.Action.CALL: 400,
            Player.Action.CHECK: False,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[2]["chips"] == 740
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 260
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[3]["chips"] == 340
        assert context.players[3]["stage_bets"] == 400
        assert context.players[3]["round_bets"] == 660
        with pytest.raises(KeyError):
            context.players[3]["dif"]
        with pytest.raises(KeyError):
            context.players[3]["abilities"]
        assert len(context.players[3]["cards"]) == 2
        assert context.players[3]["combo"] is None
        assert context.players[3]["last_action"] == {"kind": Player.Action.RAISE, "bet": 400}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.FOLD)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 4
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.TURN, "depth": 1}
        assert context.bank == 1180
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.FOLD, "bet": 0}
        assert context.current_player == 2

        assert context.players[2]["chips"] == 740
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 260
        assert context.players[2]["dif"] == 400
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 401, "max": 740},
            Player.Action.CALL: 400,
            Player.Action.CHECK: False,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[3]["chips"] == 340
        assert context.players[3]["stage_bets"] == 400
        assert context.players[3]["round_bets"] == 660
        with pytest.raises(KeyError):
            context.players[3]["dif"]
        with pytest.raises(KeyError):
            context.players[3]["abilities"]
        assert len(context.players[3]["cards"]) == 2
        assert context.players[3]["combo"] is None
        assert context.players[3]["last_action"] == {"kind": Player.Action.RAISE, "bet": 400}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.STAGE_NEEDED
        assert context.last_action == {"identifier": 2, "kind": Player.Action.CALL, "bet": 400}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.action(Player.Action.CALL).success
        context = game.new_stage()
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 5
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.RIVER, "depth": 0}
        assert context.bank == 1580
        assert context.result == None
        assert context.last_action == {"identifier": 2, "kind": Player.Action.CALL, "bet": 400}
        assert context.current_player == 2

        assert context.players[2]["chips"] == 340
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 660
        assert context.players[2]["dif"] == 0
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 340},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] is None

        assert context.players[3]["chips"] == 340
        assert context.players[3]["stage_bets"] == 0
        assert context.players[3]["round_bets"] == 660
        with pytest.raises(KeyError):
            context.players[3]["dif"]
        with pytest.raises(KeyError):
            context.players[3]["abilities"]
        assert len(context.players[3]["cards"]) == 2
        assert context.players[3]["combo"] is None
        assert context.players[3]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        game._table.items = [Card("Jd"), Card("8s"), Card("3d"), Card("Td"), Card("Ac")]

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CHECK)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 5
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.RIVER, "depth": 0}
        assert context.bank == 1580
        assert context.result == None
        assert context.last_action == {"identifier": 2, "kind": Player.Action.CHECK, "bet": 0}
        assert context.current_player == 3

        assert context.players[2]["chips"] == 340
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 660
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[3]["chips"] == 340
        assert context.players[3]["stage_bets"] == 0
        assert context.players[3]["round_bets"] == 660
        assert context.players[3]["dif"] == 0
        assert context.players[3]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 340},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[3]["cards"]) == 2
        assert context.players[3]["combo"] is None
        assert context.players[3]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.RAISE, 340)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 5
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.RIVER, "depth": 1}
        assert context.bank == 1920
        assert context.result == None
        assert context.last_action == {"identifier": 3, "kind": Player.Action.ALL_IN, "bet": 340}
        assert context.current_player == 2

        assert context.players[2]["chips"] == 340
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 660
        assert context.players[2]["dif"] == 340
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 0, "max": 0},
            Player.Action.CALL: 340,
            Player.Action.CHECK: False,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[3]["chips"] == 0
        assert context.players[3]["stage_bets"] == 340
        assert context.players[3]["round_bets"] == 1000
        with pytest.raises(KeyError):
            context.players[3]["dif"]
        with pytest.raises(KeyError):
            context.players[3]["abilities"]
        assert len(context.players[3]["cards"]) == 2
        assert context.players[3]["combo"] is None
        assert context.players[3]["last_action"] == {"kind": Player.Action.ALL_IN, "bet": 340}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.ROUND_NEEDED
        assert len(context.table) == 5
        assert context.state == Game.SHOW_DOWN
        assert context.stage == {"name": Game.Stage.RIVER, "depth": 1}
        assert context.bank == 2260
        assert context.result == {"winners": {2: 2260}, "loosers": {3: 1000, 0: 260}}
        assert context.last_action == {"identifier": 2, "kind": Player.Action.ALL_IN, "bet": 340}
        with pytest.raises(AttributeError):
            context.current_player

        assert context.players[2]["chips"] == 2260
        assert context.players[2]["stage_bets"] == 340
        assert context.players[2]["round_bets"] == 1000
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"].type == Combo.FLUSH
        assert context.players[2]["last_action"] == {"kind": Player.Action.ALL_IN, "bet": 340}

        assert context.players[3]["chips"] == 0
        assert context.players[3]["stage_bets"] == 340
        assert context.players[3]["round_bets"] == 1000
        with pytest.raises(KeyError):
            context.players[3]["dif"]
        with pytest.raises(KeyError):
            context.players[3]["abilities"]
        assert len(context.players[3]["cards"]) == 2
        assert context.players[3]["combo"].type == Combo.TWO_PAIRS
        assert context.players[3]["last_action"] == {"kind": Player.Action.ALL_IN, "bet": 340}

        #####################################################
        #####################################################
        #####################################################

        assert not game.action(Player.Action.CALL).success
        assert not game.new_stage().success
        context = game.new_round()
        assert game._players._order == [2, 0, 1]
        assert game._players._involved_order == [2, 0, 1]
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 0
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.PRE_FLOP, "depth": 0}
        assert context.bank == 30
        assert context.result == None
        assert context.last_action == {"identifier": 1, "kind": Player.Action.BLIND_BET, "bet": 20}
        assert context.current_player == 2

        assert context.players[0]["chips"] == 730
        assert context.players[0]["stage_bets"] == 10
        assert context.players[0]["round_bets"] == 10
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 10}

        assert context.players[1]["chips"] == 980
        assert context.players[1]["stage_bets"] == 20
        assert context.players[1]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 20}

        assert context.players[2]["chips"] == 2260
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 0
        assert context.players[2]["dif"] == 20
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 21, "max": 2260},
            Player.Action.CALL: 20,
            Player.Action.CHECK: False,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        game._players[0].hand.items = [Card("2d"), Card("7s")]
        game._players[1].hand.items = [Card("Kc"), Card("Js")]
        game._players[2].hand.items = [Card("Qh"), Card("9h")]

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 0
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.PRE_FLOP, "depth": 0}
        assert context.bank == 50
        assert context.result == None
        assert context.last_action == {"identifier": 2, "kind": Player.Action.CALL, "bet": 20}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 730
        assert context.players[0]["stage_bets"] == 10
        assert context.players[0]["round_bets"] == 10
        assert context.players[0]["dif"] == 10
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 11, "max": 730},
            Player.Action.CALL: 10,
            Player.Action.CHECK: False,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 10}

        assert context.players[1]["chips"] == 980
        assert context.players[1]["stage_bets"] == 20
        assert context.players[1]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 20}

        assert context.players[2]["chips"] == 2240
        assert context.players[2]["stage_bets"] == 20
        assert context.players[2]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.CALL, "bet": 20}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 0
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.PRE_FLOP, "depth": 0}
        assert context.bank == 60
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.CALL, "bet": 10}
        assert context.current_player == 1

        assert context.players[0]["chips"] == 720
        assert context.players[0]["stage_bets"] == 20
        assert context.players[0]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.CALL, "bet": 10}

        assert context.players[1]["chips"] == 980
        assert context.players[1]["stage_bets"] == 20
        assert context.players[1]["round_bets"] == 20
        assert context.players[1]["dif"] == 0
        assert context.players[1]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 980},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 20}

        assert context.players[2]["chips"] == 2240
        assert context.players[2]["stage_bets"] == 20
        assert context.players[2]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.CALL, "bet": 20}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CHECK)
        assert context.success
        assert context.point == Game.STAGE_NEEDED
        assert context.last_action == {"identifier": 1, "kind": Player.Action.CHECK, "bet": 0}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.action(Player.Action.CALL).success
        context = game.new_stage()
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 3
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.FLOP, "depth": 0}
        assert context.bank == 60
        assert context.result == None
        assert context.last_action == {"identifier": 1, "kind": Player.Action.CHECK, "bet": 0}
        assert context.current_player == 2

        assert context.players[0]["chips"] == 720
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[1]["chips"] == 980
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 2240
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 20
        assert context.players[2]["dif"] == 0
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 2240},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        game._table.items = [Card("8s"), Card("Ad"), Card("8d")]

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CHECK)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 3
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.FLOP, "depth": 0}
        assert context.bank == 60
        assert context.result == None
        assert context.last_action == {"identifier": 2, "kind": Player.Action.CHECK, "bet": 0}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 720
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 20
        assert context.players[0]["dif"] == 0
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 720},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[1]["chips"] == 980
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 2240
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.RAISE, 60)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 3
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.FLOP, "depth": 0}
        assert context.bank == 120
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.RAISE, "bet": 60}
        assert context.current_player == 1

        assert context.players[0]["chips"] == 660
        assert context.players[0]["stage_bets"] == 60
        assert context.players[0]["round_bets"] == 80
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.RAISE, "bet": 60}

        assert context.players[1]["chips"] == 980
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 20
        assert context.players[1]["dif"] == 60
        assert context.players[1]["abilities"] == {
            Player.Action.RAISE: {"min": 61, "max": 980},
            Player.Action.CALL: 60,
            Player.Action.CHECK: False,
        }
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 2240
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 3
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.FLOP, "depth": 1}
        assert context.bank == 180
        assert context.result == None
        assert context.last_action == {"identifier": 1, "kind": Player.Action.CALL, "bet": 60}
        assert context.current_player == 2

        assert context.players[0]["chips"] == 660
        assert context.players[0]["stage_bets"] == 60
        assert context.players[0]["round_bets"] == 80
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.RAISE, "bet": 60}

        assert context.players[1]["chips"] == 920
        assert context.players[1]["stage_bets"] == 60
        assert context.players[1]["round_bets"] == 80
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.CALL, "bet": 60}

        assert context.players[2]["chips"] == 2240
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 20
        assert context.players[2]["dif"] == 60
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 61, "max": 2240},
            Player.Action.CALL: 60,
            Player.Action.CHECK: False,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.STAGE_NEEDED
        assert context.last_action == {"identifier": 2, "kind": Player.Action.CALL, "bet": 60}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.action(Player.Action.CALL).success
        context = game.new_stage()
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 4
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.TURN, "depth": 0}
        assert context.bank == 240
        assert context.result == None
        assert context.last_action == {"identifier": 2, "kind": Player.Action.CALL, "bet": 60}
        assert context.current_player == 2

        assert context.players[0]["chips"] == 660
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 80
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[1]["chips"] == 920
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 80
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 2180
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 80
        assert context.players[2]["dif"] == 0
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 2180},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        game._table.items = [Card("8s"), Card("Ad"), Card("8d"), Card("4d")]

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CHECK)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 4
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.TURN, "depth": 0}
        assert context.bank == 240
        assert context.result == None
        assert context.last_action == {"identifier": 2, "kind": Player.Action.CHECK, "bet": 0}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 660
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 80
        assert context.players[0]["dif"] == 0
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 660},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[1]["chips"] == 920
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 80
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 2180
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 80
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}


        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.RAISE, 200)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 4
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.TURN, "depth": 0}
        assert context.bank == 440
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.RAISE, "bet": 200}
        assert context.current_player == 1

        assert context.players[0]["chips"] == 460
        assert context.players[0]["stage_bets"] == 200
        assert context.players[0]["round_bets"] == 280
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.RAISE, "bet": 200}

        assert context.players[1]["chips"] == 920
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 80
        assert context.players[1]["dif"] == 200
        assert context.players[1]["abilities"] == {
            Player.Action.RAISE: {"min": 201, "max": 920},
            Player.Action.CALL: 200,
            Player.Action.CHECK: False,
        }
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 2180
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 80
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.FOLD)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 4
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.TURN, "depth": 1}
        assert context.bank == 440
        assert context.result == None
        assert context.last_action == {"identifier": 1, "kind": Player.Action.FOLD, "bet": 0}
        assert context.current_player == 2

        assert context.players[0]["chips"] == 460
        assert context.players[0]["stage_bets"] == 200
        assert context.players[0]["round_bets"] == 280
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.RAISE, "bet": 200}

        assert context.players[2]["chips"] == 2180
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 80
        assert context.players[2]["dif"] == 200
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 201, "max": 2180},
            Player.Action.CALL: 200,
            Player.Action.CHECK: False,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.FOLD)
        assert context.success
        assert context.point == Game.ROUND_NEEDED
        assert len(context.table) == 4
        assert context.state == Game.FOLD
        assert context.stage == {"name": Game.Stage.TURN, "depth": 1}
        assert context.bank == 440
        assert context.result == {"winners": {0: 440}, "loosers": {1: 80, 2: 80}}
        assert context.last_action == {"identifier": 2, "kind": Player.Action.FOLD, "bet": 0}
        with pytest.raises(AttributeError):
            context.current_player

        assert context.players[0]["chips"] == 900
        assert context.players[0]["stage_bets"] == 200
        assert context.players[0]["round_bets"] == 280
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.RAISE, "bet": 200}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_stage().success
        assert not game.action(Player.Action.CALL).success
        context = game.new_round()
        assert game._players._order == [0, 1, 2]
        assert game._players._involved_order == [0, 1, 2]
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 0
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.PRE_FLOP, "depth": 0}
        assert context.bank == 30
        assert context.result == None
        assert context.last_action == {"identifier": 2, "kind": Player.Action.BLIND_BET, "bet": 20}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 900
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 0
        assert context.players[0]["dif"] == 20
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 21, "max": 900},
            Player.Action.CALL: 20,
            Player.Action.CHECK: False,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[1]["chips"] == 910
        assert context.players[1]["stage_bets"] == 10
        assert context.players[1]["round_bets"] == 10
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 10}

        assert context.players[2]["chips"] == 2160
        assert context.players[2]["stage_bets"] == 20
        assert context.players[2]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 20}

        #####################################################
        #####################################################
        #####################################################

        game._players[0].hand.items = [Card("Ks"), Card("Ah")]
        game._players[1].hand.items = [Card("Ac"), Card("Js")]
        game._players[2].hand.items = [Card("Ad"), Card("Td")]

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_stage().success
        assert not game.new_round().success
        context = game.action(Player.Action.RAISE, 60)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 0
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.PRE_FLOP, "depth": 0}
        assert context.bank == 90
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.RAISE, "bet": 60}
        assert context.current_player == 1

        assert context.players[0]["chips"] == 840
        assert context.players[0]["stage_bets"] == 60
        assert context.players[0]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.RAISE, "bet": 60}

        assert context.players[1]["chips"] == 910
        assert context.players[1]["stage_bets"] == 10
        assert context.players[1]["round_bets"] == 10
        assert context.players[1]["dif"] == 50
        assert context.players[1]["abilities"] == {
            Player.Action.RAISE: {"min": 51, "max": 910},
            Player.Action.CALL: 50,
            Player.Action.CHECK: False,
        }
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 10}

        assert context.players[2]["chips"] == 2160
        assert context.players[2]["stage_bets"] == 20
        assert context.players[2]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 20}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_stage().success
        assert not game.new_round().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 0
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.PRE_FLOP, "depth": 0}
        assert context.bank == 140
        assert context.result == None
        assert context.last_action == {"identifier": 1, "kind": Player.Action.CALL, "bet": 50}
        assert context.current_player == 2

        assert context.players[0]["chips"] == 840
        assert context.players[0]["stage_bets"] == 60
        assert context.players[0]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.RAISE, "bet": 60}

        assert context.players[1]["chips"] == 860
        assert context.players[1]["stage_bets"] == 60
        assert context.players[1]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.CALL, "bet": 50}

        assert context.players[2]["chips"] == 2160
        assert context.players[2]["stage_bets"] == 20
        assert context.players[2]["round_bets"] == 20
        assert context.players[2]["dif"] == 40
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 41, "max": 2160},
            Player.Action.CALL: 40,
            Player.Action.CHECK: False,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 20}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.STAGE_NEEDED
        assert context.last_action == {"identifier": 2, "kind": Player.Action.CALL, "bet": 40}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.action(Player.Action.CALL).success
        context = game.new_stage()
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 3
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.FLOP, "depth": 0}
        assert context.bank == 180
        assert context.result == None
        assert context.last_action == {"identifier": 2, "kind": Player.Action.CALL, "bet": 40}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 840
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 60
        assert context.players[0]["dif"] == 0
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 840},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[1]["chips"] == 860
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 2120
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        game._table.items = [Card("Qd"), Card("7s"), Card("Jd")]

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CHECK)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 3
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.FLOP, "depth": 0}
        assert context.bank == 180
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.CHECK, "bet": 0}
        assert context.current_player == 1

        assert context.players[0]["chips"] == 840
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[1]["chips"] == 860
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 60
        assert context.players[1]["dif"] == 0
        assert context.players[1]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 860},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 2120
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CHECK)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 3
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.FLOP, "depth": 0}
        assert context.bank == 180
        assert context.result == None
        assert context.last_action == {"identifier": 1, "kind": Player.Action.CHECK, "bet": 0}
        assert context.current_player == 2

        assert context.players[0]["chips"] == 840
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[1]["chips"] == 860
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[2]["chips"] == 2120
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 60
        assert context.players[2]["dif"] == 0
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 2120},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CHECK)
        assert context.success
        assert context.point == Game.STAGE_NEEDED
        assert context.last_action == {"identifier": 2, "kind": Player.Action.CHECK, "bet": 0}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.action(Player.Action.CALL).success
        context = game.new_stage()
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 4
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.TURN, "depth": 0}
        assert context.bank == 180
        assert context.result == None
        assert context.last_action == {"identifier": 2, "kind": Player.Action.CHECK, "bet": 0}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 840
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 60
        assert context.players[0]["dif"] == 0
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 840},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[1]["chips"] == 860
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 2120
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        game._table.items = [Card("Qd"), Card("7s"), Card("Jd"), Card("Tc")]

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CHECK)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 4
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.TURN, "depth": 0}
        assert context.bank == 180
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.CHECK, "bet": 0}
        assert context.current_player == 1

        assert context.players[0]["chips"] == 840
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[1]["chips"] == 860
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 60
        assert context.players[1]["dif"] == 0
        assert context.players[1]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 860},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 2120
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CHECK)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 4
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.TURN, "depth": 0}
        assert context.bank == 180
        assert context.result == None
        assert context.last_action == {"identifier": 1, "kind": Player.Action.CHECK, "bet": 0}
        assert context.current_player == 2

        assert context.players[0]["chips"] == 840
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[1]["chips"] == 860
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[2]["chips"] == 2120
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 60
        assert context.players[2]["dif"] == 0
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 2120},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.RAISE, 150)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 4
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.TURN, "depth": 1}
        assert context.bank == 330
        assert context.result == None
        assert context.last_action == {"identifier": 2, "kind": Player.Action.RAISE, "bet": 150}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 840
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 60
        assert context.players[0]["dif"] == 150
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 151, "max": 840},
            Player.Action.CALL: 150,
            Player.Action.CHECK: False,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[1]["chips"] == 860
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[2]["chips"] == 1970
        assert context.players[2]["stage_bets"] == 150
        assert context.players[2]["round_bets"] == 210
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.RAISE, "bet": 150}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 4
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.TURN, "depth": 1}
        assert context.bank == 480
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.CALL, "bet": 150}
        assert context.current_player == 1

        assert context.players[0]["chips"] == 690
        assert context.players[0]["stage_bets"] == 150
        assert context.players[0]["round_bets"] == 210
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.CALL, "bet": 150}

        assert context.players[1]["chips"] == 860
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 60
        assert context.players[1]["dif"] == 150
        assert context.players[1]["abilities"] == {
            Player.Action.RAISE: {"min": 151, "max": 860},
            Player.Action.CALL: 150,
            Player.Action.CHECK: False,
        }
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[2]["chips"] == 1970
        assert context.players[2]["stage_bets"] == 150
        assert context.players[2]["round_bets"] == 210
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.RAISE, "bet": 150}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.STAGE_NEEDED
        assert context.last_action == {"identifier": 1, "kind": Player.Action.CALL, "bet": 150}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.action(Player.Action.CALL).success
        context = game.new_stage()
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 5
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.RIVER, "depth": 0}
        assert context.bank == 630
        assert context.result == None
        assert context.last_action == {"identifier": 1, "kind": Player.Action.CALL, "bet": 150}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 690
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 210
        assert context.players[0]["dif"] == 0
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 690},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[1]["chips"] == 710
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 210
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 1970
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 210
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        game._table.items = [Card("Qd"), Card("7s"), Card("Jd"), Card("Tc"), Card("Kh")]

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CHECK)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 5
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.RIVER, "depth": 0}
        assert context.bank == 630
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.CHECK, "bet": 0}
        assert context.current_player == 1

        assert context.players[0]["chips"] == 690
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 210
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[1]["chips"] == 710
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 210
        assert context.players[1]["dif"] == 0
        assert context.players[1]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 710},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 1970
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 210
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CHECK)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 5
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.RIVER, "depth": 0}
        assert context.bank == 630
        assert context.result == None
        assert context.last_action == {"identifier": 1, "kind": Player.Action.CHECK, "bet": 0}
        assert context.current_player == 2

        assert context.players[0]["chips"] == 690
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 210
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[1]["chips"] == 710
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 210
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[2]["chips"] == 1970
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 210
        assert context.players[2]["dif"] == 0
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 1970},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.RAISE, 800)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 5
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.RIVER, "depth": 1}
        assert context.bank == 1430
        assert context.result == None
        assert context.last_action == {"identifier": 2, "kind": Player.Action.RAISE, "bet": 800}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 690
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 210
        assert context.players[0]["dif"] == 800
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 0, "max": 0},
            Player.Action.CALL: 690,
            Player.Action.CHECK: False,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[1]["chips"] == 710
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 210
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[2]["chips"] == 1170
        assert context.players[2]["stage_bets"] == 800
        assert context.players[2]["round_bets"] == 1010
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.RAISE, "bet": 800}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 5
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.RIVER, "depth": 1}
        assert context.bank == 2120
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.ALL_IN, "bet": 690}
        assert context.current_player == 1

        assert context.players[0]["chips"] == 0
        assert context.players[0]["stage_bets"] == 690
        assert context.players[0]["round_bets"] == 900
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.ALL_IN, "bet": 690}

        assert context.players[1]["chips"] == 710
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 210
        assert context.players[1]["dif"] == 800
        assert context.players[1]["abilities"] == {
            Player.Action.RAISE: {"min": 0, "max": 0},
            Player.Action.CALL: 710,
            Player.Action.CHECK: False,
        }
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        assert context.players[2]["chips"] == 1170
        assert context.players[2]["stage_bets"] == 800
        assert context.players[2]["round_bets"] == 1010
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.RAISE, "bet": 800}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.ROUND_NEEDED
        assert len(context.table) == 5
        assert context.state == Game.SHOW_DOWN
        assert context.stage == {"name": Game.Stage.RIVER, "depth": 1}
        assert context.bank == 2830
        assert context.result == {"winners": {0: 900, 1: 920, 2: 1010}, "loosers": {}}
        assert context.last_action == {"identifier": 1, "kind": Player.Action.ALL_IN, "bet": 710}
        with pytest.raises(AttributeError):
            context.current_player

        assert context.players[0]["chips"] == 900
        assert context.players[0]["stage_bets"] == 690
        assert context.players[0]["round_bets"] == 900
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"].type == Combo.STRAIGHT
        assert context.players[0]["last_action"] == {"kind": Player.Action.ALL_IN, "bet": 690}

        assert context.players[1]["chips"] == 920
        assert context.players[1]["stage_bets"] == 710
        assert context.players[1]["round_bets"] == 920
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"].type == Combo.STRAIGHT
        assert context.players[1]["last_action"] == {"kind": Player.Action.ALL_IN, "bet": 710}

        assert context.players[2]["chips"] == 2180
        assert context.players[2]["stage_bets"] == 800
        assert context.players[2]["round_bets"] == 1010
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"].type == Combo.STRAIGHT
        assert context.players[2]["last_action"] == {"kind": Player.Action.RAISE, "bet": 800}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_stage().success
        assert not game.action(Player.Action.CALL).success
        context = game.new_round()
        assert game._players._order == [1, 2, 0]
        assert game._players._involved_order == [1, 2, 0]
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 0
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.PRE_FLOP, "depth": 0}
        assert context.bank == 30
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.BLIND_BET, "bet": 20}
        assert context.current_player == 1

        assert context.players[0]["chips"] == 880
        assert context.players[0]["stage_bets"] == 20
        assert context.players[0]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 20}

        assert context.players[1]["chips"] == 920
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 0
        assert context.players[1]["dif"] == 20
        assert context.players[1]["abilities"] == {
            Player.Action.RAISE: {"min": 21, "max": 920},
            Player.Action.CALL: 20,
            Player.Action.CHECK: False,
        }
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 2170
        assert context.players[2]["stage_bets"] == 10
        assert context.players[2]["round_bets"] == 10
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 10}

        #####################################################
        #####################################################
        #####################################################

        game._players[2].hand.items = [Card("Th"), Card("9c")]
        game._players[0].hand.items = [Card("Qc"), Card("Qd")]
        game._players[1].hand.items = [Card("Td"), Card("4s")]

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_stage().success
        assert not game.new_round().success
        context = game.action(Player.Action.RAISE, 60)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 0
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.PRE_FLOP, "depth": 0}
        assert context.bank == 90
        assert context.result == None
        assert context.last_action == {"identifier": 1, "kind": Player.Action.RAISE, "bet": 60}
        assert context.current_player == 2

        assert context.players[0]["chips"] == 880
        assert context.players[0]["stage_bets"] == 20
        assert context.players[0]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 20}

        assert context.players[1]["chips"] == 860
        assert context.players[1]["stage_bets"] == 60
        assert context.players[1]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.RAISE, "bet": 60}

        assert context.players[2]["chips"] == 2170
        assert context.players[2]["stage_bets"] == 10
        assert context.players[2]["round_bets"] == 10
        assert context.players[2]["dif"] == 50
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 51, "max": 2170},
            Player.Action.CALL: 50,
            Player.Action.CHECK: False,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 10}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_stage().success
        assert not game.new_round().success
        context = game.action(Player.Action.FOLD)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 0
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.PRE_FLOP, "depth": 0}
        assert context.bank == 90
        assert context.result == None
        assert context.last_action == {"identifier": 2, "kind": Player.Action.FOLD, "bet": 0}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 880
        assert context.players[0]["stage_bets"] == 20
        assert context.players[0]["round_bets"] == 20
        assert context.players[0]["dif"] == 40
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 41, "max": 880},
            Player.Action.CALL: 40,
            Player.Action.CHECK: False,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 20}

        assert context.players[1]["chips"] == 860
        assert context.players[1]["stage_bets"] == 60
        assert context.players[1]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.RAISE, "bet": 60}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.STAGE_NEEDED
        assert context.last_action == {"identifier": 0, "kind": Player.Action.CALL, "bet": 40}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.action(Player.Action.CALL).success
        context = game.new_stage()
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 3
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.FLOP, "depth": 0}
        assert context.bank == 130
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.CALL, "bet": 40}
        assert context.current_player == 1

        assert context.players[0]["chips"] == 840
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[1]["chips"] == 860
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 60
        assert context.players[1]["dif"] == 0
        assert context.players[1]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 860},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        game._table.items = [Card("8s"), Card("Qh"), Card("7d")]

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.RAISE, 100)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 3
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.FLOP, "depth": 0}
        assert context.bank == 230
        assert context.result == None
        assert context.last_action == {"identifier": 1, "kind": Player.Action.RAISE, "bet": 100}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 840
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 60
        assert context.players[0]["dif"] == 100
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 101, "max": 840},
            Player.Action.CALL: 100,
            Player.Action.CHECK: False,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[1]["chips"] == 760
        assert context.players[1]["stage_bets"] == 100
        assert context.players[1]["round_bets"] == 160
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.RAISE, "bet": 100}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.STAGE_NEEDED
        assert context.last_action == {"identifier": 0, "kind": Player.Action.CALL, "bet": 100}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.action(Player.Action.CALL).success
        context = game.new_stage()
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 4
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.TURN, "depth": 0}
        assert context.bank == 330
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.CALL, "bet": 100}
        assert context.current_player == 1

        assert context.players[0]["chips"] == 740
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 160
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[1]["chips"] == 760
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 160
        assert context.players[1]["dif"] == 0
        assert context.players[1]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 760},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        game._table.items = [Card("8s"), Card("Qh"), Card("7d"), Card("6d")]

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.RAISE, 330)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 4
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.TURN, "depth": 0}
        assert context.bank == 660
        assert context.result == None
        assert context.last_action == {"identifier": 1, "kind": Player.Action.RAISE, "bet": 330}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 740
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 160
        assert context.players[0]["dif"] == 330
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 331, "max": 740},
            Player.Action.CALL: 330,
            Player.Action.CHECK: False,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[1]["chips"] == 430
        assert context.players[1]["stage_bets"] == 330
        assert context.players[1]["round_bets"] == 490
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.RAISE, "bet": 330}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.RAISE, 640)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 4
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.TURN, "depth": 1}
        assert context.bank == 1300
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.RAISE, "bet": 640}
        assert context.current_player == 1

        assert context.players[0]["chips"] == 100
        assert context.players[0]["stage_bets"] == 640
        assert context.players[0]["round_bets"] == 800
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.RAISE, "bet": 640}

        assert context.players[1]["chips"] == 430
        assert context.players[1]["stage_bets"] == 330
        assert context.players[1]["round_bets"] == 490
        assert context.players[1]["dif"] == 310
        assert context.players[1]["abilities"] == {
            Player.Action.RAISE: {"min": 311, "max": 430},
            Player.Action.CALL: 310,
            Player.Action.CHECK: False,
        }
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.RAISE, "bet": 330}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.STAGE_NEEDED
        assert context.last_action == {"identifier": 1, "kind": Player.Action.CALL, "bet": 310}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.action(Player.Action.CALL).success
        context = game.new_stage()
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 5
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.RIVER, "depth": 0}
        assert context.bank == 1610
        assert context.result == None
        assert context.last_action == {"identifier": 1, "kind": Player.Action.CALL, "bet": 310}
        assert context.current_player == 1

        assert context.players[0]["chips"] == 100
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 800
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[1]["chips"] == 120
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 800
        assert context.players[1]["dif"] == 0
        assert context.players[1]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 120},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        game._table.items = [Card("8s"), Card("Qh"), Card("7d"), Card("6d"), Card("2c")]

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CHECK)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 5
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.RIVER, "depth": 0}
        assert context.bank == 1610
        assert context.result == None
        assert context.last_action == {"identifier": 1, "kind": Player.Action.CHECK, "bet": 0}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 100
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 800
        assert context.players[0]["dif"] == 0
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 100},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[1]["chips"] == 120
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 800
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.RAISE, 100)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 5
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.RIVER, "depth": 1}
        assert context.bank == 1710
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.ALL_IN, "bet": 100}
        assert context.current_player == 1

        assert context.players[0]["chips"] == 0
        assert context.players[0]["stage_bets"] == 100
        assert context.players[0]["round_bets"] == 900
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"]  == {"kind": Player.Action.ALL_IN, "bet": 100}

        assert context.players[1]["chips"] == 120
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 800
        assert context.players[1]["dif"] == 100
        assert context.players[1]["abilities"] == {
            Player.Action.RAISE: {"min": 101, "max": 120},
            Player.Action.CALL: 100,
            Player.Action.CHECK: False,
        }
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.RAISE, 120)
        assert context.success
        assert context.point == Game.ROUND_NEEDED
        assert len(context.table) == 5
        assert context.state == Game.SHOW_DOWN
        assert context.stage == {"name": Game.Stage.RIVER, "depth": 1}
        assert context.bank == 1830
        assert context.result == {"winners": {0: 1810}, "loosers": {1: 900, 2: 10}}
        assert context.last_action == {"identifier": 1, "kind": Player.Action.ALL_IN, "bet": 120}
        with pytest.raises(AttributeError):
            context.current_player

        assert context.players[0]["chips"] == 1810
        assert context.players[0]["stage_bets"] == 100
        assert context.players[0]["round_bets"] == 900
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"].type == Combo.STRAIGHT
        assert context.players[0]["last_action"]  == {"kind": Player.Action.ALL_IN, "bet": 100}

        assert context.players[1]["chips"] == 20
        assert context.players[1]["stage_bets"] == 120
        assert context.players[1]["round_bets"] == 920
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"].type == Combo.THREE_OF_A_KIND
        assert context.players[1]["last_action"] == {"kind": Player.Action.ALL_IN, "bet": 120}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_stage().success
        assert not game.action(Player.Action.CALL).success
        context = game.new_round()
        assert game._players._order == [2, 0, 1]
        assert game._players._involved_order == [2, 0, 1]
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 0
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.PRE_FLOP, "depth": 0}
        assert context.bank == 30
        assert context.result == None
        assert context.last_action == {"identifier": 1, "kind": Player.Action.ALL_IN, "bet": 20}
        assert context.current_player == 2

        assert context.players[0]["chips"] == 1800
        assert context.players[0]["stage_bets"] == 10
        assert context.players[0]["round_bets"] == 10
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 10}

        assert context.players[1]["chips"] == 0
        assert context.players[1]["stage_bets"] == 20
        assert context.players[1]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.ALL_IN, "bet": 20}

        assert context.players[2]["chips"] == 2170
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 0
        assert context.players[2]["dif"] == 20
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 21, "max": 2170},
            Player.Action.CALL: 20,
            Player.Action.CHECK: False,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        game._players[1].hand.items = [Card("Ks"), Card("Kc")]
        game._players[2].hand.items = [Card("4d"), Card("8s")]
        game._players[0].hand.items = [Card("Jh"), Card("Ah")]

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.RAISE, 60)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 0
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.PRE_FLOP, "depth": 0}
        assert context.bank == 90
        assert context.result == None
        assert context.last_action == {"identifier": 2, "kind": Player.Action.RAISE, "bet": 60}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 1800
        assert context.players[0]["stage_bets"] == 10
        assert context.players[0]["round_bets"] == 10
        assert context.players[0]["dif"] == 50
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 51, "max": 1800},
            Player.Action.CALL: 50,
            Player.Action.CHECK: False,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.BLIND_BET, "bet": 10}

        assert context.players[1]["chips"] == 0
        assert context.players[1]["stage_bets"] == 20
        assert context.players[1]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] == {"kind": Player.Action.ALL_IN, "bet": 20}

        assert context.players[2]["chips"] == 2110
        assert context.players[2]["stage_bets"] == 60
        assert context.players[2]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.RAISE, "bet": 60}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.STAGE_NEEDED
        assert context.last_action == {"identifier": 0, "kind": Player.Action.CALL, "bet": 50}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.action(Player.Action.CALL).success
        context = game.new_stage()
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 3
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.FLOP, "depth": 0}
        assert context.bank == 140
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.CALL, "bet": 50}
        assert context.current_player == 2

        assert context.players[0]["chips"] == 1750
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[1]["chips"] == 0
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 2110
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 60
        assert context.players[2]["dif"] == 0
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 2110},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        game._table.items = [Card("Kd"), Card("Th"), Card("Qh")]

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CHECK)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 3
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.FLOP, "depth": 0}
        assert context.bank == 140
        assert context.result == None
        assert context.last_action == {"identifier": 2, "kind": Player.Action.CHECK, "bet": 0}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 1750
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 60
        assert context.players[0]["dif"] == 0
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 1750},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[1]["chips"] == 0
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 2110
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 60
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.RAISE, 100)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 3
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.FLOP, "depth": 1}
        assert context.bank == 240
        assert context.result == None
        assert context.last_action == {"identifier": 0, "kind": Player.Action.RAISE, "bet": 100}
        assert context.current_player == 2

        assert context.players[0]["chips"] == 1650
        assert context.players[0]["stage_bets"] == 100
        assert context.players[0]["round_bets"] == 160
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] == {"kind": Player.Action.RAISE, "bet": 100}

        assert context.players[1]["chips"] == 0
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 2110
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 60
        assert context.players[2]["dif"] == 100
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 101, "max": 2110},
            Player.Action.CALL: 100,
            Player.Action.CHECK: False,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.CHECK, "bet": 0}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.STAGE_NEEDED
        assert context.last_action == {"identifier": 2, "kind": Player.Action.CALL, "bet": 100}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.action(Player.Action.CALL).success
        context = game.new_stage()
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 4
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.TURN, "depth": 0}
        assert context.bank == 340
        assert context.result == None
        assert context.last_action == {"identifier": 2, "kind": Player.Action.CALL, "bet": 100}
        assert context.current_player == 2

        assert context.players[0]["chips"] == 1650
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 160
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[1]["chips"] == 0
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 2010
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 160
        assert context.players[2]["dif"] == 0
        assert context.players[2]["abilities"] == {
            Player.Action.RAISE: {"min": 1, "max": 2010},
            Player.Action.CALL: 0,
            Player.Action.CHECK: True,
        }
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] is None

        #####################################################
        #####################################################
        #####################################################

        game._table.items = [Card("Kd"), Card("Th"), Card("Qh"), Card("Kh")]

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.RAISE, 2010)
        assert context.success
        assert context.point == Game.ACTION_NEEDED
        assert len(context.table) == 4
        assert context.state == Game.NORMAL
        assert context.stage == {"name": Game.Stage.TURN, "depth": 0}
        assert context.bank == 2350
        assert context.result == None
        assert context.last_action == {"identifier": 2, "kind": Player.Action.ALL_IN, "bet": 2010}
        assert context.current_player == 0

        assert context.players[0]["chips"] == 1650
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 160
        assert context.players[0]["dif"] == 2010
        assert context.players[0]["abilities"] == {
            Player.Action.RAISE: {"min": 0, "max": 0},
            Player.Action.CALL: 1650,
            Player.Action.CHECK: False,
        }
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"] is None
        assert context.players[0]["last_action"] is None

        assert context.players[1]["chips"] == 0
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["combo"] is None
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 0
        assert context.players[2]["stage_bets"] == 2010
        assert context.players[2]["round_bets"] == 2170
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"] is None
        assert context.players[2]["last_action"] == {"kind": Player.Action.ALL_IN, "bet": 2010}

        #####################################################
        #####################################################
        #####################################################

        game._deck = Deck()
        for c in [Card("Kd"), Card("Th"), Card("Qh"), Card("Kh"),
            Card("Ks"), Card("Kc"), Card("4d"), Card("8s"), Card("Jh"), Card("Ah")]:
            game._deck.cards.pop(game._deck.cards.index(c))

        assert not game.new_round().success
        assert not game.new_stage().success
        context = game.action(Player.Action.CALL)
        assert context.success
        assert context.point == Game.STAGE_NEEDED
        assert context.last_action == {"identifier": 0, "kind": Player.Action.ALL_IN, "bet": 1650}

        #####################################################
        #####################################################
        #####################################################

        assert not game.new_round().success
        assert not game.action(Player.Action.CALL).success
        context = game.new_stage()
        assert context.success
        assert context.point == Game.THE_END
        assert len(context.table) == 5
        assert context.state == Game.THE_END
        assert context.stage == {"name": Game.Stage.RIVER, "depth": 0}
        assert context.bank == 4000
        assert context.result == {"winners": {2: 4000}, "loosers": {0: 1810, 1: 20}}
        assert context.last_action == {"identifier": 0, "kind": Player.Action.ALL_IN, "bet": 1650}
        with pytest.raises(AttributeError):
            context.current_player

        assert context.players[0]["chips"] == 0
        assert context.players[0]["stage_bets"] == 0
        assert context.players[0]["round_bets"] == 1810
        with pytest.raises(KeyError):
            context.players[0]["dif"]
        with pytest.raises(KeyError):
            context.players[0]["abilities"]
        assert len(context.players[0]["cards"]) == 2
        assert context.players[0]["combo"].type == Combo.FOUR_OF_A_KIND
        assert context.players[0]["last_action"] is None

        assert context.players[1]["chips"] == 0
        assert context.players[1]["stage_bets"] == 0
        assert context.players[1]["round_bets"] == 20
        with pytest.raises(KeyError):
            context.players[1]["dif"]
        with pytest.raises(KeyError):
            context.players[1]["abilities"]
        assert len(context.players[1]["cards"]) == 2
        assert context.players[1]["last_action"] is None

        assert context.players[2]["chips"] == 4000
        assert context.players[2]["stage_bets"] == 0
        assert context.players[2]["round_bets"] == 2170
        with pytest.raises(KeyError):
            context.players[2]["dif"]
        with pytest.raises(KeyError):
            context.players[2]["abilities"]
        assert len(context.players[2]["cards"]) == 2
        assert context.players[2]["combo"].type == Combo.STRAIGHT_FLUSH
        assert context.players[2]["last_action"] is None
