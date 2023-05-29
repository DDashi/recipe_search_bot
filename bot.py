import logging

from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, CallbackQueryHandler
import os
from data_base_and_user import data_base

from parsers import ParserForRequest
from parsers import generate_url
from parsers import open_file
from inline_keyboard import InlineKeyboard
from parsers.parser_for_recipes import ParserForRecipes

recipes_enumerator = InlineKeyboard(
    [('меню', 'start'), ('предыдущий', 'previous'), ('следующий', 'next'), ('показать', 'open'),
     ('выбрать другие фильтры', 'find')],
    1, 5).get_keyboard()
menu_enumerator = InlineKeyboard(
    [('найти рецепт', 'find'), ('избранное', 'favourites')],
    1, 2).get_keyboard()
filter_page = {'название рецепта': 'title',
               'тип блюда': 'type',
               'кухня': 'cuisine',
               'желаемые ингридиенты': 'wanted_ingr',
               'нежелаемые ингридиенты': 'unwanted_ingr',
               'время приготовления': 'time',

               'применить фильтры': 'get_recipes',
               'сбросить фильтры': 'reset',
               'меню': 'start'}
recipe_page = InlineKeyboard(
    [('меню', 'start'), ('назад', 'back'), ('предыдущий шаг', 'previous_step'),
     ('следующий шаг', 'next_step'), ('добавить в избранное', 'add')],
    1, 5).get_keyboard()
favourites_enumerator = InlineKeyboard(
    [('меню', 'start'), ('предыдущий', 'previous_favourites'), ('следующий', 'next_favourites'),
     ('показать', 'open_favourites'), ('удалить из избранного', 'remove')],
    1, 5).get_keyboard()
favourites_open_page = InlineKeyboard(
    [('меню', 'start'), ('назад', 'back_favourites'), ('предыдущий шаг', 'previous_favourites_step'),
     ('следующий шаг', 'next_favourites_step'), ('удалить из избранного', 'remove')],
    1, 5).get_keyboard()


def dict_to_keyboard(data):
    keyboard = []
    for key, value in data.items():
        keyboard.append((key, value))
    if 'меню' not in data:
        keyboard.append(('назад', 'find'))
    return InlineKeyboard(keyboard, len(keyboard), 1).get_keyboard()


type_of_dish = open_file('parsers\\filters\\type_of_dish.json')
type_of_kitchen = open_file('parsers\\filters\\type_of_kitchen.json')
amount_of_time = open_file('parsers\\filters\\amount_of_time.json')

# настроим модуль ведения журнала логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def get_keyboard(update, context, keyboard, text, recipe_number=None):
    message = await context.bot.send_message(chat_id=update.effective_chat.id,
                                             reply_markup=keyboard,
                                             text=text)
    data_base.create(str(update.effective_chat.id), message_id=message.message_id, message_text=text,
                     recipe_number=recipe_number)
    data_base.save()


def normalize_filters(context):
    context.user_data.clear()
    context.user_data['title'] = []
    context.user_data['cuisine'] = []
    context.user_data['wanted_ingr'] = []
    context.user_data['unwanted_ingr'] = []
    context.user_data['vegetarian'] = False


async def get_keyboard_with_photo(update, context, keyboard, text, photo, recipe_number=None):
    message = await context.bot.send_photo(chat_id=update.effective_chat.id,
                                           reply_markup=keyboard,
                                           caption=text,
                                           photo=photo)
    data_base.create(str(update.effective_chat.id), message_id=message.message_id, message_text=text,
                     recipe_number=recipe_number)
    data_base.save()


async def start(update, context):
    await get_keyboard(update, context,
                       menu_enumerator,
                       'Привет! Я бот, предназначенный для поиска рецептов.')


async def find_filter(update, context):
    new_keyboard = dict_to_keyboard(get_keyboard_with_filters(context, filter_page))
    await get_keyboard(update, context,
                       new_keyboard,
                       'Вы можете выбрать нужные вам фильтры для поиска рецептов:')


async def error(update, context):
    await send_message(update, context, "Ошибка! Неизвестная команда.")
    await start(update, context)


