import aiogram.types as types
from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove



#Write your token
TOKEN ="WRITE_TOKEN_HERE"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# A greeting text message after the bot starts
@dp.message_handler(Command('start'))
async def cmd_start(message: types.Message):
    # Send a welcome message and a list of beverages
    await message.reply("Hi there! Please choose something from our list of beverages", reply_markup=get_beverages_keyboard())


# Message after selection 
@dp.message_handler(lambda message: message.text in ['Tea', 'Coffee', 'Beer', 'Pepsi', 'Cola'])
async def process_beverage(message: types.Message):
    # Send a confirmation message 
    await message.reply(f"You chose {message.text}! Enjoy!", reply_markup=get_confirmation_keyboard())


# Different answer choices
@dp.message_handler()
async def clientn(message: types.Message):
    if message.text == 'No, thanks.':       
        await message.reply("Then... Please choose something else :", reply_markup=get_beverages_keyboard())

    elif message.text == 'Yes, please!':       
        await message.reply("Enjoy it!, Can I suggest something else? ", reply_markup=get_beverages_keyboard())

    else:
        await message.reply("Sorry, I don't understand you. I'm just a bot offering drinks😀. ")


# Function that creates a custom keyboard
def get_beverages_keyboard():
    beverages = ['Tea', 'Coffee', 'Beer', 'Pepsi', 'Cola']
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(*beverages)
    return markup


# Confirmation button
def get_confirmation_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton('Yes, please!'))
    markup.add(KeyboardButton('No, thanks.'))
    return markup


# Start the bot
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp)
