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

from thpoker.core import Table, Hand, Combo
from thpoker.game import Context, Player, Game
from thpoker.exceptions import PlayerActionKindError, PlayerActionBetError

from utils import get_parameters


class TestPlayerAction:
    def test_validation(self):
        with pytest.raises(PlayerActionKindError):
            Player.Action(kind="wait")
        with pytest.raises(PlayerActionKindError):
            Player.Action(kind=15)
        with pytest.raises(PlayerActionBetError):
            Player.Action(kind=Player.Action.CHECK, bet="123")
        with pytest.raises(PlayerActionBetError):
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

    # def test_new_round(self):
    #     self.player.new_round()
