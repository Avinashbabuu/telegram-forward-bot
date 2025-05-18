from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ParseMode
import logging

# === Configuration ===
TOKEN = "8059875822:AAFBJzNez7gTlIVqrMzQCpFybmoprmgNK1k"
SOURCE_CHANNEL_ID = -1002286453219
DEST_CHANNEL_ID = -1002106363303

# === Filters ===
filter_word = None
replace_word = None

# === Logging ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# === /filter command ===
def filter_command(update, context):
    update.message.reply_text("Enter the word you want to filter:")
    return 1

def set_filter_word(update, context):
    global filter_word
    filter_word = update.message.text
    update.message.reply_text(f"Word to filter: '{filter_word}'\nNow send the word to replace it with:")
    return 2

def set_replace_word(update, context):
    global replace_word
    replace_word = update.message.text
    update.message.reply_text(f"Filter set!\n'{filter_word}' will be replaced with '{replace_word}'")
    return -1


# === Forwarding logic ===
def forward_message(update, context):
    if update.effective_chat.id == SOURCE_CHANNEL_ID and update.message.text:
        msg = update.message.text
        if filter_word and replace_word:
            msg = msg.replace(filter_word, replace_word)
        context.bot.send_message(chat_id=DEST_CHANNEL_ID, text=msg, parse_mode=ParseMode.HTML)


# === Cancel command (optional) ===
def cancel(update, context):
    update.message.reply_text("Filter setup cancelled.")
    return -1


# === Main function ===
def main():
    from telegram.ext import ConversationHandler

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Conversation handler for /filter
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('filter', filter_command)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, set_filter_word)],
            2: [MessageHandler(Filters.text & ~Filters.command, set_replace_word)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.text & Filters.chat(SOURCE_CHANNEL_ID), forward_message))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
