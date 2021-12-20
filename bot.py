#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
REWRITE DESCRIPTION
"""

import logging
import os
import requests
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

PORT = int(os.environ.get('PORT', 5000))
TOKEN = "5066378494:AAF7F9kK6JfPjsR0rricjqhGvcrnB80zSzk"
PAIRINGS_SHEET = "https://api.sheety.co/88b03a94afafb9c4b54898d7a83e64de/coMaraderieBot/pairings"
POINTS_TALLY_SHEET = "https://api.sheety.co/88b03a94afafb9c4b54898d7a83e64de/coMaraderieBot/pointsTally"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Welcome to COMpanion :>')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Please contact @___ for more help!')


def nonCommand(update, context):
    """Inform the user that the command was not entered correctly"""
    # update.message.reply_text(update.message.text) # same message
    update.message.reply_text("Sorry! \"" + update.message.text + "\" is not a recognised command :(")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def companion(update, context):
    teleHandle = "@" + update.message.from_user.username
    output_message = "Hi " + update.message.from_user.first_name + "! These are the details of your pairing:\n\n"
    response = requests.get(PAIRINGS_SHEET) #response is a requests.Response Object
    response_json = response.json() #transforms response into json format

    for person in response_json["pairings"]:
        # print(person)
        if person['teleHandle'] == teleHandle or person['telegramHandle'] == teleHandle:
            output_message += "Name: {}\nTelegram Handle: {}\nYear: {}\nMajor: {}\nInterests: {}\nPersonality Quiz Answers: {}\nPair Code: {}\n\n".format(
                person["name"], person["teleHandle"], person["year"], person["major"], person["interests"], person["personalityQuizAnswers"], person["pairCode"]
            )

    # print(output_message)
    update.message.reply_text(output_message)

def credits(update, context):
    teleHandle = "@" + update.message.from_user.username
    output_message = "Haro " + update.message.from_user.first_name + "! These are your pair's SOCial Credits (points) so far:\n\n"
    response = requests.get(POINTS_TALLY_SHEET) #response is a requests.Response Object
    response_json = response.json() #transforms response into json format
    # update.message.reply_text(response.text)

    for pair in response_json["pointsTally"]:
        # print(person)
        if pair['firstPersonTele'] == teleHandle or pair['secondPersonTele'] == teleHandle:
            output_message += "Point Tally: {}\nRanking: {}".format(pair["pointTally"], pair["ranking"])

    # print(output_message)
    update.message.reply_text(output_message)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("companion", companion))
    dp.add_handler(CommandHandler("credits", credits))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, nonCommand))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(PORT),
    #                       url_path=TOKEN)
    # updater.bot.setWebhook('https://yourherokuappname.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

'''
References:
https://www.codementor.io/@karandeepbatra/part-1-how-to-create-a-telegram-bot-in-python-in-under-10-minutes-19yfdv4wrq
https://elements.heroku.com/buttons/anshumanfauzdar/telegram-bot-heroku-deploy
https://www.dataquest.io/blog/python-api-tutorial/
'''