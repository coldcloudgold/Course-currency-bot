"""Модуль для обработки входящих сообщений.

Function
--------
get_start()
    Функция реагирует на команду 'start'
get_help()
    функция реагирует на команду 'help'
callback_query()
    функция обработки инлайн клавиатуры
get_all()
    функция реагирует на сообщения пользователя
bot_is_alive(id_admin: str, type_update: str) -> None
    функция опповещения администратора о запуске бота
update_course_rub() -> dict
    функция для обновления курса рубля к инстранной валюте
update_course_crypto() -> dict
    функция для обновления курса доллара к криптовалюте
"""

from bot import *
from parse import start_parse
from database import write_user_db
from keyboard import k_info_about, k_next, k_course
from config import NAME_DATABASE, NAME_TABLE, dict_to_parse, SBERBANK_CARD, YANDEX_CARD


@bot.message_handler(commands=['start'])
def get_start(message):
    """Функция реагирует на команду 'start' и вызывает функцию для занесения пользователя в базу данных. \
Возвращает пользователю инлайн клавиатуру. \
Кнопка: 'Продолжить', коллбек кнопки: 'info_about'.

    Parameters
    ----------
    message : message
        автоматически полученные данные от пользователя
    """
    u_name = message.from_user.first_name
    c_id = message.chat.id
    data = write_user_db(name_db=NAME_DATABASE,
                         name_tb=NAME_TABLE, message=message)
    if data == []:
        info = f'{u_name}, этот бот отслеживает курс различных пар:\n\
Валюта - Рубль\n\
Криптовалюта - Доллар'
    else:
        info = f'Бот снова приветствует тебя, {u_name}.\n\
Этот бот отслеживает курс различных пар:\n\
Валюта - Рубль\n\
Криптовалюта - Доллар'
    k_board = k_info_about

    bot.send_message(chat_id=c_id, text=info, reply_markup=k_board)


@bot.message_handler(commands=['help'])
def get_help(message):
    """Функция реагирует на команду 'help'. \
Возвращает пользователю реплай клавиатуру. \
Кнопки: '₽' и '₿'.

    Parameters
    ----------
    message : message
        автоматически полученные данные от пользователя
    """
    c_id = message.chat.id
    info = f'Чтобы получить курс валют к рублю нажмите на кнопку: ₽\n\
Курс криптовалют к доллару: ₿'
    k_board = k_course

    bot.send_message(chat_id=c_id, text=info, reply_markup=k_board)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """Функция обработки инлайн клавиатуры. \
Возвращает пользователю колбек клавиатуру. \
Кнопка: 'Далее', коллбек кнопки: 'next'.

    Parameters
    ----------
    call : call
        автоматически полученные данные от пользователя
    """
    c_id = call.message.chat.id
    m_id = call.message.message_id
    if call.data == 'info_about':
        if SBERBANK_CARD and YANDEX_CARD:
            info = f'Вся информация берется из открытых источников.\n\
Если хотите поддержать автора, можете перевести деньги по номеру карты.\n\
Номер карты Сбербанк: {SBERBANK_CARD}\n\
Номер карты Яндекс: {YANDEX_CARD}\n\
Курс рубля: {dict_to_parse["rub"]["url_orginal"]}\n\
Курс криптовалют: {dict_to_parse["crypto"]["url"]}'
        else:
            info = f'Вся информация берется из открытых источников.\n\
Курс рубля: {dict_to_parse["rub"]["url_orginal"]}\n\
Курс криптовалют: {dict_to_parse["crypto"]["url"]}'
        k_board = k_next
    elif call.data == 'next':
        info = f'Для получения курса пар нажмите на соответсвующие кнопки:\n\
Валюта - Рубль: ₽\n\
Криптовалюта - Доллар: ₿'
        k_board = k_course

    bot.send_message(chat_id=c_id, text=info,
                     reply_markup=k_board, disable_web_page_preview=True)
    bot.edit_message_reply_markup(chat_id=c_id, message_id=m_id)


