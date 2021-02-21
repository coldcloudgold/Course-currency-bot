from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_keyboad_info_about():
    keyboad_info_about = InlineKeyboardMarkup()
    button_info = InlineKeyboardButton("Продолжить", callback_data='info_about')
    keyboad_info_about.add(button_info)
    return keyboad_info_about


def get_keyboad_next():
    keyboad_next = InlineKeyboardMarkup()
    button_next = InlineKeyboardButton("Далее", callback_data='next')
    keyboad_next.add(button_next)
    return keyboad_next


def get_keyboad_course():
    keyboad_course = ReplyKeyboardMarkup(resize_keyboard=True)
    button_rub = KeyboardButton(text='₽')
    button_crypto = KeyboardButton(text='₿')
    keyboad_course.add(button_rub, button_crypto)
    return keyboad_course


if __name__ != '__main__':
    k_info_about = get_keyboad_info_about()
    k_next = get_keyboad_next()
    k_course = get_keyboad_course()
