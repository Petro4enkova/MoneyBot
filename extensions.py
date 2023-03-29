import requests
import json
from config import exchanges

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            return APIException(f"Валюта {base} не найдена!")
        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            return APIException(f"Валюта {sym} не найдена!")
        if base_key == sym_key:
            raise APIException(f"Невозможно перевести одинаковые валюты {base}!")

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}!")


        payload = {}
        headers = {
            "apikey": "nTCbl1XBwtvr4ks86HDw1VU2UHeXD80T"
        }
        r = requests.get(f"https://api.apilayer.com/exchangerates_data/latest?symbols={sym_key}&base={base_key}",
                         headers=headers, data=payload)
        resp = json.loads(r.content)
        new_price = resp['rates'][sym_key] * float(amount)
        return round(new_price, 2)