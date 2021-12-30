#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
REWRITE DESCRIPTION
"""

import logging
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Update, Bot
from flask import Flask, request
from db import TOKEN, PAIRINGS_SHEET, POINTS_TALLY_SHEET

app = Flask(__name__)
bot = Bot(token=TOKEN)
URL = "https://commaraderiebot.meganwee.repl.co"

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
    output_message = "Sorry! You're not a recognised participant :("

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
    output_message = "Sorry! You're not a recognised participant :("
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
    output_message = "Sorry! You're not a recognised participant :("

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

    # Start the Bot locally, removed due to app.run()
    # updater.start_polling() 

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond() -> None:
    update: Update = Update.de_json(request.get_json(force=True), bot)
    print(update)
    dispatcher = setup(bot)
    dispatcher.process_update(update)
    return "ok"


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s: bool = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        print("webhook setup ok")
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/removeWebhook', methods=['GET', 'POST'])
def remove_webhook():
    s: bool = bot.deleteWebhook(drop_pending_updates=True)
    if s:
        return "webhook removed"
    else:
        return "webhook removed unsuccessfully"


@app.route('/')
def index():
    return '.'

if __name__ == 'main':
    # note the threaded arg which allow your app to have more than one thread
    app.run("0.0.0.0", threaded=True)
    set_webhook()

'''
References:
https://www.codementor.io/@karandeepbatra/part-1-how-to-create-a-telegram-bot-in-python-in-under-10-minutes-19yfdv4wrq
https://elements.heroku.com/buttons/anshumanfauzdar/telegram-bot-heroku-deploy
https://www.dataquest.io/blog/python-api-tutorial/
https://docs.replit.com/tutorials/18-telegram-bot 
'''