from os import getenv


TOKEN = getenv('TOKEN')
ADMIN = getenv('ADMIN')
HEROKU = getenv('HEROKU') or False
HEROKU_APP = getenv('HEROKU_APP') or False
PORT = getenv('HEROKU_APP') or 8443
YANDEX_CARD = getenv('YANDEX_CARD') or False
SBERBANK_CARD = getenv('SBERBANK_CARD') or False
NAME_DATABASE = getenv('NAME_DATABASE') or 'users_tg_bot'
NAME_TABLE = getenv('NAME_TABLE') or 'users'

dict_to_parse = {
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    },
    'rub': {
        'list': ['₽', 'rub', 'ruble', 'руб', 'рубль'],
        'url_orginal': 'https://www.cbr.ru/currency_base/daily/',
        'url': 'https://www.cbr-xml-daily.ru/daily_utf8.xml',
        'name_rub': {
            'Фунт стерлингов Соединенного королевства': 'GBP (Фунт стерлингов Великобритании)',
            'Швейцарский франк': 'CHF (Швейцарский франк)',
            'Доллар США': 'USD (Доллар США)',
            'Евро': 'EUR (Евро)',
            'Китайский юань': 'CNY (Китайский юань)',
            'Японских иен': 'JPY (Японских иен)',
        }
    },
    'crypto': {
        'list': ['₿', 'crypto', 'cryptocurrency', 'крипто', 'криптовалюта'],
        'url': 'https://myfin.by/crypto-rates',
        're': 'xs\W+\D+\W+div\W+div\W+td\W+td\W\d+.\d+\D',
        'split': '</div>\n                </div></td><td>',
        'name_crypto': {
            'BTC': 'BTC (Bitcoin)',
            'BCH': 'BCH (Bitcoin Cash/BCC)',
            'ETH': 'ETH (Ethereum)',
            'ETC': 'ETC (Ethereum Classic)',
            'LTC': 'LTC (Litecoin)',
            'XRP': 'XRP (Ripple)',
            'XLM': 'XLM (Stellar)',
        },
    },
}
