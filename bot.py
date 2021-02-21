import logging

import telebot

from config import TOKEN


bot = telebot.TeleBot(token=TOKEN)
telebot.logger.setLevel(logging.INFO)