def get_parser(context):
    filters_types = []
    filters_time = []
    for val in context.user_data.keys():
        if val in type_of_dish and context.user_data[val]:
            filters_types.append(val)
        if val in amount_of_time and context.user_data[val]:
            filters_time.append(val)
    if context.user_data['title'] == [] \
            and context.user_data['cuisine'] == [] \
            and context.user_data['wanted_ingr'] == [] \
            and context.user_data['unwanted_ingr'] == [] \
            and not context.user_data['vegetarian'] \
            and filters_types == [] \
            and filters_time == []:
        url = generate_url()
    else:
        if context.user_data['title'] == []:
            context.user_data['title'] = None
        else:
            context.user_data['title'] = context.user_data['title'][0]

        url = generate_url(name=context.user_data['title'],
                           kitchen=context.user_data['cuisine'],
                           iningr=context.user_data['wanted_ingr'],
                           exingr=context.user_data['unwanted_ingr'],
                           types=filters_types,
                           time=filters_time,
                           veget=context.user_data['vegetarian'])
        if context.user_data['title'] == None:
            context.user_data['title'] = []
        else:
            context.user_data['title'] = [context.user_data['title']]
    context.user_data['url'] = url
    print(url)
    parser = ParserForRequest(url)
    return parser


async def get_recipes(update, context, page, recipe_number):
    await get_keyboard_with_photo(update, context,
                                  recipes_enumerator,
                                  page.img.description + '\n' + page.title,
                                  page.img.img,
                                  recipe_number)


async def get_favourites(update, context, page, recipe_number):
    await get_keyboard_with_photo(update, context,
                                  favourites_enumerator,
                                  page.description,
                                  page.img,
                                  recipe_number)


async def get_step(update, context, step, recipe_number):
    if step.img is None:
        await get_keyboard(update, context,
                           recipe_page,
                           step.description,
                           recipe_number)
    else:
        await get_keyboard_with_photo(update, context,
                                      recipe_page,
                                      step.description,
                                      step.img,
                                      recipe_number)


async def get_favourites_step(update, context, step, recipe_number):
    if step.img is None:
        await get_keyboard(update, context,
                           favourites_open_page,
                           step.description,
                           recipe_number)
    else:
        await get_keyboard_with_photo(update, context,
                                      favourites_open_page,
                                      step.description,
                                      step.img,
                                      recipe_number)


async def get_type_of_dish_filter(update, context):
    new_keyboard = dict_to_keyboard(get_keyboard_with_filters(context, type_of_dish))
    await get_keyboard(update, context,
                       new_keyboard,
                       "Выберете, блюда какого типа вы ищете:")


async def get_amount_of_time_filter(update, context):
    new_keyboard = dict_to_keyboard(get_keyboard_with_filters(context, amount_of_time))
    await get_keyboard(update, context,
                       new_keyboard,
                       "Выберете время приготовления:")


suitable_messages_to_respond_to = {"title": "Введите название блюда",
                                   "unwanted_ingr": "Введите через запятую(без пробела) названия не желательных ингредиентов\n"
                                                    "Например: апельсин,лимон",
                                   "wanted_ingr": "Введите через запятую(без пробела) названия нужных ингредиентов\n"
                                                  "Например: морковка,лук",
                                   "cuisine": "Введите через запятую(без пробела) названия кухни\n"
                                              "Например: японская,китайская"}


async def get_message(update, context):
    user = data_base.get_user(update.effective_chat.id)
    if user.message_text == suitable_messages_to_respond_to["cuisine"]:
        text = update.message.text.split(',')
        for word in text:
            if word in type_of_kitchen:
                context.user_data["cuisine"].append(word)
            else:
                await send_message(update, context, "Ошибка! Текст не распознан.")
                break
        await context.bot.edit_message_text(chat_id=update.message.chat_id,
                                            message_id=user.message_id,
                                            text=user.message_text)
        await find_filter(update, context)
    elif user.message_text in suitable_messages_to_respond_to.values():
        command = ""
        for comm, val in suitable_messages_to_respond_to.items():
            if user.message_text == val:
                command = comm
                break
        text = update.message.text.split(',')
        for word in text:
            context.user_data[command].append(word)

        await context.bot.edit_message_text(chat_id=update.message.chat_id,
                                            message_id=user.message_id,
                                            text=user.message_text)
        await find_filter(update, context)
    else:
        await send_message(update, context, "Ошибка! Текст не распознан.")
        await start(update, context)


async def send_message(update, context, text):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text)


async def delete_message(update, context, message_id):
    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message_id)


def get_keyboard_with_filters(context, keyboard):
    new_keyboard = {}

    if "кухня" in keyboard and context.user_data['vegetarian']:
        new_keyboard['вегетарианское блюдо✅'] = 'vegetarian'

    elif 'кухня' in keyboard and not context.user_data['vegetarian']:
        new_keyboard['вегетарианское блюдо'] = 'vegetarian'

    for button in keyboard:
        if button in context.user_data and context.user_data[button]:
            new_keyboard[button + '✅'] = keyboard[button]
        elif button in context.user_data:
            new_keyboard[button] = keyboard[button]
        else:
            new_keyboard[button] = keyboard[button]

    return new_keyboard


