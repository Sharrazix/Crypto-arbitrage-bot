import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text



#Write your token
TOKEN ="WRITE_TOKEN_HERE"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def echo(message: types.Message):
#Getting the username 
    name = message.from_user.first_name
#Sending a message with the user's name
    await message.reply(f"Hello, your name is {name}")

# Start the bot
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp)
