import apiai
import json
from aiogram import executor, types
from add_data_in_tp import add_tp
import asyncio
from misc import dp, bot
from config_settings import DETAIL_TEXT, DF_HELP_UUID, DF_PASS_UUID, DF_PROJECT_ID, DIALOGFLOW_ID, QUESTION_TEXT, ADMINS, PASTE_TEXT, NEPRIVET_TEXT, NOMETA_TEXT, IMPORT_DATA_FAIL

commands = ('!go', '!paste', '!np', '!nm', '!dnm')  # Bot`s commands. If you add a new one then add it here!

@dp.message_handler(content_types=['text'])
async def text_com(message: types.Message):
    username = message.from_user.username
    request = apiai.ApiAI(f'{DIALOGFLOW_ID}').text_request()
    request.lang = 'ru'
    request.session_id = 'xyu'
    request.query = message.text
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    try:
        response = responseJson['result']['fulfillment']['speech']
    except KeyError:
        response = None
    try:
        photo = message.photo.file_size
    except AttributeError:
        photo = 0
    if response and photo == 0:
        tailkey = types.InlineKeyboardMarkup()
        tailkey.add(types.InlineKeyboardButton(text=DETAIL_TEXT,
                                                            url=f"https://neprivet.ru"))
        tailkey.add(types.InlineKeyboardButton(text=DETAIL_TEXT,
                                                        url=f"https://nometa.xyz"))
        await message.reply(
            text=response, 
            reply=message.reply_to_message.message_id, 
            reply_markup=tailkey,
            )
    if message.reply_to_message is not None and message.reply_to_message.from_user.is_bot is not True:  # Check if replied message is replied to a human
        try:
            if str(message.text).startswith(commands):  # Check if user has used any of those commands
                await bot.delete_message(message.chat.id, message.message_id)
        except Exception as DelError:
            print(f"DelError: {DelError}")
        if str(message.text).startswith('!go'):  # Google
            try:  # Checking that query is not empty
                search_query = str(message.text).split('!go ')[1]
            except IndexError:
                search_query = 'Как правильно задавать вопросы на сообществе'

            search_key = types.InlineKeyboardMarkup()
            search_key.add(types.InlineKeyboardButton(text=DETAIL_TEXT,
                                                                url=f"http://google.com/search?q={search_query}"))

            await bot.send_message(
                chat_id=message.chat.id,
                text=QUESTION_TEXT,
                reply_markup=search_key,
                reply_to_message_id=message.reply_to_message.message_id,
                disable_web_page_preview=True
            )

        elif str(message.text).startswith('!paste'):  # Pastebin
            await bot.send_message(
                chat_id=message.chat.id,
                text=PASTE_TEXT,
                reply_to_message_id=message.reply_to_message.message_id,
                disable_web_page_preview=True
            )
        elif str(message.text).startswith('!nm'):  # nometa.xyz
            if username in ADMINS:  # Bot checks if user is in admins so randoms can't use this a lot
                data2input = message.reply_to_message.text
                try:
                    add_tp(DF_HELP_UUID, DF_PROJECT_ID, message=f'{data2input}')
                except Exception:
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text=IMPORT_DATA_FAIL,
                        reply_to_message_id=message.reply_to_message.message_id
                    )
                nometa_key = types.InlineKeyboardMarkup()
                nometa_key.add(types.InlineKeyboardButton(text=DETAIL_TEXT, url="http://nometa.xyz"))
                await bot.send_message(
                        chat_id=message.chat.id,
                        text=NOMETA_TEXT,
                        reply_markup=nometa_key,
                        reply_to_message_id=message.reply_to_message.message_id
                )
            else:
                await message.reply(
                    reply=False,
                    text=f'@{username}, пожалуйста, если Вы считаете, что это мета-вопрос или просто "Привет", оповестите об этом администрацию. Спасибо!',
                    )

        elif str(message.text).startswith('!np'):  # neprivet.ru
            if username in ADMINS:  # Bot checks if user is in admins so randoms can't use this a lot
                data2input = message.reply_to_message.text
                try:
                    add_tp(DF_HELP_UUID, DF_PROJECT_ID, message=f'{data2input}')
                except Exception:
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text=IMPORT_DATA_FAIL,
                        reply_to_message_id=message.reply_to_message.message_id
                    )
                nometa_key = types.InlineKeyboardMarkup()
                nometa_key.add(types.InlineKeyboardButton(text=DETAIL_TEXT, url="http://neprivet.ru"))
                await bot.send_message(
                        chat_id=message.chat.id,
                        text=NEPRIVET_TEXT,
                        reply_markup=nometa_key,
                        reply_to_message_id=message.reply_to_message.message_id
                )
            else:
                await message.reply(
                    text=f'@{username}, пожалуйста, если Вы считаете, что это мета-вопрос или просто "Привет", оповестите об этом администрацию. Спасибо!',
                    reply=False
                )
        elif str(message.text).startswith('!dnm'):  # if that's not a meta-question
            if username in ADMINS:  # Bot checks if user is in admins so randoms can't use this a lot
                data2input = message.reply_to_message.text
                try:
                    add_tp(DF_PASS_UUID, DF_PROJECT_ID, message=f'{data2input}')
                except Exception:
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text=IMPORT_DATA_FAIL,
                        reply_to_message_id=message.reply_to_message.message_id
                    )
                await bot.send_message(
                    chat_id=message.chat.id,
                    text='Ошибся, извините =)',
                    reply_to_message_id=message.reply_to_message.message_id,
                )
            else:
                await message.reply(
                    text=f'@{username}, пожалуйста, если Вы считаете, что это не мета-вопрос и не просто "Привет", оповестите об этом администрацию. Спасибо!',
                    reply=False
                )
