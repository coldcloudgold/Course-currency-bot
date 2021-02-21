"""Модуль для парсинга и обработки данных.

Function
--------
get_course_crypto(url_site: str, headers_site: dict, re_pattern: str, split_pattern: str, name_space: dict) -> dict
    функция парсит и обрабатывет данные, возвращая словарь
get_course_rub(url_site: str, name_space: dict) -> dict
    функция парсит и обрабатывет данные, возвращая словарь
start_parse(currency: str) -> dict
    функция вызывает одну из функци (get_course_rub, get_course_crypto) и возвращает словарь
"""

from re import findall
from time import time
import requests

import xmltodict

from config import dict_to_parse


def get_course_crypto(url_site: str, headers_site: dict, re_pattern: str, split_pattern: str, name_space: dict) -> dict:
    """Функция парсит и обрабатывает данные, возвращая словарь с парами: криптовалюта - доллар.

    Parameters
    ----------
    url_site : str
        ссылка на сайт для парсинга (https://myfin.by/crypto-rates)
    headers_site : dict
        словарь с параметрами User-Agent
    re_pattern : str
        паттерн регулярного выражения, по которому выполяется поиск
    split_pattern : str
        паттерн разбития строки
    name_space :  dict
        словарь с необохдимыми валютами

    Exception
    ---------
        Если парсинг не удался, вернется словарь со значением даты в формате unix time
    """
    try:
        responce = requests.get(url=url_site, headers=headers_site)
        responce.encoding = 'utf-8'
        responce = responce.text
        course_crypto = {}
        all_currency = findall(pattern=re_pattern, string=responce)
        needed_currency = []
        for currency in all_currency:
            currency = currency[4:]
            currency = currency.split(split_pattern)
            needed_currency.append(currency)
        for currency in needed_currency:
            if currency[0] in name_space:
                course_crypto[name_space[currency[0]]] = currency[1]
        crypto = {
            'date': int(time()),
            'currency': dict(sorted(course_crypto.items()))
        }
    except Exception:
        crypto = {'date': int(time())}

    return crypto


def get_course_rub(url_site: str, name_space: dict) -> dict:
    """Функция парсит и обрабатывает данные, выдавая словарь с парами: иностраная валюта - рубль.

    Parameters
    ----------
    url_site : str
        ссылка на сайт для парсинга
    name_space :  dict
        словарь с необохдимыми валютами

    Exception
    ---------
        Если парсинг не удался, вернется словарь со значением даты в формате unix time
    """
    try:
        responce = requests.get(url=url_site)
        responce.encoding = 'utf-8'
        responce = responce.text
        course_rub = {}
        all_currency = xmltodict.parse(xml_input=responce)
        for currency in all_currency['ValCurs']['Valute']:
            if currency['Name'] in name_space:
                if currency['Name'] != 'Японских иен':
                    value_currency = currency['Value'].replace(',', '.')
                else:
                    value_currency = currency['Value'].replace(',', '.')
                    value_currency = round(float(value_currency)/100, 5)
                name_currency = name_space[currency['Name']]
                value_currency = str(value_currency) + '₽'
                course_rub[name_currency] = value_currency
        rub = {
            'date': int(time()),
            'currency': dict(sorted(course_rub.items()))
        }
    except Exception:
        rub = {'date': int(time())}

    return rub


def start_parse(currency: str) -> dict:
    """Функция вызывает одну из двух функций данного модуля (get_course_rub, get_course_crypto), в зависимости от переданного параметра.

    Parameters
    ----------
    currency : str
        валюта
    """
    if currency == '₽':
        course = get_course_rub(
            url_site=dict_to_parse['rub']['url'],
            name_space=dict_to_parse['rub']['name_rub']
        )
    else:
        course = get_course_crypto(
            url_site=dict_to_parse['crypto']['url'],
            headers_site=dict_to_parse['headers'],
            re_pattern=dict_to_parse['crypto']['re'],
            split_pattern=dict_to_parse['crypto']['split'],
            name_space=dict_to_parse['crypto']['name_crypto']
        )

    return course
