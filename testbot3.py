import logging
import re
import aiogram.utils.markdown as md
import aiogram.utils.exceptions as exc
import aiogram.types as types
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage



# Initialize bot and dispatcher
TOKEN = 'WRITE_TOKEN_HERE'
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Define states for FSM
class RegistrationForm(StatesGroup):
    name = State()  # User's name
    age = State()  # User's age
    phone = State()  # User's phone number
    email = State()  # User's email address


# Define a command handler to start the registration process
@dp.message_handler(Command('register'))
async def register(message: types.Message):
    # Ask for the user's name
    await message.answer("What's your name?")
    # Set the state to 'name'
    await RegistrationForm.name.set()

# Define a message handler for each state
@dp.message_handler(state=RegistrationForm.name)
async def process_name(message: types.Message, state: FSMContext):
    # Get the user's name from the message text
    name = message.text.strip()
    # Validate the name (only letters and spaces)
    if not re.match("^[A-Za-z ]+$", name):
        # If the name is invalid, send an error message and stay in the same state
        await message.answer("Please enter a valid name (only letters and spaces).")
        return
    # Store the name in the state and ask for the user's age
    await state.update_data(name=name)
    await message.answer("How old are you?")
    # Set the state to 'age'
    await RegistrationForm.age.set()

@dp.message_handler(state=RegistrationForm.age)
async def process_age(message: types.Message, state: FSMContext):
    # Get the user's age from the message text
    age = message.text.strip()
    # Validate the age (only digits)
    if not age.isdigit():
        # If the age is invalid, send an error message and stay in the same state
        await message.answer("Please enter a valid age (only digits).")
        return
    # Store the age in the state and ask for the user's phone number
    await state.update_data(age=age)
    await message.answer("What's your phone number?")
    # Set the state to 'phone'
    await RegistrationForm.phone.set()

@dp.message_handler(state=RegistrationForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    # Get the user's phone number from the message text
    phone = message.text.strip()
    # Validate the phone number (10 digits)
    if not re.match("^[0-9]{10}$", phone):
        # If the phone number is invalid, send an error message and stay in the same state
        await message.answer("Please enter a valid phone number (10 digits).")
        return
    # Store the phone number in the state and ask for the user's email address
    await state.update_data(phone=phone)
    await message.answer("What's your email address?")
    # Set the state to 'email'
    await RegistrationForm.email.set()

@dp.message_handler(state=RegistrationForm.email)
async def process_email(message: types.Message, state: FSMContext):
    # Get the user's email address from the message text
    email = message.text.strip()
    # Validate the email address (simple email regex)
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        # If the email address is invalid, send an error message and stay in the same state
        await message.answer("Please enter a valid email address.")
        return
    # Store the email address in the state
    data = await state.get_data()
    name = data.get('name')
    age = data.get('age')
    phone = data.get('phone')
    await state.finish()
    # Send a summary message with the collected user data
    await message.answer(
        md.text(
            md.bold('Registration summary:'),
            md.text('Name:', name),
            md.text('Age:', age),
            md.text('Phone:', phone),
            md.text('Email:', email),
            sep='\n',
        ),
        parse_mode=ParseMode.MARKDOWN,
    )

# Start the bot
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp)
