import logging

from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, CallbackQueryHandler
import os
from recipe_search_bot.recipe_search_bot.data_base_and_user import data_base

from recipe_search_bot.recipe_search_bot.parser import ParserForRequest
from recipe_search_bot.recipe_search_bot.parser import generate_url

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
    url = generate_url(types=['салат', 'суп', 'второе блюдо'],
                       kitchen=['домашняя', 'европейская'],
                       time=['20-40 минут', '40-60 минут', '60-90 минут', '90-120 минут'])

    parser = ParserForRequest(url)
    print(parser)



async def button(update, context):
    query = update.callback_query
    await query.answer()

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
