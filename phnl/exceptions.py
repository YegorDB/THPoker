class CardWeightSymbolError(Exception):
    def __init__(self, symbol):
        hint = f"""
    '{symbol}' is not a correct card weight symbol.
    Try to use '1', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'."""
        super().__init__(hint)


class CardSuitSymbolError(Exception):
    def __init__(self, symbol):
        hint = f"""
    '{symbol}' is not a correct card suit symbol.
    Try to use 'c', 'd', 'h', 's'."""
        super().__init__(hint)


class CardEmptySymbolError(Exception):
    def __init__(self):
        super().__init__("Card weight or suit need to be specified.")


class DeckCountTypeError(Exception):
    def __init__(self, count_type):
        super().__init__(f"Type of count cards to push need to be 'int' not '{count_type}'.")


class DeckCountNumberError(Exception):
    def __init__(self, count_number):
        super().__init__(f"{count_number} is out of current deck cards count.")


class CardsStringTypeError(Exception):
    def __init__(self, cards_string_type):
        super().__init__(f"Type of count cards to push need to be 'str' not '{cards_string_type}'.")


class ComboCardsTypeError(Exception):
    def __init__(self, current_type, needed_type, cards_kind):
        super().__init__(f"Type of {cards_kind} need to be '{needed_type}' not '{current_type}'.")


class ComboArgumentsError(Exception):
    def __init__(self):
        hint = f"""
    Combo takes keyword aruments only.
    Try to pass
        'cards_string'
        (example: Combo(cards_string='As/Ks/Qs/Js/Ts'))
    or
        'cards'
        (example: Combo(cards=Cards('As/Ks/Qs/Js/Ts')))
    or
        'table' and 'hand'
        (example: Combo(table=Table('As/Ks/Qs'), hand=Hand('Js/Ts'))
    or
        'table' and 'hand' and 'nominal_check_needed'
        (example: Combo(table=Table('As/Ks/Qs'), hand=Hand('Js/Ts'), nominal_check_needed=True)."""
        super().__init__(hint)