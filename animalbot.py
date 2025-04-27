import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from api_token import TOKEN


bot = Bot(TOKEN)
dp = Dispatcher()

TEXT = '''
/help - справочный текст
/start - запуск бота
'''

@dp.message(Command('start'))
async def start_command(message: types.Message):
    kb = [
        [KeyboardButton(text='Милый')],
        [KeyboardButton(text='Вредный')]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, is_persistent=True, resize_keyboard=True)
    await message.answer('Твое тотемное животное - сладкий котик', reply_markup=keyboard)


@dp.message(Command('help'))
async def help_command(message: types.Message):
    await message.reply(TEXT)


@dp.message(F.text.lower() == 'милый')
async def cute(message: types.Message):
    await message.answer_sticker('CAACAgQAAxkBAAEOQtpn9TwXOyl5ROOdwSdlORr4Y55gTwACqhMAAuu3kFHxeXU1k4WV8jYE')


@dp.message(F.text.lower() == 'вредный')
async def bad(message: types.Message):
    await message.answer_sticker('CAACAgQAAxkBAAEOQtxn9TxiTJvATuzNZzic2Y0ShrKHvQACGRMAAhmZoVHmPlnf5mOkRTYE')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
