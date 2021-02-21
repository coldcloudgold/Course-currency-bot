from time import sleep

from flask import Flask, request

from handlers_and_function import *
from database import create_db
from config import ADMIN, TOKEN, HEROKU, HEROKU_APP, PORT


if __name__ == "__main__":
    create_db(name_db=NAME_DATABASE, name_tb=NAME_TABLE)
    if not HEROKU:
        info = 'LONGPOLL'
        bot_is_alive(id_admin=ADMIN, type_update=info)
        bot.remove_webhook()
        sleep(0.1)
        bot.polling(none_stop=True)
    elif HEROKU and HEROKU_APP:
        info = 'WEBHOOK'
        bot_is_alive(id_admin=ADMIN, type_update=info)
        server = Flask(__name__)
        # server.debug = True
        bot.remove_webhook()
        sleep(0.1)
        bot.set_webhook(url=f'{HEROKU_APP}{TOKEN}')

        @server.route('/' + TOKEN, methods=['POST'])
        def getMessage():
            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            bot.process_new_updates(
                [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
            return "!", 200

        server.run(host="0.0.0.0", port=int(PORT))
