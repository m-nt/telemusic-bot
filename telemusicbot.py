#!/usr/bin/env python
import requests as req
import re
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
import Finder
import time
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

""" start = time.time()
result = Finder.Search("yavar hamishe momen")
end = time.time()
print("time taked: "+str(end-start))
print(result) """

# check if a string is ascii of not


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def echo(update: Update, context: CallbackContext):
    key = update.message.text
    if not is_ascii(key):
        update.message.reply_text("corrently we can't support this language, please try english.")
    else:
        start = time.time()
        result = Finder.Search(key, cache=True)
        end = time.time()
        output = "search result: time taked({})".format(round(end-start, 2))
        if result == None:
            update.message.reply_text("""not found""")
        else:
            keys = list(result.keys())[0]
            output += "\n{}\n\n{}".format(keys, result[keys])
            update.message.reply_text(output, parse_mode=ParseMode.HTML)


def main():
    updater = Updater("1620117997:AAFfJ3xbuU3KbEpqVPdXB4I_8TlhUg8w2tU", use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
