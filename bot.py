import logging
import json

from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, CallbackQueryHandler
import os
from data_base_and_user import data_base

from parsers import ParserForRequest
from parsers import generate_url
from parsers import open_file
from inline_keyboard import InlineKeyboard


recipes_enumerator = InlineKeyboard(
    [('Меню', 'menu'), ('Следующий', 'next'), ('Предыдущий', 'previous'), ('Показать', 'open')],
    1, 4).get_keyboard()
menu_enumerator = InlineKeyboard(
    [('Найти рецепт', 'find'), ('Избранное', 'favourites')],
    1, 2).get_keyboard()
filters_enumerator = InlineKeyboard(
    [('Название рецепта', 'title'), ('Тип блюда', 'type'), ('Кухня', 'cuisine'),
     ('Желаемые ингридиенты', 'unwanted_ingr'), ('Нежелаемые ингридиенты', 'wanted_ingr'),
     ('Время приготовления', 'time'),('Должно ли блюдо быть вегетарианским', 'vegetarian')],
    5, 1).get_keyboard()


def dict_to_keyboard(data):
    keyboard = []
    for key, value in data.items():
        keyboard.append((key, value))
    keyboard.append(('Назад', 'previous'))
    return InlineKeyboard(keyboard, len(keyboard), 1).get_keyboard()


type_of_dish_filter = dict_to_keyboard(open_file('parsers\\filters\\type_of_dish.json'))
#type_of_kitchen_filter = dict_to_keyboard(open_file('parsers\\filters\\type_of_kitchen.json'))
amount_of_time_filter = dict_to_keyboard(open_file('parsers\\filters\\amount_of_time.json'))


# настроим модуль ведения журнала логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def get_keyboard(update, context, keyboard, text):
    message = await context.bot.send_message(chat_id=update.effective_chat.id,
                                   reply_markup=keyboard,
                                   text=text)
    data_base.create(update.effective_chat.id, message_id=message.message_id)
    data_base.save()


async def get_keyboard_with_photo(update, context, keyboard, text, photo):
    message = await context.bot.send_photo(chat_id=update.effective_chat.id,
                                            reply_markup=keyboard,
                                            caption=text,
                                            photo=photo)
    data_base.create(update.effective_chat.id, message_id=message.message_id)
    data_base.save()


async def start(update, context):
    await get_keyboard(update, context,
                       menu_enumerator,
                       'Привет! Я бот, предназначенный для поиска рецептов.')


async def find_filter(update, context):
    await get_keyboard(update, context,
                       filters_enumerator,
                       'Вы можете выбрать нужные вам фильтры для поиска рецептов:')


async def error(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Ошибка! Неизвестная команда.")


async def get_recipes(update, context, parser):
    page = parser.pages[0]
    await get_keyboard_with_photo(update, context,
                                  recipes_enumerator,
                                  page.img.description + '\n' + page.title,
                                  page.img.img)


async def get_type_of_dish_filter(update, context):
    await get_keyboard(update, context,
                       type_of_dish_filter,
                        "Выберете, блюда какого типа вы ищете:")


async def delete_message(update, context, message_id):
    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message_id)


async def button(update, context):
    query = update.callback_query

    choice = query.data
    user = data_base.get_user(update.effective_chat.id)

    if choice == 'find':
        await delete_message(update, context, user.message_id)
        await find_filter(update, context)
    elif choice == 'type':
        await delete_message(update, context, user.message_id)
        await get_type_of_dish_filter(update, context)



if __name__ == '__main__':
    TOKEN = os.environ["TOKEN"]
    # создание экземпляра бота через `ApplicationBuilder`
    application = ApplicationBuilder().token(TOKEN).build()

    # создаем обработчик
    start_handler = CommandHandler('start', start)
    keyboard_handler = CommandHandler('recipes', get_recipes)
    error_handler = MessageHandler(filters.COMMAND, error)
    button_handler = CallbackQueryHandler(button)
    find_handler = CommandHandler('find', find_filter)
    # регистрируем обработчик в приложение
    application.add_handler(start_handler)
    application.add_handler(keyboard_handler)
    application.add_handler(button_handler)
    application.add_handler(find_handler)
    application.add_handler(error_handler)
    # запускаем приложение

    application.run_polling()
