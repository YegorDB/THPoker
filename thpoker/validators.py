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


from functools import wraps

from thpoker import exceptions


class CardSymbolValidator:
    def __init__(self, symbols, exception):
        self._symbols = symbols
        self._exception = exception

    def __call__(self, init_function):
        def wrap(init_self, symbol):
            symbol = str(symbol)
            if not symbol in set(self._symbols):
                raise self._exception(symbol)
            init_function(init_self, symbol)
        return wrap


class PlayerActionValidator:
    def __init__(self, all_kinds):
        self._all_kinds = all_kinds

    def __call__(self, init_function):
        def wrap(init_self, kind, bet=0):
            if not kind in self._all_kinds:
                raise exceptions.PlayerActionKindError(kind)
            if not type(bet) is int or bet < 0:
                raise exceptions.PlayerActionBetError(kind)
            init_function(init_self, kind, bet)
        return wrap


def game_players_validator(func):
    @wraps(func)
    def wrap(self, chips, *players):
        if not type(chips) is int or chips < 1:
            raise exceptions.GamePlayersChipsError()
        players_count = len(players)
        if players_count < 2 or players_count > 10:
            raise exceptions.GamePlayersPlayersError()
        func(self, chips, *players)
    return wrap
