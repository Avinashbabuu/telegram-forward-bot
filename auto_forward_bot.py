# auto_forward_bot.py

from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# BOT TOKEN
BOT_TOKEN = "8059875822:AAFBJzNez7gTlIVqrMzQCpFybmoprmgNK1k"

# Chat IDs (aapko channel ID lena hoga)
SOURCE_CHANNEL_ID = -1002286453219  # Replace with your source channel ID
DEST_CHANNEL_ID = -1002106363303    # Replace with your destination channel ID

def forward_message(update: Update, context: CallbackContext):
    if update.channel_post:
        context.bot.forward_message(
            chat_id=DEST_CHANNEL_ID,
            from_chat_id=SOURCE_CHANNEL_ID,
            message_id=update.channel_post.message_id
        )

updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(Filters.chat(SOURCE_CHANNEL_ID), forward_message))

updater.start_polling()
updater.idle()
