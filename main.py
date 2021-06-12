# -*- coding: utf-8 -*-
#
#  BochkaBot - Main script
#  Created by LulzLoL231 at 12/6/21
#
from os import environ
from asyncio import get_event_loop
from logging import basicConfig, INFO, getLogger

from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram.utils.executor import start_polling


cmds = [
    BotCommand('start', 'Start'),
    BotCommand('help', 'How make a Bochka?')
]
basicConfig(
    format='[%(levelname)s] %(name)s (%(lineno)d) >> %(message)s',
    level=INFO
)
log = getLogger('BochkaBot')
log.info('Telegram Bot BochkaBot v0.0.2')
loop = get_event_loop()
bot = Dispatcher(Bot(environ.get('TGBOT_TOKEN', ''), loop), loop)
loop.run_until_complete(bot.bot.set_my_commands(cmds))


@bot.message_handler(commands=['start'])
async def start(msg: types.Message):
    log.info(f'"start": Called by {msg.chat.mention} ({str(msg.chat.id)})')
    cnt = 'Как сделать бочку?'
    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton(
        text='УЗНАТЬ',
        callback_data='bochka'
    ))
    await msg.answer(cnt, reply_markup=key)


@bot.callback_query_handler(lambda q: q.data == 'bochka')
async def query_bochka(query: types.CallbackQuery):
    await query.answer()
    await query.message.delete()
    await bochka(query.message)


@bot.message_handler(commands=['bochka', 'help'])
async def bochka(msg: types.Message):
    log.info(f'"bochka": Called by {msg.chat.mention} ({str(msg.chat.id)})')
    await msg.answer_chat_action(types.ChatActions.UPLOAD_PHOTO)
    cnt = 'Бочку сделать очень просто!'
    media = types.MediaGroup()
    media.attach_photo(types.InputFile('bochka.jpg'), caption=cnt)
    await msg.answer_media_group(media)


if __name__ == '__main__':
    start_polling(bot)
