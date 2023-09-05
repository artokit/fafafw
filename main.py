from aiogram import executor, Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
import keyboard
import asyncio
import db_api
import random
import time
import threading
from concurrent.futures import ProcessPoolExecutor
import telebot
import sender

token = '6523887463:AAFblhgHgPh-JD4QjUB5rgRfYZPpgTHMZjs'
bot_for_send = telebot.TeleBot(token=token)
bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())
sender.set_bot(dp)
sender.init_handlers()
# CHANNEL_ID_POSTBACK = -1001849822929
CHANNEL_ID_POSTBACK = -1001900031175
loop_to_send = asyncio.new_event_loop()
ID_TO_CHECK = {
    
}


def ids_checker():
    while True:
        time.sleep(.5)
        arr_to_del = []
        for i in ID_TO_CHECK:
            if time.time() - ID_TO_CHECK[i][0] > 900:
                try:
                    arr_to_del.append(i)
                    bot_for_send.send_message(i, "Wrong mosbet ID", reply_markup=keyboard.try_again)
                except Exception as e:
                    print(str(e))
        
        for i in arr_to_del:
            del ID_TO_CHECK[i]


def site_id_in_checher(site_id):
    for i in ID_TO_CHECK:
        if ID_TO_CHECK[i][1] == site_id:
            return i
    return False


class EnterPassword(StatesGroup):
    enter_1win_id = State()


@dp.channel_post_handler(lambda message: message.chat.id == CHANNEL_ID_POSTBACK)
async def handler_postback(message: Message):
    data = message.text.split(':')
    if len(data) == 2 or len(data) == 3:
        if data[1] == 'registration':
            db_api.add_register_user(data[0])
            r = site_id_in_checher(data[0])
            if r:
                del ID_TO_CHECK[r]
                await bot.send_message(r, f'ID {data[0]}\nmostbet - Registered successfully ✅.\n'
                                 f'Connection is possible ✅.\nAccount activation is required ⌛️')
                return await bot.send_message(r, 'For activation bot you need make deposit 500 ₹')


        if data[1] == 'fdp':
            user = db_api.get_site_id(int(data[0]))
            deposit = float(data[2]) + user[0][1]
            db_api.set_deposit(int(data[0]), deposit)
            user = db_api.get_user_by_site_id(int(data[0]))
            if user:
                if user[0][3] == 30 and float(data[2]) >= 3.5:
                    db_api.update_user_dep_tries(-1, user[0][0])
                    return await bot.send_message(
                        int(user[0][0]),
                        f'ID {data[0]} mostbet - Deposit successfully ✅.\nOperation in bot is correctly again'
                    )
                if user[0][3] == 30 and float(data[2]) < 3.5:
                    return await bot.send_message(
                        int(user[0][0]),
                        f'ID {data[0]} mostbet - Deposit unsuccessfully ❌. Deposit is too small.\n'
                        f'<b>Minimum 300₹</b>',
                        parse_mode='html'
                    )

                if deposit >= 6:
                    await bot.send_message(
                        int(user[0][0]),
                        f'ID {data[0]} mostbet - Deposit successfully ✅.',
                        parse_mode='html',
                    )
                    await bot.send_message(
                        int(user[0][0]),
                        'The bot will give you the odds at which you should bet Auto Cash Out. You must strictly '
                        'follow the odds given by the bot. If you deviate from the bot\'s strategy, you may lose.\n'
                        'Before you start, click the Help button.',
                        reply_markup=keyboard.instruction
                    )
                else:
                    await bot.send_message(
                        int(user[0][0]),
                        f'ID {data[0]} mostbet - Deposit unsuccessfully ❌. Deposit is too small.\n'
                        f'<b>Minimum 500₹</b>',
                        parse_mode='html'
                    )


@dp.callback_query_handler(lambda call: call.data == 'help')
async def get_help(call: CallbackQuery):
    await call.message.edit_text(
        'The minimum balance to play with the bot is 1000.\n\n'
        'The process of using the bot: \n'
        'The bot gives you the odds you should use in the next round. Just follow the given odds. Don\'t worry if you '
        'lose in a round, just click the "NEXT ROUND" button and continue playing next. '
        'In the end, you will always end up with a win.\n\n'
        'You have to use the Auto Cash Out feature.\n'
        'You can only play for one bet.\n'
        'You can skip rounds\n'
        '⚠️Play only with the Auto Cash Out odds given to you by the bot!  Do NOT change the Auto Cash Out odds! ⚠️\n\n'
        'Good luck😉',
        reply_markup=keyboard.ok_button
    )


@dp.callback_query_handler(lambda call: call.data == 'Ok')
async def ok_answer(call: CallbackQuery):
    await call.message.edit_text(
        'The bot will give you the odds at which you should bet Auto Cash Out. You must strictly follow the odds given'
        ' by the bot. If you deviate from the bot\'s strategy, you may lose.\n'
        'Before you start, click the Help button.',
        reply_markup=keyboard.instruction
    )


@dp.message_handler(commands=['start'], state='*')
async def start(message: Message, state: FSMContext):
    await state.finish()
    db_api.add_user(message.chat.id)
    await message.answer(
        'Welcome to ANIMESH SARKAR HACK BOT. Is bot se aapko AVIATOR game ke upcoming rounds ke liye accurate '
        'coefficients milenge. Please read the instructions below to properly connect to the bot. '
        'https://telegra.ph/HOW-TO-USE-ANIRUDH-HACK-BOT-08-30',
        reply_markup=keyboard.start
    )