async def save_filters(update, context, choice, user):
    if choice in context.user_data:
        context.user_data[choice] = not context.user_data[choice]
    else:
        context.user_data[choice] = True
    print(context.user_data[choice], choice)
    await delete_message(update, context, user.message_id)


async def button(update, context):
    query = update.callback_query

    choice = query.data
    user = data_base.get_user(update.effective_chat.id)

    print(choice)
    if choice == 'find':
        if len(context.user_data) == 0:
            normalize_filters(context)
        await delete_message(update, context, user.message_id)
        await find_filter(update, context)

    elif choice == 'start':
        normalize_filters(context)
        await delete_message(update, context, user.message_id)
        await start(update, context)

    elif choice == 'reset':
        await send_message(update, context, 'Фильтры были сборшены')
        normalize_filters(context)

    elif choice == 'type':
        await delete_message(update, context, user.message_id)
        await get_type_of_dish_filter(update, context)

    elif choice == 'time':
        await delete_message(update, context, user.message_id)
        await get_amount_of_time_filter(update, context)

    elif choice == 'title' or choice == 'unwanted_ingr' \
            or choice == 'wanted_ingr' or choice == 'cuisine':
        await delete_message(update, context, user.message_id)
        await get_keyboard(update, context,
                           InlineKeyboard([('назад', 'find')], 1, 1).get_keyboard(),
                           suitable_messages_to_respond_to[choice])

    elif choice in type_of_dish.values():
        for type, value in type_of_dish.items():
            if value == choice:
                await save_filters(update, context, type, user)
                break
        await get_type_of_dish_filter(update, context)

    elif choice in amount_of_time.values():
        for type, value in amount_of_time.items():
            if value == choice:
                await save_filters(update, context, type, user)
                break
        await get_amount_of_time_filter(update, context)

    elif choice == 'vegetarian':
        await save_filters(update, context, choice, user)
        await find_filter(update, context)

    elif choice == 'get_recipes':
        await delete_message(update, context, user.message_id)
        parser = get_parser(context)
        if parser.pages_count == 0:
            await get_keyboard(update, context,
                               InlineKeyboard([('назад', 'find')], 1, 1).get_keyboard(),
                               "Рецепты не найдены")
        else:
            await get_recipes(update, context, parser.pages[0], (0, 0))

    elif choice == 'next':
        await delete_message(update, context, user.message_id)
        parser = get_parser(context)
        recipe_number = user.recipe_number[0] + 1
        if int(recipe_number) > parser.pages_count or parser.pages_count == 0:
            await get_keyboard(update, context,
                               InlineKeyboard([('назад', 'previous')], 1, 1).get_keyboard(),
                               "Рецепты по таким фильтрам закончились")
        else:
            await get_recipes(update, context, parser.pages[recipe_number], (recipe_number, 0))

    elif choice == 'previous':
        await delete_message(update, context, user.message_id)
        parser = get_parser(context)
        recipe_number = user.recipe_number[0] - 1
        if int(recipe_number) <= -1 or parser.pages_count == 0:
            recipe_number = 0
            await send_message(update, context, 'Вы уже на 1-ом рецепте')
        await get_recipes(update, context, parser.pages[recipe_number], (recipe_number, 0))

    elif choice == 'open':
        await delete_message(update, context, user.message_id)
        recipe_parser = get_parser(context)
        recipe_number = user.recipe_number[0]
        parser = ParserForRecipes(recipe_parser.pages[recipe_number].href)
        await get_step(update, context, parser.steps[0], (recipe_number, 0))

    elif choice == 'next_step':
        await delete_message(update, context, user.message_id)
        recipe_parser = get_parser(context)
        recipe_number, recipe_step = user.recipe_number
        recipe_step += 1
        parser = ParserForRecipes(recipe_parser.pages[recipe_number].href)
        if recipe_step >= len(parser.steps):
            recipe_step -= 1
            await send_message(update, context, 'Это был последний шаг')
        await get_step(update, context, parser.steps[recipe_step], (recipe_number, recipe_step))

    elif choice == 'previous_step':
        await delete_message(update, context, user.message_id)
        recipe_parser = get_parser(context)
        recipe_number, recipe_step = user.recipe_number
        recipe_step -= 1
        parser = ParserForRecipes(recipe_parser.pages[recipe_number].href)
        if recipe_step < 0:
            recipe_step += 1
            await send_message(update, context, 'Это был первый шаг')
        await get_step(update, context, parser.steps[recipe_step], (recipe_number, recipe_step))

    elif choice == 'back':
        await delete_message(update, context, user.message_id)
        parser = get_parser(context)
        recipe_number = user.recipe_number[0]
        await get_recipes(update, context, parser.pages[recipe_number], (recipe_number, 0))

    elif choice == 'add':
        parser = get_parser(context)
        recipe_number = user.recipe_number[0]
        if user.update(parser.pages[recipe_number].href):
            await send_message(update, context, 'Рецепт уже добавлен в избранное')
        else:
            await send_message(update, context, 'Рецепт был добавлен в избранное')
        data_base.save()

    elif choice == 'favourites':
        await delete_message(update, context, user.message_id)
        if len(user.recipes) == 0:
            await get_keyboard(update, context,
                               InlineKeyboard([('назад', 'start')], 1, 1).get_keyboard(),
                               "Рецепты не найдены")
        else:
            parser = ParserForRecipes(user.recipes[0])
            await get_favourites(update, context, parser.steps[0], (0, 0))

    elif choice == 'remove':
        await delete_message(update, context, user.message_id)
        await send_message(update, context, 'Рецепт был удалён из избранного')
        recipe_number = user.recipe_number[0]

        user.remove(recipe_number)
        data_base.save()
        if len(user.recipes) == 0:
            await get_keyboard(update, context,
                               InlineKeyboard([('назад', 'start')], 1, 1).get_keyboard(),
                               "Рецепты в избранном закончились")
        else:
            recipe_number = user.recipe_number[0] - 1
            parser = ParserForRecipes(user.recipes[recipe_number])
            await get_favourites(update, context, parser.steps[recipe_number], (recipe_number, 0))

    elif choice == 'next_favourites':
        await delete_message(update, context, user.message_id)
        recipe_number = user.recipe_number[0] + 1
        if int(recipe_number) >= len(user.recipes):
            recipe_number = user.recipe_number[0]
            await send_message(update, context, 'Вы уже на последнем рецепте')
        parser = ParserForRecipes(user.recipes[recipe_number])
        await get_favourites(update, context, parser.steps[0], (recipe_number, 0))

    elif choice == 'previous_favourites':
        await delete_message(update, context, user.message_id)
        print(user.recipe_number[0])
        recipe_number = user.recipe_number[0] - 1
        if int(recipe_number) <= -1:
            recipe_number = 0
            await send_message(update, context, 'Вы уже на 1-ом рецепте')
        parser = ParserForRecipes(user.recipes[recipe_number])
        await get_favourites(update, context, parser.steps[0], (recipe_number, 0))

    elif choice == 'open_favourites':
        await delete_message(update, context, user.message_id)
        recipe_number = user.recipe_number[0]
        parser = ParserForRecipes(user.recipes[recipe_number])
        await get_favourites_step(update, context, parser.steps[1], (recipe_number, 1))

    elif choice == 'back_favourites':
        await delete_message(update, context, user.message_id)
        recipe_number = user.recipe_number[0]
        parser = ParserForRecipes(user.recipes[recipe_number])
        await get_favourites(update, context, parser.steps[recipe_number], (recipe_number, 0))

    elif choice == 'next_favourites_step':
        await delete_message(update, context, user.message_id)
        recipe_number, recipe_step = user.recipe_number
        recipe_step += 1
        parser = ParserForRecipes(user.recipes[recipe_number])
        if recipe_step >= len(parser.steps):
            recipe_step -= 1
            await send_message(update, context, 'Это был последний шаг')
        await get_favourites_step(update, context, parser.steps[recipe_step], (recipe_number, recipe_step))

    elif choice == 'previous_favourites_step':
        await delete_message(update, context, user.message_id)
        recipe_number, recipe_step = user.recipe_number
        recipe_step -= 1
        parser = ParserForRecipes(user.recipes[recipe_number])
        if recipe_step < 0:
            recipe_step += 1
            await send_message(update, context, 'Это был первый шаг')
        await get_favourites_step(update, context, parser.steps[recipe_step], (recipe_number, recipe_step))


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
    title_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), get_message)

    # регистрируем обработчик в приложение
    application.add_handler(start_handler)
    application.add_handler(keyboard_handler)
    application.add_handler(button_handler)
    application.add_handler(find_handler)
    application.add_handler(title_handler)
    application.add_handler(error_handler)
    # запускаем приложение

    application.run_polling()
