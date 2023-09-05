from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot import types

start = InlineKeyboardMarkup()
start.add(
    InlineKeyboardButton('START', callback_data='start'),
    InlineKeyboardButton('DEMO BOT', callback_data='demo')
)

bet = InlineKeyboardMarkup()
bet.add(
    InlineKeyboardButton('WIN', callback_data='win'),
    InlineKeyboardButton('LOSE', callback_data='lose')
)

demo_end = InlineKeyboardMarkup()
demo_end.add(InlineKeyboardButton('START', callback_data='start'))

real_bet = InlineKeyboardMarkup()
real_bet.add(
    InlineKeyboardButton('🚀NEW ROUND🚀', callback_data='real_win'),
)

instruction = InlineKeyboardMarkup()
instruction.add(InlineKeyboardButton('❓Help❓', callback_data='help'))
instruction.add(InlineKeyboardButton('Start', callback_data='start'))

ok_button = InlineKeyboardMarkup()
ok_button.add(InlineKeyboardButton('Ok', callback_data='Ok'))

try_again = types.InlineKeyboardMarkup()
try_again.add(types.InlineKeyboardButton("Try again", callback_data='start'))
