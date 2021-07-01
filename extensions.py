import requests
import json
from tkeys import keys


class ConvertionException(Exception):
    pass


class CryptoConvertion:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f'В параметрах одинаковые валюты {base}!')

        try:
            quote_tiker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Валюта {quote} не найдена!')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Валюта {base} не найдена!')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Неверное количество "{amount}"!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_tiker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base
