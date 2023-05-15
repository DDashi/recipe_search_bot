from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, CallbackQueryHandler

class InlineKeyboard:
    def __init__(self, buttons, row, column):
        self.buttons = buttons # list[(button, call_back)]
        self.row = row
        self.column = column

    def get_keyboard(self):

        keyboard = []
        iterator = 0
        for i in range(self.row):
            line = []
            for j in range(self.column):
                button = self.buttons[iterator][0]
                call_back = self.buttons[iterator][1]
                line.append(InlineKeyboardButton(button, callback_data=call_back))
                iterator += 1
            keyboard.append(line)

        return InlineKeyboardMarkup(keyboard)