@bot.message_handler(content_types=['text'])
def get_all(message):
    """Функция реагирует на сообщения пользователя. \
Если сообщение содержит следующие слова: '₽', 'rub', 'ruble', 'руб', 'рубль' - запускается парсинг рубля к иностранной валюте. \
Если сообщение содержит следующие слова: '₿', 'crypto', 'cryptocurrency', 'крипто', 'криптовалюта' - запускается парсинг доллара к криптовалюте. \
Возвращает пользователю реплай клавиатуру. \
Кнопки: '₽' и '₿'.

    Parameters
    ----------
    message : message
        автоматически полученные данные от пользователя
    """
    c_id = message.chat.id
    m_text = message.text.lower()
    m_date = message.date
    k_board = k_course
    # Парсинг криптовалюты
    if m_text in dict_to_parse['crypto']['list']:
        if m_date-course_crypto['date'] < 300:
            if len(course_crypto) == 2:
                string = ''.join(f'{key}: {value}\n' for key,
                                 value in course_crypto['currency'].items())
                info = f'Курс ₿:\n{string}'
            else:
                info = f'К сожалению, запрос не удался и возникла ошибка.\n\
Повторите попытку позднее или ознакомьтесь с курсом лично, перейдя по ссылке: {dict_to_parse["crypto"]["url"]}'
                update_course_crypto()
        else:
            data_curency_crypto = start_parse('₿')
            course_crypto.clear()
            course_crypto.update(data_curency_crypto)
            if len(course_crypto) == 2:
                string = ''.join(f'{key}: {value}\n' for key,
                                 value in course_crypto['currency'].items())
                info = f'Курс ₿:\n{string}'
            else:
                info = f'К сожалению, запрос не удался и возникла ошибка.\n\
Повторите попытку позднее или ознакомьтесь с курсом лично, перейдя по ссылке: {dict_to_parse["crypto"]["url"]}'
                update_course_crypto()
    # Парсинг обычной валюты
    elif m_text in dict_to_parse['rub']['list']:
        if m_date-course_rub['date'] < 3600:
            if len(course_rub) == 2:
                string = ''.join(f'{key}: {value}\n' for key,
                                 value in course_rub['currency'].items())
                info = f'Курс ₽:\n{string}'
            else:
                info = f'К сожалению, запрос не удался и возникла ошибка.\n\
Повторите попытку позднее или ознакомьтесь с курсом лично, перейдя по ссылке: {dict_to_parse["rub"]["url_orginal"]}'
                update_course_rub()
        else:
            data_curency_rub = start_parse('₽')
            course_rub.clear()
            course_rub.update(data_curency_rub)
            if len(course_rub) == 2:
                string = ''.join(f'{key}: {value};\n' for key,
                                 value in course_rub['currency'].items())
                info = f'Курс ₽:\n{string}'
            else:
                info = f'К сожалению, запрос не удался и возникла ошибка.\n\
Повторите попытку позднее или ознакомьтесь с курсом лично, перейдя по ссылке: {dict_to_parse["rub"]["url_orginal"]}'
                update_course_rub()
    else:
        info = 'Бот реагирует только на 2 команды.'

    bot.send_message(chat_id=c_id, text=info,
                     reply_markup=k_board, disable_web_page_preview=True)


def bot_is_alive(id_admin: str, type_update: str) -> None:
    """Функция опповещения администратора о запуске бота.

    Parameters
    ----------
    id_admin : str
        уникальный идентификатор администратора
    type_update : str
        тип работы (longpoll, webhook)
    """
    info = f'Бот запустился.\nРаботает через: {type_update}'
    bot.send_message(chat_id=id_admin, text=info)


def update_course_rub() -> dict:
    """Функция для обновления курса рубля к иностранной валюте."""
    global course_rub
    course_rub = start_parse('₽')
    return course_rub


def update_course_crypto() -> dict:
    """Функция для обновления курса доллара к криптовалюте."""
    global course_crypto
    course_crypto = start_parse('₿')
    return course_crypto


if __name__ != '__main__':
    update_course_rub()
    update_course_crypto()
