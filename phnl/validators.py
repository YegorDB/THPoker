class CardSymbolValidator:
    def __init__(self, symbols, exception):
        self.symbols = symbols
        self.exception = exception

    def __call__(self, init_function):
        def wrap(init_self, symbol):
            symbol = str(symbol)
            if symbol not in set(self.symbols):
                raise self.exception(symbol)
            init_function(init_self, symbol)

        return wrap