@dp.callback_query_handler(lambda call: call.data == 'demo', state='*')
@dp.callback_query_handler(lambda call: call.data == 'win', state='*')
@dp.callback_query_handler(lambda call: call.data == 'lose', state='*')
async def start_demo(call: CallbackQuery, state: FSMContext):
    await state.finish()
    tries = db_api.get_tries(call.message.chat.id)

    if tries < 3:
        db_api.set_tries(tries, call.message.chat.id)
        await call.message.answer(
            f'ID: DEMO MODE, NO NEED TO PLACE BETS. NEED ACTIVATION PLAYER ID.\n'
            f'coef {random.randint(100, 200)/100}',
            reply_markup=keyboard.bet
        )
    else:
        await call.message.answer(
            'DEMONSTRATION COMPLETED ✅. BOT KA ISTEMAAL KARNE KE LIYE APNE ACCOUNT KO AKTIVATE KAREIN. AKTIVATION '
            'KE BAAD, PLAYER ID DIKHEGI AUR AAP APNI ID KO BOT KE SAATH JOD SAKTE HAIN, AGAMI ROUNDS KE LIYE SAHI '
            'COEFFICIENTS PRAPT KARNE KE LIYE.',
            reply_markup=keyboard.demo_end
        )


@dp.callback_query_handler(lambda call: call.data == 'start')
async def inline_start(call: CallbackQuery):
    user = db_api.get_user(call.message.chat.id)
    site_id = user[2]
    dep_tries = user[3]

    #if site_id and dep_tries >= random.randint(15, 20):
    #    db_api.update_user_dep_tries(30, call.message.chat.id)
   #     return await call.message.answer(
     #               "⚠️The <b>CASINO</b> system, noticed suspicious!⚠️\n\n"
     #               "The bot has been <b>UPDATED</b>✅\n\n"
     #               "❗️For the correct operation of the bot, deposit another <b>300 rupees</b> to your balance❗️",
     #               parse_mode='html'
     #           )
    if site_id:
        deposit = db_api.get_site_id(site_id)
        if deposit:
            if deposit[0][1] >= 6:
                return await call.message.answer(
                    f'PLAYER ID: {deposit[0][0]}\n'
                    f'CASHOUT {random.randint(100, 200) / 100} ✅',
                    reply_markup=keyboard.real_bet
                )

    await EnterPassword.enter_1win_id.set()
    await call.message.answer(
        'For activation bot register here and enter account ID✅\n\n'
        '***LINK***: https://2skonkem5mb.com/4Vvs\n\n'
        '***PROMOCODE***: `JUL777`\n\n'
        '`Use promocode` it’s very important for activation bot',
        parse_mode='markdown',
        disable_web_page_preview=True
    )
    await call.message.answer(
        '🆔Enter mostbet ID:'
    )


@dp.message_handler(state=EnterPassword.enter_1win_id)
async def enter_1win_id_by_user(message: Message, state: FSMContext):
    user_id = message.text

    if user_id.isdigit():
        is_register = db_api.get_site_id(user_id)

        if is_register:
            db_api.set_site_id(message.chat.id, user_id)
            await state.finish()
            if is_register[0][1] >= 6:
                return await bot.send_message(
                    message.chat.id,
                    f'ID {is_register[0][0]} mostbet - Deposit successfully ✅.',
                    parse_mode='html',
                    reply_markup=keyboard.demo_end
                )

            await message.answer(f'ID {is_register[0][0]}\nmostbet - Registered successfully ✅.\n'
                                 f'Connection is possible ✅.\nAccount activation is required ⌛️')
            return await message.answer('For activation bot you need make deposit 500 ₹')

    ID_TO_CHECK[message.chat.id] = [time.time(), message.text]
    db_api.set_site_id(message.chat.id, user_id)
    await message.answer('❗️Wait 10-15 minutes ❗️\n⏳Your ID is checked in the database⌛️')
    await state.finish()


@dp.callback_query_handler(lambda call: call.data == 'real_win')
@dp.callback_query_handler(lambda call: call.data == 'real_lose')
async def real_bet(call: CallbackQuery):
    user = db_api.get_user(call.message.chat.id)
    site_id = user[2]
    dep_tries = user[3]

    if site_id and dep_tries == -1:
        deposit = db_api.get_site_id(site_id)
        if deposit:
            if deposit[0][1] >= 6:
                return await call.message.answer(
                    f'PLAYER ID: {deposit[0][0]}\n'
                    f'CASHOUT {random.randint(130, 1000) / 100} ✅',
                    reply_markup=keyboard.real_bet
                )
    # if site_id and dep_tries >= random.randint(15, 20):
        # db_api.update_user_dep_tries(30, call.message.chat.id)
        # return await call.message.answer(
                    # "⚠️The <b>CASINO</b> system, noticed suspicious!⚠️\n\n"
                    # "The bot has been <b>UPDATED</b>✅\n\n"
                    # "❗️For the correct operation of the bot, deposit another <b>300 rupees</b> to your balance❗️",
                    # parse_mode='html'
                # )
    if site_id:
        deposit = db_api.get_site_id(site_id)
        print(dep_tries + 1, call.message.chat.id)
        db_api.update_user_dep_tries(dep_tries + 1, call.message.chat.id)
        await call.message.answer(
            f'PLAYER ID: {deposit[0][0]}\n'
            f'CASHOUT {random.randint(110, 520) / 100} ✅',
            reply_markup=keyboard.real_bet
        )



t = threading.Thread(target=ids_checker)
t.start()
executor.Executor(dp).start_polling()
