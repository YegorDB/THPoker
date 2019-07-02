# Copyright 2018-2019 Yegor Bitensky

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class ComboCardsTypeError(Exception):
    def __init__(self, current_type, needed_type, cards_kind):
        super().__init__(f"Type of {cards_kind} need to be '{needed_type}' not '{current_type}'.")


class ComboArgumentsError(Exception):
    def __init__(self):
        super().__init__(
            """
                Combo takes keyword aruments only.
                Examples
                'cards_string': Combo(cards_string='As/Ks/Qs/Js/Ts');
                'cards': Combo(cards=Cards('As/Ks/Qs/Js/Ts'));
                'table' and 'hand': Combo(table=Table('As/Ks/Qs'), hand=Hand('Js/Ts'));
                'table' and 'hand' and 'nominal_check_needed':
                    Combo(table=Table('As/Ks/Qs'), hand=Hand('Js/Ts'), nominal_check_needed=True).
            """
        )
