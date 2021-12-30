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

PORT = int(os.environ.get('PORT', '8443'))
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
    update.message.reply_text('Please contact @COMaraderie for more help!')


def nonCommand(update, context):
    """Inform the user that the command was not entered correctly"""
    # update.message.reply_text(update.message.text) # same message
    update.message.reply_text("Sorry! \"" + update.message.text + "\" is not a recognised command :(")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def checkcompanion(update, context):
    teleHandle = "@" + update.message.from_user.username
    response = requests.get(PAIRINGS_SHEET) #response is a requests.Response Object
    response_json = response.json() #transforms response into json format

    for person in response_json["pairings"]:
        # print(person)
        if person['telegramHandle'] == teleHandle:
            output_message = "Your COMpanion is {}!\nTelegram handle: {}\nYear/Course: {}/{}\nInterests: {}\nKind of COMpanion they’re looking for : {}\n\n".format(
                person["name"], person["teleHandle"], person["year"], person["major"], person["interests"], person["personalityQuizAnswers"])
            break
    # print(output_message)
    update.message.reply_text(output_message)

def checksocialxp(update, context):
    teleHandle = "@" + update.message.from_user.username
    response = requests.get(POINTS_TALLY_SHEET) #response is a requests.Response Object
    response_json = response.json() #transforms response into json format
    updatedAsOf = ""
    # update.message.reply_text(response.text)

    for pair in response_json["pointsTally"]:
        if pair['firstPerson'] == "" and pair['secondPerson'] == "" and pair['pointTally'] == "":
            updatedAsOf = pair['updatedAsOf']

        if pair['firstPersonTele'] == teleHandle:
            output_message = "You and {} have {} SOCial XP as of {}".format(pair['secondPerson'], pair['pointTally'], updatedAsOf)
            break
        if pair['secondPersonTele'] == teleHandle:
            output_message = "You and {} have {} SOCial XP as of {}".format(pair['firstPerson'], pair['pointTally'], updatedAsOf)
            break
    update.message.reply_text(output_message)

def checkpaircode(update, context):
    teleHandle = "@" + update.message.from_user.username
    response = requests.get(PAIRINGS_SHEET) #response is a requests.Response Object
    response_json = response.json() #transforms response into json format

    for person in response_json["pairings"]:
        # print(person)
        if person['teleHandle'] == teleHandle:
            output_message = "Your unique pair code with {} is {}".format(
                person["pairName"], person["pairCode"])
            break
        
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
    dp.add_handler(CommandHandler("checkcompanion", checkcompanion))
    dp.add_handler(CommandHandler("checksocialxp", checksocialxp))
    dp.add_handler(CommandHandler("checkpaircode", checkpaircode))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, nonCommand))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling() # this is to run the bot locally
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(PORT),
    #                       url_path=TOKEN)
    # updater.bot.setWebhook('https://comaraderiebot.herokuapp.com/' + TOKEN)

    updater.idle()


if __name__ == '__main__':
    main()

'''
References:
https://www.codementor.io/@karandeepbatra/part-1-how-to-create-a-telegram-bot-in-python-in-under-10-minutes-19yfdv4wrq
https://elements.heroku.com/buttons/anshumanfauzdar/telegram-bot-heroku-deploy
https://www.dataquest.io/blog/python-api-tutorial/
'''