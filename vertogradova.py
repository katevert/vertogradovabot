import requests
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging
import random as rnd
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
MY_MENU, MY_ROUTER, MY_SOURCE1, MY_SOURCE2, MY_SOURCE3 = 1, 2, 3, 4, 5
def start(bot, update):
    update.message.reply_text('Я бот, который выдаёт разные факты из разных источников. Как Вас зовут?')

    return MY_MENU
def menu(bot, update, user_data):
    user_answer = update.message.text

    user_data['user_answer'] = user_answer
    update.message.reply_text('Приятно познакомиться, {}. Факт из какого источника Вы бы хотели узнать?'.format(user_answer),
        reply_markup=ReplyKeyboardMarkup(
            [['Получить факт из Advice Slip'],
             ['Получить факт из Cat Facts'],
             ['Получить факт из Chuck Norris facts']],
            one_time_keyboard=True,))

    return MY_ROUTER
def router(bot, update, user_data):
    route = update.message.text

    if route == 'Получить факт из Advice Slip':
        url = 'http://api.adviceslip.com/advice'

        response = requests.get(url).json()
        result = response['slip']['advice']

        update.message.reply_text('Случайный совет от Advice Slip: ' + result)
    elif route == 'Получить факт из Cat Facts':
        url='https://cat-fact.herokuapp.com/facts'
        
        response = requests.get(url).json()
        result = response['all'][rnd.randint(0, len(response['all']))]['text']
        
        update.message.reply_text('Случайный факт о животных: ' + result)
    elif route == 'Получить факт из Chuck Norris facts':
        url='https://api.chucknorris.io/jokes/random'
        
        response = requests.get(url).json()
        result = response['value']
        
        update.message.reply_text('Случайный факт о Чаке Норрисе: ' + result)


    return MY_MENU
def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)
def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("593655730:AAEPldQSWmvJLMyfnpTWNArdxVFYY3f6d2Q")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MY_MENU: [
                MessageHandler(
                    Filters.text,
                    menu,
                    pass_user_data=True,),],

            MY_ROUTER: [
                MessageHandler(
                    Filters.text,
                    router,
                    pass_user_data=True,),],
        },

        fallbacks=[],
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()