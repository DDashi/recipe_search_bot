import logging
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler
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


if __name__ == '__main__':
    TOKEN = os.environ["TOKEN"]
    # создание экземпляра бота через `ApplicationBuilder`
    application = ApplicationBuilder().token(TOKEN).build()


    # создаем обработчик
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    # регистрируем обработчик в приложение
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    # запускаем приложение
    application.run_polling()
