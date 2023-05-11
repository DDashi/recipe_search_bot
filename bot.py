import logging

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, CallbackQueryHandler
import os
from data_base_and_user import data_base

# настроим модуль ведения журнала логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="I'm a bot, please talk to me!")


async def echo(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def send_piture(update, context):
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo='https://www.gastronom.ru/binfiles/images/20170208/m2faa08a.jpg')


async def get_recipes(update, context):
    #update.message.reply_text("Beginning of inline keyboard")
    keyboard = [
        [
            InlineKeyboardButton("Button 1", callback_data='1'),
            InlineKeyboardButton("Button 2", callback_data='2'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    #update.message.reply_text("Replying to text", reply_markup=reply_markup)

    await context.bot.send_message(chat_id=update.effective_chat.id, text="aga", reply_markup=reply_markup)


async def button(update, context):
    query = update.callback_query
    query.answer()

    # This will define which button the user tapped on (from what you assigned to "callback_data". As I assigned them "1" and "2"):
    choice = query.data

    # Now u can define what choice ("callback_data") do what like this:
    if choice == '1':
        print("a")

    if choice == '2':
        print('b')

if __name__ == '__main__':
    TOKEN = os.environ["TOKEN"]
    # создание экземпляра бота через `ApplicationBuilder`
    application = ApplicationBuilder().token(TOKEN).build()


    # создаем обработчик
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    img_handler = CommandHandler('img', send_piture)
    keyboard_handler = CommandHandler('recipes', get_recipes)
    button_handler = CallbackQueryHandler(button)
    # регистрируем обработчик в приложение
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(img_handler)
    application.add_handler(keyboard_handler)
    application.add_handler(button_handler)
    # запускаем приложение

    application.run_polling()
