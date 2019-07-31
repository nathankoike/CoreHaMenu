"""
    Proj: CoreHaMenu - a menu fetching bot (Telegram Bot Section)
    Auth: Ken Fung
    Desc: Allows the user to access information from Hamilton College's
    food services menus from a Telegram bot
"""

# Universally Unique Identifier, because telegram requires UUID for requests passed to the bot
from uuid import uuid4

# some telegram stuff, because this is a telegram bot, after all...
import telegram
from telegram.utils.helpers import escape_markdown
from telegram import InlineQueryResultArticle, Chat, User, ParseMode, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler

# Modules for HTML, json and ast to make things easier for the bot to read!
import json
import requests
import ast

# The logging module
import logging


# For logging purposes
#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                    level=logging.INFO)
#
#logger = logging.getLogger(__name__)

# The start message!
def start(bot, update):
    update.message.reply_text('Hi! Type @Mc125_Bot to begin!')

#--------------------------------------
# Preparation of materials that will go into either a slash command response or an inline menu request response

seperator = '\n'

commons_intro = 'Commons Food!'
commons_URL = 'https://hamilton.cafebonappetit.com/cafe/soper-commons-cafe/'

commons_list = []
commons_list.append(commons_intro)
commons_list.append(commons_URL)
commons_spaced_list = seperator.join(commons_list)

commons_dinner_intro = 'Commons Dinner Food!'
print(commons_dinner_intro)

commons_dinner_list = []
t = open("dinner_home_list", "r")
t_new = ast.literal_eval(t.read())
for x in t_new:
    commons_dinner_list.append(x.title())
commons_dinner_spaced_list = seperator.join(commons_dinner_list)

commons_omelets_intro = 'Commons Omelet List!'
print(commons_omelets_intro)

commons_omelets_list = []
t = open("breakfast_omelet_list", "r")
t_new = ast.literal_eval(t.read())
for x in t_new:
    commons_omelets_list.append(x.title())
commons_omelets_spaced_list = seperator.join(commons_omelets_list)

mcewen_intro = 'McEwen Food!'
mcewen_URL = 'https://hamilton.cafebonappetit.com/cafe/mcewens-green-cafe/'

mcewen_list = []
mcewen_list.append(mcewen_intro)
mcewen_list.append(mcewen_URL)
mcewen__spaced_list = seperator.join(mcewen_list)

diner_intro = 'Diner Food!'
diner_URL = 'https://hamilton.cafebonappetit.com/cafe/the-howard-diner/'

diner_list = []
diner_list.append(diner_intro)
diner_list.append(diner_URL)
diner_spaced_list = seperator.join(diner_list)

#------------------------------------------------


# When the word after def is typed into telegram following a slash (e.g.: /commons), display
# the relevant information
def commons(bot, update):
    update.message.reply_text(text = ("*"+str(commons_omelets_intro)+"*" + "\n" + str(commons_omelets_spaced_list) + "\n\n" + "*"+str(commons_dinner_intro)+"*" + "\n" + str(commons_dinner_spaced_list)) ,parse_mode=telegram.ParseMode.MARKDOWN)

def mcewen(bot, update):
    update.message.reply_text(str(mcewen__spaced_list), parse_mode)

def diner(bot, update):
    update.message.reply_text(str(diner__spaced_list))

# The inline query code
def inlinequery(bot, update):
    """Handle the inline query."""
    #So I type "@Mc125_Bot" followed by a space...
    query = update.inline_query.query

    #...and these are the things that pop out!
    results = [

        InlineQueryResultArticle(
            id=uuid4(),
            title="The Howard Diner",
            input_message_content=
            InputTextMessageContent("https://hamilton.cafebonappetit.com/cafe/the-howard-diner/",parse_mode=ParseMode.MARKDOWN),
            description="Diner Food!",
            thumb_url="https://hamilton.cafebonappetit.com/content/themes/bamco/img/theme/cafe_bamco_logo-new.png"),

        InlineQueryResultArticle(
            id=uuid4(),
            title="McEwen",
            input_message_content=
            InputTextMessageContent("https://hamilton.cafebonappetit.com/cafe/mcewens-green-cafe/",parse_mode=ParseMode.MARKDOWN),
            description="McEwen Food!",
            thumb_url="https://hamilton.cafebonappetit.com/content/themes/bamco/img/theme/cafe_bamco_logo-new.png"),

        InlineQueryResultArticle(
            id=uuid4(),
            title="Commons",
            input_message_content=
            InputTextMessageContent("https://hamilton.cafebonappetit.com/cafe/soper-commons-cafe/",parse_mode=ParseMode.MARKDOWN),
            description="Commons Food!",
            thumb_url="https://hamilton.cafebonappetit.com/content/themes/bamco/img/theme/cafe_bamco_logo-new.png"),

        InlineQueryResultArticle(
            id=uuid4(),
            title="Hill Card Refill",
            input_message_content=
            InputTextMessageContent("https://hamilton-sp.blackboard.com/eaccounts/AnonymousHome.aspx",parse_mode=ParseMode.MARKDOWN),
            description="It's as if Hamilton hasn't taken enough of our money yet!",
            thumb_url="https://upload.wikimedia.org/wikipedia/commons/0/00/Hamilton_Continentals_logo.png"),

        InlineQueryResultArticle(
            id=uuid4(),
            title="Blackboard",
            input_message_content=
            InputTextMessageContent("https://blackboard.hamilton.edu/",parse_mode=ParseMode.MARKDOWN),
            description="See your classes and stuff!",
            thumb_url="https://en.wikipedia.org/wiki/Blackboard_Inc.#/media/File:Blackboard_Inc._logo.png")
        ]

    #Once the user clicks enter, the results will pop out!
    update.inline_query.answer(results)


# For diagnostics purposes
#def error(bot, update, error):
#    """Log Errors caused by Updates."""
#    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("Get the Token from the Telegram BotFather")

    # Activate the bot's ability to accept slash commands!
    dp = updater.dispatcher

    # Slash command list!
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("diner", diner))
    dp.add_handler(CommandHandler("mcewen", mcewen))
    dp.add_handler(CommandHandler("commons", commons))

    # When the user pings the bot and presses space,
    # the inline menu will appear!
    dp.add_handler(InlineQueryHandler(inlinequery))

    # For error logging purposes
    dp.add_error_handler(error)

    # Bot begin!
    updater.start_polling()

    # The bot will run until someone presses Ctrl-C on the terminal that the bot is running on!
    updater.idle()

if __name__ == '__main__':
    main()
