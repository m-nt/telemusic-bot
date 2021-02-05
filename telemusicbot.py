#!/usr/bin/env python
import requests as req
import re
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, Handler
import logging
import Finder
import time
import json
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def echo(update: Update, context: CallbackContext):
    key = update.message.text
    if not is_ascii(key):
        update.message.reply_text("corrently we can't support this language, please try english.")
    else:
        result = {}
        start = time.time()
        for i in range(0, 45, 3):
            find = Finder.CacheSearch(key, i)
            if find != None:
                keys = list(find.keys())[0]
                result[keys] = find[keys]
        end = time.time()
        output = "search result ({} seconds)\n--------------------------------------------\n".format(round(end-start, 2))

        #keys = list(result.keys())[0]
        for i in range(len(result)-1, -1, -1):
            key = list(result.keys())[i]
            output += "\n{}: {}\ndownload: /{}\n--------------------------------------------\n".format(
                i+1, result[key], key)
        update.message.reply_text(output, parse_mode=ParseMode.HTML)


def download(update: Update, context: CallbackContext):
    hash = update.message.text.replace("/", "")
    with open("Links.txt", mode="r") as file:
        items = file.read()
    link = re.findall('^{}.*'.format(hash), items, flags=re.M)[0].split('[seprator]')
    update.message.reply_document(link[2].replace('\\n', ''))


def updateed():
    print("hey yo")


def main():
    updater = Updater("1620117997:AAFfJ3xbuU3KbEpqVPdXB4I_8TlhUg8w2tU", use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.command, download))
    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
