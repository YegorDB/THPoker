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
