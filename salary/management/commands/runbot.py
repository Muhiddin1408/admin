from django.core.management import BaseCommand

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from config.settings import TOKEN
from ..start import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        updater = Updater(TOKEN)
        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(MessageHandler(filters=Filters.all & Filters.chat_type.private, callback=begin))
        updater.start_polling()
        updater.idle()
