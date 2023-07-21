import ssl
import time
import hashlib
import hmac
import base64
import logging
import aiogram.utils.exceptions
import aiohttp
import asyncio
import datetime as dt
from random import choice
import aiohttp_socks
from fake_useragent import UserAgent
from aiohttp_socks import ProxyConnector
from aiogram import Bot, Dispatcher, executor, types, utils


logging.basicConfig(level=logging.INFO, filename="tgbot_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


# proxy_list = [
#     'socks5://z0FU9G:LTSXrt@46.3.138.169:8000',
#     'socks5://z0FU9G:LTSXrt@46.3.137.28:8000',
#     'socks5://NPmnKq:tLNh4y@168.80.202.228:8000',
#     'socks5://NPmnKq:tLNh4y@168.80.200.54:8000',
#     'socks5://NPmnKq:tLNh4y@168.80.203.52:8000'
# ]

headers = {
    'user-agent': UserAgent().random
}

# Type your token here
bot = Bot(token='YOUR_TOKEN')
dp = Dispatcher(bot)

crypto_settings = {
    'admin':
        {
            'interval': 15,
            'percent': 0,
            'volume': 10000,
            'order': 10,
            'run': False
        }
}

admins_list = [
      'YOUR_ID',
]

chat_id = '-1001692516543'
history = list()
run_status = str()


black_list = ['QUACKUSDT', 'REDUSDT', 'BABYDOGEUSDT', 'REVOUSDT',]

#functions that starts everything in 2 languages
async def run_cryptoEN():
    while crypto_settings.get("admin")["run"]:
        try:
            await comparison_allEN()
            await asyncio.sleep(crypto_settings.get("admin")["interval"] * 60)
        except:
            pass

async def run_cryptoRU():
    while crypto_settings.get("admin")["run"]:
        try:
            await comparison_allRU()
            await asyncio.sleep(crypto_settings.get("admin")["interval"] * 60)
        except:
            pass

@dp.message_handler(commands='start')
async def start(message: types.Message):
    if str(message.from_user.id) in admins_list and str(message.chat.id) not in chat_id:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,)
        btn1 = types.KeyboardButton('Start')
        btn2 = types.KeyboardButton('Stop')
        btn3 = types.KeyboardButton('Minimal daily volume')
        btn4 = types.KeyboardButton('Minimal order amount')
        btn5 = types.KeyboardButton('Percentage price difference')
        btn6 = types.KeyboardButton('Interval')
        btn7 = types.KeyboardButton('Blacklist')
        btn8 = types.KeyboardButton('list of exchanges')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
        await bot.send_message(message.from_user.id, text='Hello, {0.first_name}! 👋🏻'.format(message.from_user),
                                reply_markup=markup)
        await bot.send_message(message.from_user.id, text=f'Standard characteristics that you can change: 👇🏻\n'
                           f'🔸 Autostart interval: {crypto_settings.get("admin")["interval"]} minutes ⏰\n'
                           f'🔸 Percentage price difference: {crypto_settings.get("admin")["percent"]} %\n'
                           f'🔸 Minimal daily volume: {crypto_settings.get("admin")["volume"]} $\n'
                           f'🔸 Minimal order amount: {crypto_settings.get("admin")["order"]} $')

@dp.message_handler(commands='faq')
async def faq(message: types.Message):
    if str(message.from_user.id) in admins_list and str(message.chat.id) not in chat_id:
        await bot.send_message(message.from_user.id, text="The '/start' command in the menu is designed to start the Telegram bot.\n\nThe 'Start' button automatically starts a search on exchanges with an interval as long as it is active. Subsequent clicks will not change anything.\n\nThe 'Stop' button stops the automatic search, but only when the bot is not in an active search cycle. This is a protection against launching multiple cycles in a row. You need to wait for the cycle to finish and then press the button again to stop it.\n\nThe bot will respond to the command by duplicating it, signaling that the button has been pressed. If the cycle is active, the button can be pressed, but there will be no response messages or actions. In other words, once the cycle is started, you need to wait for it to finish and then stop it before starting again.")

@dp.message_handler(content_types='text')
async def func(message: types.Message):
    if str(message.from_user.id) in admins_list and str(message.chat.id) not in chat_id:
        global run_status
        if message.text == 'Start':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Russian')
            btn2 = types.KeyboardButton('English')
            btn3 = types.KeyboardButton('Main menu')
            markup.add(btn1, btn2, btn3)
            await bot.send_message(message.from_user.id,
                                text=f'Choose language', reply_markup=markup)
        elif message.text == 'Russian':
            if not crypto_settings.get("admin")["run"] and run_status == '':
                await bot.send_message(message.from_user.id, text='Autostart in Russian is running')
                crypto_settings.get("admin")["run"] = True
                run_status = 'started'
                await run_cryptoRU()

        elif message.text == 'English':
            if not crypto_settings.get("admin")["run"] and run_status == '':
                await bot.send_message(message.from_user.id, text='Autostart in English is running')
                crypto_settings.get("admin")["run"] = True
                run_status = 'started'
                await run_cryptoEN()

        elif message.text == 'Stop':
            if run_status == 'ended':
                await bot.send_message(message.from_user.id, text='Autostart stopped')
                crypto_settings.get("admin")["run"] = False
                run_status = str()

        elif message.text == 'Percentage price difference':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Change percentage')
            btn2 = types.KeyboardButton('Main menu')
            markup.add(btn1, btn2)
            await bot.send_message(message.from_user.id,
                                text=f'Percentage: {crypto_settings.get("admin")["percent"]} %', reply_markup=markup)

        elif message.text == 'Change percentage':
            history.append(message.text)
            markup = types.ReplyKeyboardRemove()
            await bot.send_message(message.from_user.id, text='Set the percentage', reply_markup=markup)


        elif message.text == 'Minimal daily volume':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Change volume')
            btn2 = types.KeyboardButton('Main menu')
            markup.add(btn1, btn2)
            await bot.send_message(message.from_user.id,
                                   text=f'Volume: {crypto_settings.get("admin")["volume"]} $', reply_markup=markup)

        elif message.text == 'Change volume':
            history.append(message.text)
            markup = types.ReplyKeyboardRemove()
            await bot.send_message(message.from_user.id, text='Set the volume', reply_markup=markup)


        elif message.text == 'Minimal order amount':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Change amount')
            btn2 = types.KeyboardButton('Main menu')
            markup.add(btn1, btn2)
            await bot.send_message(message.from_user.id,
                                    text=f'Amount: {crypto_settings.get("admin")["order"]} $', reply_markup=markup)

        elif message.text == 'Change amount':
            history.append(message.text)
            markup = types.ReplyKeyboardRemove()
            await bot.send_message(message.from_user.id, text='Set the amount', reply_markup=markup)

        elif message.text == 'Interval':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Change interval')
            btn2 = types.KeyboardButton('Main menu')
            markup.add(btn1, btn2)
            await bot.send_message(message.from_user.id,
                                    text=f'Now interval: {crypto_settings.get("admin")["interval"]} minutes', reply_markup=markup)
        elif message.text == 'Change interval':
            history.append(message.text)
            markup = types.ReplyKeyboardRemove()
            await bot.send_message(message.from_user.id, text='Set interval', reply_markup=markup)


        elif message.text == 'Add to blacklist':
            history.append(message.text)
            markup = types.ReplyKeyboardRemove()
            await bot.send_message(message.from_user.id, text='Write a coin to be added to the blacklist', reply_markup=markup)

        elif message.text == 'list of exchanges':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Main menu')
            markup.add(btn1)
            await bot.send_message(message.from_user.id,
                                   text=f'Binance\nHuobi\nBybit\nKucoin\nGateio\nMexc\nOkx\nWhitebit\nPoloniex\nBitget',
                                   reply_markup=markup)

        elif (message.text).isdigit():
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Main menu')
            markup.add(btn1)
            if 'Change percentage' in history:
                crypto_settings.get("admin")["percent"] = int(message.text)
                await bot.send_message(message.from_user.id, text=f'New percentage: {message.text} %',
                                       reply_markup=markup)
            elif 'Change volume' in history:
                crypto_settings.get("admin")["volume"] = int(message.text)
                await bot.send_message(message.from_user.id, text=f'New volume: {message.text} $', reply_markup=markup)
            elif 'Change amount' in history:
                crypto_settings.get("admin")["order"] = int(message.text)
                await bot.send_message(message.from_user.id, text=f'New amount: {message.text} $', reply_markup=markup)
            elif 'Change interval' in history:
                crypto_settings.get("admin")["interval"] = int(message.text)
                await bot.send_message(message.from_user.id, text=f'New interval: {message.text} minutes', reply_markup=markup)
            else:
                await bot.send_message(message.from_user.id, text='Unnknown command')

        elif 'Add to blacklist' in history:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Main menu')
            markup.add(btn1)
            black_list.append(message.text)
            await bot.send_message(message.from_user.id, text=f'Coin {message.text} has been added', reply_markup=markup)
            history.clear()

        elif message.text == 'Blacklist':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Add to blacklist')
            btn2 = types.KeyboardButton('Main menu')
            markup.add(btn1, btn2)
            await bot.send_message(message.from_user.id,
                                text=f'Now in blacklist: {black_list}', reply_markup=markup)

        elif(message.text) == 'Main menu':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, )
            btn1 = types.KeyboardButton('Start')
            btn2 = types.KeyboardButton('Stop')
            btn3 = types.KeyboardButton('Minimal daily volume')
            btn4 = types.KeyboardButton('Minimal order amount')
            btn5 = types.KeyboardButton('Percentage price difference')
            btn6 = types.KeyboardButton('Interval')
            btn7 = types.KeyboardButton('Blacklist')
            btn8 = types.KeyboardButton('list of exchanges')
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
            history.clear()
            await bot.send_message(message.from_user.id, text='You are back in the main menu', reply_markup=markup)

        else:
            await bot.send_message(message.from_user.id, text='Unnknown command')

########################################################################################################################

async def binance():
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get('https://api.binance.com/api/v3/ticker/24hr', headers=headers) as response:
    #             response = await response.json()
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.binance.com/api/v3/ticker/24hr', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        return None

    try:
        binance_price = dict()
        for crypto in response:
            if crypto.get('bidPrice') not in ("", None) and crypto.get('askPrice') not in ("", None):
                if float(crypto.get('bidPrice')) > 0 and float(crypto.get('askPrice')) > 0:
                    if crypto.get('symbol')[-4:] == 'USDT':
                        if float(crypto.get('quoteVolume')) > crypto_settings.get("admin")["volume"]:
                            binance_price.update({crypto.get('symbol').upper():
                                                      [float(crypto.get('bidPrice')) * 0.999,
                                                       float(crypto.get('askPrice')) * 1.001]})
        return binance_price
    except (AttributeError, TypeError):
        print("Закончил бинанс")
        return None

async def huobi():
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get('https://api.huobi.pro/market/tickers', headers=headers) as response:
    #             response = await response.json()
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.huobi.pro/market/tickers', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        return None

    try:
        huobi_price = dict()
        for crypto in response['data']:
            if crypto.get('bid') not in ("", None) and crypto.get('ask') not in ("", None):
                if float(crypto.get('bid')) > 0 and float(crypto.get('ask')) > 0:
                    if crypto.get('symbol')[-4:] == 'usdt':
                        if float(crypto.get('vol')) > crypto_settings.get("admin")["volume"]:
                            huobi_price.update({crypto.get('symbol').upper():
                                        [float(crypto.get('bid')) * 0.998, float(crypto.get('ask')) * 1.002]})
        return huobi_price
    except (AttributeError, TypeError):
        print("Закончил хуоби")
        return None

async def bybit():
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get('https://api.bybit.com/spot/quote/v1/ticker/24hr', headers=headers) as response:
    #             response = await response.json()
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.bybit.com/spot/quote/v1/ticker/24hr', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        return None

    try:
        bybit_price = dict()
        for crypto in response['result']:
            if crypto.get('bestBidPrice') not in ("", None) and crypto.get('bestAskPrice') not in ("", None):
                if float(crypto.get('bestBidPrice')) > 0 and float(crypto.get('bestAskPrice')) > 0:
                    if crypto.get('symbol')[-4:] == 'USDT':
                        if float(crypto.get('quoteVolume')) > crypto_settings.get("admin")["volume"]:
                            bybit_price.update({crypto.get('symbol').upper():
                                [float(crypto.get('bestBidPrice')) * 0.999, float(crypto.get('bestAskPrice')) * 1.001]})
        return bybit_price
    except (AttributeError, TypeError):
        print("Закончил байбит")
        return None

async def kucoin():
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get('https://api.kucoin.com/api/v1/market/allTickers', headers=headers) as response:
    #             response = await response.json()
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.kucoin.com/api/v1/market/allTickers', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        return None

    try:
        kucoin_price = dict()
        for crypto in response['data']['ticker']:
            if '3' not in crypto.get('symbol') and '5' not in crypto.get('symbol'):
                if crypto.get('buy') not in ("", None) and crypto.get('sell') not in ("", None):
                    if float(crypto.get('buy')) > 0 and float(crypto.get('sell')) > 0:
                        if crypto.get('symbol')[-4:] == 'USDT':
                            if float(crypto.get('volValue')) > crypto_settings.get("admin")["volume"]:
                                kucoin_price.update({crypto.get('symbol').upper().replace('-', ''):
                                             [float(crypto.get('buy')) * 0.999, float(crypto.get('sell')) * 1.001]})
        return kucoin_price
    except (AttributeError, TypeError):
        print("Закончил кукоин")
        return None

async def gateio():
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get('https://api.gateio.ws/api/v4/spot/tickers', headers=headers) as response:
    #             response = await response.json()
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.gateio.ws/api/v4/spot/tickers', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        return None

    try:
        gateio_price = dict()
        for crypto in response:
            if '3' not in crypto.get('currency_pair') and '5' not in crypto.get('currency_pair'):
                if crypto.get('highest_bid') not in ("", None) and crypto.get('lowest_ask') not in ("", None):
                    if float(crypto.get('highest_bid')) > 0 and float(crypto.get('lowest_ask')) > 0:
                        if crypto.get('currency_pair')[-4:] == 'USDT':
                            if float(crypto.get('quote_volume')) > crypto_settings.get("admin")["volume"]:
                                gateio_price.update({crypto.get('currency_pair').upper().replace('_', ''):
                                   [float(crypto.get('highest_bid')) * 0.998, float(crypto.get('lowest_ask')) * 1.002]})
        return gateio_price
    except (AttributeError, TypeError):
        print("Закончил гейтио")
        return None

async def mexc():
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get('https://api.mexc.com/api/v3/ticker/24hr', headers=headers) as response:
    #             response = await response.json()
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.mexc.com/api/v3/ticker/24hr', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        return None

    try:
        mexc_price = dict()
        for crypto in response:
            if '3' not in crypto.get('symbol') and '5' not in crypto.get('symbol'):
                if crypto.get('bidPrice') not in ("", None) and crypto.get('askPrice') not in ("", None):
                    if float(crypto.get('bidPrice')) > 0 and float(crypto.get('askPrice')) > 0:
                        if crypto.get('symbol')[-4:] == 'USDT':
                            if float(crypto.get('quoteVolume')) > crypto_settings.get("admin")["volume"]:
                                mexc_price.update({crypto.get('symbol'):
                                        [float(crypto.get('bidPrice')) * 0.998, float(crypto.get('askPrice')) * 1.002]})
        return mexc_price
    except (AttributeError, TypeError):
        print("Закончил мехц")
        return None

async def okx():
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get('https://www.okx.com/api/v5/market/tickers?instType=SPOT', headers=headers) \
    #                 as response:
    #             response = await response.json()
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.okx.com/api/v5/market/tickers?instType=SPOT', headers=headers) \
                    as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        return None

    try:
        okx_price = dict()
        for crypto in response['data']:
            if crypto.get('bidPx') not in ("", None) and crypto.get('askPx') not in ("", None):
                if float(crypto.get('bidPx')) > 0 and float(crypto.get('askPx')) > 0:
                    if crypto.get('instId')[-4:] == 'USDT':
                        if float(crypto.get('volCcy24h')) > crypto_settings.get("admin")["volume"]:
                            okx_price.update({crypto.get('instId').upper().replace('-', ''):
                                      [float(crypto.get('bidPx')) * 0.999, float(crypto.get('askPx')) * 1.001]})
        return okx_price
    except (AttributeError, TypeError):
        print("Закончил окх")
        return None

async def whitebit():
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get('https://whitebit.com/api/v2/public/ticker', headers=headers) as response:
    #             response = await response.json()
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://whitebit.com/api/v2/public/ticker', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        return None

    try:
        whitebit_price = dict()
        for crypto in response['result']:
            if crypto.get('highestBid') not in ("", None) and crypto.get('lowestAsk') not in ("", None):
                if float(crypto.get('highestBid')) > 0 and float(crypto.get('lowestAsk')) > 0:
                    if crypto.get('tradingPairs')[-4:] == 'USDT':
                        if float(crypto.get('quoteVolume24h')) > crypto_settings.get("admin")["volume"]:
                            whitebit_price.update({crypto.get('tradingPairs').replace('_', ''):
                                [float(crypto.get('highestBid')) * 0.999, float(crypto.get('lowestAsk')) * 1.001]})
        return whitebit_price
    except (AttributeError, TypeError):
        print("Закончил вайтбит")
        return None

async def poloniex():
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get('https://poloniex.com/public?command=returnTicker', headers=headers) as response:
    #             response = await response.json()
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://poloniex.com/public?command=returnTicker', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        return None

    try:
        poloniex_price = dict()
        for crypto in response:
            if response.get(crypto)['highestBid'] not in ("", None) \
                    and response.get(crypto)['lowestAsk'] not in ("", None):
                if float(response.get(crypto)['highestBid']) > 0 and float(response.get(crypto)['lowestAsk']) > 0:
                    if crypto[:4] == 'USDT':
                        if float(response.get(crypto)['baseVolume']) > crypto_settings.get("admin")["volume"]:
                            poloniex_price.update({crypto[5:] + crypto[:4]:
                                                       [float(response.get(crypto)['highestBid']) * 0.9985,
                                                        float(response.get(crypto)['lowestAsk']) * 1.0015]})
        return poloniex_price
    except (AttributeError, TypeError):
        print("Закончил полонех")
        return None

async def bitget():
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get('https://api.bitget.com/api/spot/v1/market/tickers', headers=headers) \
    #                 as response:
    #             response = await response.json()
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.bitget.com/api/spot/v1/market/tickers', headers=headers) \
                    as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        return None

    try:
        bitget_price = dict()
        for crypto in response['data']:
            if crypto.get('buyOne') not in ("", None) and crypto.get('sellOne') not in ("", None):
                if float(crypto.get('buyOne')) > 0 and float(crypto.get('sellOne')) > 0:
                    if crypto.get('symbol')[-4:] == 'USDT':
                        if float(crypto.get('quoteVol')) > crypto_settings.get("admin")["volume"]:
                            bitget_price.update({crypto.get('symbol'):
                                      [float(crypto.get('buyOne')) * 0.999, float(crypto.get('sellOne')) * 1.001]})
        return bitget_price
    except (AttributeError, TypeError):
        print("Закончил битджет")
        return None

cex_func = {
    'binance': binance,
    'huobi': huobi,
    'bybit': bybit,
    'kucoin': kucoin,
    'gateio': gateio,
    'mexc': mexc,
    'okx': okx,
    'whitebit': whitebit,
    'poloniex': poloniex,
    'bitget': bitget
    }

async def binance_chain():
    KEY = "jJDSZcCeEHv57DGoje9rtxvJtAct39U6swkfDN3mSSwouN6exUx7FoPlIbWI76So"
    SECRET = "99F56iCmjHRH6aLeKCmKmIsdU8TS51fg8zldYoqO1p38JfBnArpO4qLifsSMPQ5m"
    BASE_URL = "https://api.binance.com"

    query_string = "timestamp={}".format(int(time.time() * 1000))
    url = (BASE_URL + '/sapi/v1/capital/config/getall' + "?" + query_string + "&signature=" +
            hmac.new(SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest())

    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         session.headers.update({"Content-Type": "application/json;charset=utf-8", "X-MBX-APIKEY": KEY})
    #         async with session.get(url, headers=headers) as response:
    #             response = await response.json()
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            session.headers.update({"Content-Type": "application/json;charset=utf-8", "X-MBX-APIKEY": KEY})
            async with session.get(url, headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        print("Закончил бинанс 2")
        return None

    chain_rename = {
        'BSC': 'BEP20',
        'BNB': 'BEP2',
        'ETH': 'ERC20',
        'TRX': 'TRC20',
        'APT': 'APTOS'
    }

    try:
        binance_status = dict()
        for value in response:
            binance_status.update({value.get('coin'): {}})
            for value_ in value.get('networkList'):
                if value_.get('network') in chain_rename:
                    chain = chain_rename[value_.get('network')]
                else:
                    chain = value_.get('network')
                binance_status[value.get('coin')].update({chain:
                         [value_.get('depositEnable'), value_.get('withdrawEnable'), float(value_.get('withdrawFee'))]})
        return binance_status
    except (AttributeError, TypeError, KeyError):
        print("Закончил бинанс 3")
        return None

async def huobi_chain():
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get('https://api.huobi.pro/v2/reference/currencies', headers=headers) as response:
    #             response = await response.json()
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.huobi.pro/v2/reference/currencies', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        print("Закончил хуоби 2")
        return None

    chain_rename = {
        'AVAXCCHAIN': 'AVAXC',
        'ARBITRUMONE': 'ARBITRUM',
        'OP': 'OPTIMISM',
        'ATOM1': 'ATOM',
        'C-CHAIN': 'AVAXC',
        'CCHAIN': 'AVAXC',
        'APT': 'APTOS',
        'MOONBEAM': 'GLMR',
        'WAX1': 'WAX'
    }

    try:
        huobi_status = dict()
        for value in response['data']:
            huobi_status.update({value.get('currency').upper(): {}})
            for value_ in value.get('chains'):
                if value_.get('transactFeeWithdraw') not in ('', None):
                    if value_.get('displayName') in chain_rename:
                        chain = chain_rename[value_.get('displayName')]
                    else:
                        chain = value_.get('displayName')
                    if value_.get('depositStatus') == 'allowed':
                        deposit = True
                    else:
                        deposit = False
                    if value_.get('withdrawStatus') == 'allowed':
                        withdrawal = True
                    else:
                        withdrawal = False
                    huobi_status[value.get('currency').upper()].update({chain: [deposit, withdrawal,
                                                                            float(value_.get('transactFeeWithdraw'))]})
        return huobi_status
    except (AttributeError, TypeError, KeyError):
        print("Закончил хуоби 3")
        return None

async def bybit_chain():
    api_key = 'a6C644LXqUtcQiCdJN'
    secret_key = 'I80WRDINApk9Bwah4wrwcUWta4TmEP7AbjTg'

    recv_window = str(5000)
    time_stamp = str(int(time.time() * 10 ** 3))
    param_str = str(time_stamp) + api_key + recv_window
    hash = hmac.new(bytes(secret_key, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
    signature = hash.hexdigest()
    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-SIGN': signature,
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-TIMESTAMP': time_stamp,
        'X-BAPI-RECV-WINDOW': recv_window,
        'Content-Type': 'application/json'
    }
    url = ("https://api.bybit.com" + "/asset/v3/private/coin-info/query")

    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get(url, headers=headers) as response:
    #             response = await response.json()
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        print("Закончил байбит 2")
        return None

    chain_rename = {
        'BSC (BEP20)': 'BEP20',
        'Bitcoin Cash': 'BCH',
        'Arbitrum One': 'ARBITRUM',
        'Dogecoin': 'DOGE',
        'Waves': 'WAVES',
        'Terra Classic': 'LUNC',
        'Terra': 'LUNA',
        'BNB (BEP2)': 'BEP2',
        'Caduceus': 'CMP',
        'Ethereum Classic': 'ETC',
        'Optimism': 'OPTIMISM',
        'Stellar Lumens': 'XLM',
        'Filecoin': 'FIL',
        'Klaytn': 'KLAY',
        'zkSync': 'ZKSYNC',
    }

    try:
        bybit_status = dict()
        for value in response['result']['rows']:
            bybit_status.update({value.get('name'): {}})
            for value_ in value.get('chains'):
                if value_.get('withdrawFee') not in ('', None):
                    if value_.get('chainType') in chain_rename:
                        chain = chain_rename[value_.get('chainType')]
                    else:
                        chain = value_.get('chainType')
                    if value_.get('chainDeposit') == '1':
                        deposit = True
                    else:
                        deposit = False
                    if value_.get('chainWithdraw') == '1':
                        withdrawal = True
                    else:
                        withdrawal = False
                    bybit_status[value.get('name')].update({chain: [deposit, withdrawal,
                                                                    float(value_.get('withdrawFee'))]})
        return bybit_status
    except (AttributeError, TypeError, KeyError):
        print("Закончил байбит 3")
        return None

async def kucoin_chain():
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get(f'https://api.kucoin.com/api/v1/currencies', headers=headers) as response:
    #             response = await response.json()
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.kucoin.com/api/v1/currencies', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        print("Закончил кукоин 2")
        return None

    kucoin_status = {
        'LOKI': {'LOKI': []}, 'NRG': {'NRG': []}, 'FET': {'ERC20': []}, 'XMR': {'XMR': []}, 'RBTC': {'RBTC': []},
        'RIF': {'RBTC': []}, 'ANKR': {'ERC20': []}, 'MTV': {'ERC20': []}, 'CRO': {'ERC20': []}, 'OPT': {'ERC20': []},
        'KMD': {'KMD': []}, 'RFOX': {'ERC20': []}, 'TT': {'TT': []}, 'ATOM': {'ATOM': []}, 'CHR': {'ERC20': []},
        'NIM': {'NIM': []}, 'OCEAN': {'ERC20': []}, 'COTI': {'COTI': []}, 'FX': {'ERC20': []}, 'PIVX': {'PIVX': []},
        'XTZ': {'XTZ': []}, 'BNB': {'BEP2': []}, 'JAR': {'ERC20': []}, 'ALGO': {'ALGO': []}, 'ADA': {'ADA': []},
        'XEM': {'NEM': []}, 'CIX100': {'ERC20': []}, 'ZEC': {'ZEC': []}, 'WXT': {'XLM': []},
        'FORESTPLUS': {'ERC20': []}, 'BOLT': {'ERC20': []}, 'ARPA': {'ERC20': []}, 'CHZ': {'BEP2': []},
        'NOIA': {'ERC20': []}, 'DAPPT': {'ERC20': []}, 'EOSC': {'EOSC': []}, 'DERO': {'DEROHE': []},
        'WIN': {'TRC20': []}, 'FKX': {'ERC20': []}, 'ENQ': {'ENQ': []}, 'THETA': {'THETA': []}, 'ONE': {'ONE': []},
        'TOKO': {'ERC20': []}, 'TFUEL': {'THETA': []}, 'LOL': {'IOST': []}, 'LUNA': {'LUNA': []}, 'VID': {'ERC20': []},
        'MXW': {'MXW': []}, 'SXP': {'ERC20': []}, 'VIDT': {'ERC20': []}, 'AKRO': {'ERC20': []}, 'ROOBEE': {'ERC20': []},
        'AMPL': {'ERC20': []}, 'MAP': {'ERC20': []}, 'COS': {'COS': []}, 'POL': {'TRC20': []}, 'ARX': {'ERC20': []},
        'NWC': {'XLM': []}, 'BEPRO': {'ERC20': []}, 'VRA': {'ERC20': []}, 'KSM': {'KSM': []}, 'SUTER': {'ERC20': []},
        'ACOIN': {'ERC20': []}, 'VI': {'ERC20': []}, 'AXE': {'AXE': []}, 'STEEM': {'STEEM': []}, 'SENSO': {'ERC20': []},
        'PRE': {'ERC20': []}, 'XDB': {'DigitalBits': []}, 'SYLO': {'ERC20': []}, 'WOM': {'ERC20': []},
        'LYXE': {'ERC20': []}, 'CADH': {'ERC20': []}, 'JST': {'TRC20': []}, 'STX': {'STX': []}, 'USDN': {'WAVES': []},
        'XSR': {'ERC20': []}, 'COMP': {'ERC20': []}, 'KAI': {'KAI': []}, 'DOT': {'ACA': []}, 'EWT': {'EWT': []},
        'WEST': {'WEST': []}, 'NVT': {'NULS': []}, 'BNS': {'ERC20': []}, 'ORN': {'ERC20': []}, 'PNK': {'ERC20': []},
        'WAVES': {'WAVES': []}, 'SUKU': {'ERC20': []}, 'MLK': {'LUK': []}, 'DIA': {'ERC20': []}, 'SHA': {'VET': []},
        'LINK': {'ERC20': []}, 'USDJ': {'TRC20': []}, 'ALEPH': {'ERC20': []}, 'EFX': {'EOS': []}, 'CKB': {'CKB': []},
        'UMA': {'ERC20': []}, 'VELO': {'XLM': []}, 'SUN': {'TRC20': []}, 'BUY': {'ERC20': []}, 'YFI': {'ERC20': []},
        'UNI': {'ERC20': []}, 'UOS': {'ERC20': []}, 'SATT': {'ERC20': []}, 'KTS': {'KTS': []}, 'DEGO': {'ERC20': []},
        'UDOO': {'ERC20': []}, 'RFUEL': {'ERC20': []}, 'UBX': {'ERC20': []}, 'FIL': {'FIL': []}, 'COMB': {'ERC20': []},
        'REAP': {'ERC20': []}, 'AAVE': {'ERC20': []}, 'TONE': {'ERC20': []}, 'OPCT': {'ERC20': []},
        'UQC': {'ERC20': []}, 'SHR': {'ERC20': []}, 'UBXT': {'ERC20': []}, 'ROSE': {'OASIS': []}, 'UST': {'LUNA': []},
        'CTI': {'ERC20': []}, 'BUX': {'BEP20': []}, 'XHV': {'XHV': []}, 'PLU': {'ERC20': []}, 'CAS': {'BEP2': []},
        'GRT': {'ERC20': []}, 'MSWAP': {'BEP20': []}, 'GOM2': {'ERC20': []}, 'REVV': {'ERC20': []},
        'LON': {'ERC20': []}, 'API3': {'ERC20': []}, 'SUSHI': {'ERC20': []}, 'UNFI': {'ERC20': []},
        'ALPA': {'ERC20': []}, '1INCH': {'ERC20': []}, 'HTR': {'HTR': []}, 'FRONT': {'ERC20': []},
        'WBTC': {'ERC20': []}, 'HYDRA': {'HYDRA': []}, 'MIR': {'ERC20': []}, 'DFI': {'DFI': []}, 'FRM': {'ERC20': []},
        'CRV': {'ERC20': []}, 'GZIL': {'ZIL': []}, 'ZEN': {'ZEN': []}, 'CUDOS': {'ERC20': []}, 'MAP2': {'LUK': []},
        'REN': {'ERC20': []}, 'LRC': {'ERC20': []}, 'KLV': {'TRC20': []}, 'BOA': {'ERC20': []}, 'QNT': {'ERC20': []},
        'BAT': {'ERC20': []}, 'DAO': {'ERC20': []}, 'DOGE': {'DOGE': []}, 'STRONG': {'ERC20': []},
        'TRIAS': {'ERC20': []}, 'MITX': {'ERC20': []}, 'CAKE': {'BEP20': []}, 'ORAI': {'ERC20': []},
        'LTX': {'ERC20': []}, 'ZEE': {'ERC20': []}, 'MASK': {'ERC20': []}, 'IDEA': {'ERC20': []}, 'PHA': {'ERC20': []},
        'SRK': {'ERC20': []}, 'SWINGBY': {'BEP2': []}, 'AVAX': {'AVAXC': []}, 'DON': {'IOST': []},
        'KRL': {'ERC20': []}, 'POLK': {'ERC20': []}, 'RNDR': {'ERC20': []}, 'RLY': {'ERC20': []}, 'ANC': {'ERC20': []},
        'SKEY': {'ERC20': []}, 'LAYER': {'ERC20': []}, 'TARA': {'ERC20': []}, 'XYM': {'XYM': []}, 'DYP': {'ERC20': []},
        'PCX': {'PCX': []}, 'ORBS': {'ERC20': []}, 'DSLA': {'ERC20': []}, 'FLUX': {'FLUX': []}, 'SAND': {'ERC20': []},
        'SPI': {'ERC20': []}, 'XCUR': {'ERC20': []}, 'VAI': {'ERC20': []}, 'DODO': {'ERC20': []},
        'PUNDIX': {'ERC20': []}, 'BOSON': {'ERC20': []}, 'HT': {'HRC20': []}, 'PDEX': {'ERC20': []},
        'LABS': {'ERC20': []}, 'STRK': {'ERC20': []}, 'PHNX': {'ERC20': []}, 'HAI': {'VET': []}, 'EQZ': {'ERC20': []},
        'FORTH': {'ERC20': []}, 'HORD': {'ERC20': []}, 'CGG': {'ERC20': []}, 'GHX': {'ERC20': []}, 'TCP': {'ERC20': []},
        'TOWER': {'ERC20': []}, 'ACE': {'ERC20': []}, 'STND': {'ERC20': []}, 'LOCG': {'ERC20': []},
        'FLY': {'ERC20': []}, 'CARD': {'ERC20': []}, 'XDC': {'XDC': []}, 'CWS': {'BEP20': []}, 'FCL': {'ERC20': []},
        'SHIB': {'ERC20': []}, 'POLX': {'MATIC': []}, 'KDA': {'KDA': []}, 'GOVI': {'ERC20': []}, 'ICP': {'ICP': []},
        'CELO': {'CELO': []}, 'CUSD': {'CELO': []}, 'STC': {'ERC20': []}, 'MATIC': {'ERC20': []}, 'OGN': {'ERC20': []},
        'OUSD': {'ERC20': []}, 'GLQ': {'ERC20': []}, 'TLOS': {'ERC20': []}, 'YOP': {'ERC20': []}, 'MXC': {'ERC20': []},
        'ERSDL': {'ERC20': []}, 'HOTCROSS': {'BEP20': []}, 'HYVE': {'ERC20': []}, 'DAPPX': {'ERC20': []},
        'FEAR': {'ERC20': []}, 'KONO': {'ERC20': []}, 'MAHA': {'ERC20': []}, 'UNO': {'ERC20': []}, 'PRQ': {'ERC20': []},
        'PYR': {'ERC20': []}, 'GLCH': {'ERC20': []}, 'ALBT': {'ERC20': []}, 'XCAD': {'ERC20': []},
        'PROM': {'ERC20': []}, 'ELON': {'ERC20': []}, 'APL': {'APL': []}, 'DIVI': {'DIVI': []}, 'VEED': {'VET': []},
        'LSS': {'ERC20': []}, 'JUP': {'BEP20': []}, 'AGIX': {'ERC20': []}, 'DORA': {'ERC20': []},
        'LPOOL': {'ERC20': []}, 'ETHO': {'ERC20': []}, 'POLS': {'ERC20': []}, 'KOK': {'ERC20': []},
        'ABBC': {'ABBC': []}, 'ZCX': {'ERC20': []}, 'ROSN': {'BEP20': []}, 'NORD': {'ERC20': []}, 'GMEE': {'ERC20': []},
        'XAVA': {'AVAXC': []}, 'AI': {'ERC20': []}, 'SFUND': {'BEP20': []}, 'IOI': {'ERC20': []},
        'ALPACA': {'BEP20': []}, 'NFT': {'TRC20': []}, 'MNST': {'BEP20': []}, 'MEM': {'ERC20': []},
        'DLTA': {'ERC20': []}, 'AIOZ': {'BEP20': []}, 'MARSH': {'BEP20': []}, 'CQT': {'ERC20': []},
        'HAPI': {'ERC20': []}, 'GENS': {'BEP20': []}, 'YFDAI': {'ERC20': []}, 'FORM': {'ERC20': []},
        'MODEFI': {'ERC20': []}, 'ARRR': {'ARRR': []}, 'SPHRI': {'ERC20': []}, 'CEUR': {'CELO': []},
        'ASD': {'ERC20': []}, 'EXRD': {'ERC20': []}, 'NGM': {'ERC20': []}, 'LPT': {'ERC20': []}, 'STMX': {'ERC20': []},
        'BOND': {'ERC20': []}, '2CRZ': {'ERC20': []}, 'SHFT': {'ERC20': []}, 'NEAR': {'NEAR': []}, 'OOE': {'ERC20': []},
        'DFYN': {'ERC20': []}, 'CFG': {'ERC20': []}, 'AXC': {'ERC20': []}, 'MUSH': {'ERC20': []}, 'SMT': {'ERC20': []},
        'AXS': {'ERC20': []}, 'CLV': {'ERC20': []}, 'ROUTE': {'ERC20': []}, 'KAR': {'KAR': []}, 'BURP': {'ERC20': []},
        'DPET': {'KAI': []}, 'PMON': {'ERC20': []}, 'ERG': {'ERG': []}, 'LITH': {'ERC20': []}, 'SOL': {'SOL': []},
        'SLP': {'ERC20': []}, 'XCH': {'XCH': []}, 'HAKA': {'ERC20': []}, 'MTL': {'ERC20': []}, 'GALAX': {'ERC20': []},
        'CIRUS': {'ERC20': []}, 'TXA': {'ERC20': []}, 'QI': {'AVAXC': []}, 'ODDZ': {'BEP20': []}, 'PNT': {'ERC20': []},
        'XPR': {'XPR': []}, 'TRIBE': {'ERC20': []}, 'MOVR': {'MOVR': []}, 'MAKI': {'HRC20': []}, 'QRDO': {'ERC20': []},
        'WOO': {'ERC20': []}, 'WILD': {'ERC20': []}, 'SDN': {'SDN': []}, 'REP': {'ERC20': []}, 'BNT': {'ERC20': []},
        'OXT': {'ERC20': []}, 'BAL': {'ERC20': []}, 'STORJ': {'ERC20': []}, 'YGG': {'ERC20': []}, 'NDAU': {'NDAU': []},
        'SDAO': {'ERC20': []}, 'SKL': {'ERC20': []}, 'NMR': {'ERC20': []}, 'TRB': {'ERC20': []}, 'IXS': {'ERC20': []},
        'PBX': {'ERC20': []}, 'GTC': {'ERC20': []}, 'DYDX': {'ERC20': []}, 'EQX': {'ERC20': []}, 'RLC': {'ERC20': []},
        'XNL': {'ERC20': []}, 'HBAR': {'HBAR': []}, 'XPRT': {'XPRT': []}, 'EGLD': {'EGLD': []}, 'FLOW': {'FLOW': []},
        'NKN': {'ERC20': []}, 'MLN': {'ERC20': []}, 'WNCG': {'ERC20': []}, 'DMTR': {'ERC20': []}, 'CTSI': {'ERC20': []},
        'ALICE': {'ERC20': []}, 'OPUL': {'ERC20': []}, 'ILV': {'ERC20': []}, 'BAND': {'BAND': []}, 'FTT': {'ERC20': []},
        'DVPN': {'DVPN': []}, 'SKU': {'ERC20': []}, 'SLIM': {'SOL': []}, 'EDG': {'EDG': []}, 'DEXE': {'BEP20': []},
        'TLM': {'BEP20': []}, 'RMRK': {'RMRK': []}, 'RUNE': {'RUNE': []}, 'MATTER': {'ERC20': []}, 'SOV': {'RBTC': []},
        'BMON': {'BEP20': []}, 'C98': {'BEP20': []}, 'BLOK': {'MATIC': []}, 'SOLR': {'SOL': []},
        'SIENNA': {'ERC20': []}, 'PUSH': {'ERC20': []}, 'WSIENNA': {'ERC20': []}, 'NTVRK': {'ERC20': []},
        'YLD': {'ERC20': []}, 'FLAME': {'MATIC': []}, 'AGLD': {'ERC20': []}, 'NAKA': {'MATIC': []},
        'REEF': {'BEP20': []}, 'TORN': {'ERC20': []}, 'TIDAL': {'ERC20': []}, 'TVK': {'ERC20': []}, 'INJ': {'INJ': []},
        'NFTB': {'BEP20': []}, 'ALPHA': {'BEP20': []}, 'BADGER': {'ERC20': []}, 'VEGA': {'ERC20': []},
        'ZKT': {'ERC20': []}, 'AR': {'AR': []}, 'XVS': {'BEP20': []}, 'GHST': {'ERC20': []}, 'PERP': {'ERC20': []},
        'SCLP': {'BEP20': []}, 'JASMY': {'ERC20': []}, 'CPOOL': {'ERC20': []}, 'LTO': {'ERC20': []},
        'SUPER': {'BEP20': []}, 'BASIC': {'ERC20': []}, 'AURY': {'SOL': []}, 'HERO': {'BEP20': []},
        'XED': {'ERC20': []}, 'SWASH': {'ERC20': []}, 'DREAMS': {'BEP20': []}, 'MTRG': {'BEP20': []},
        'QUICK': {'ERC20': []}, 'TRU': {'ERC20': []}, 'WRX': {'BEP2': []}, 'TKO': {'BEP20': []}, 'DATA': {'ERC20': []},
        'ISP': {'ERC20': []}, 'CERE': {'ERC20': []}, 'SHILL': {'BEP20': []}, 'HEGIC': {'ERC20': []},
        'ERN': {'ERC20': []}, 'PAXG': {'ERC20': []}, 'AUDIO': {'ERC20': []}, 'FTG': {'ERC20': []}, 'XTM': {'ERC20': []},
        'ENS': {'ERC20': []}, 'ATA': {'ERC20': []}, 'FXS': {'ERC20': []}, 'MNW': {'ERC20': []}, 'CWAR': {'SOL': []},
        'VXV': {'ERC20': []}, 'DPR': {'BEP20': []}, 'SWP': {'KAVA': []}, 'PBR': {'ERC20': []}, 'WNXM': {'ERC20': []},
        'ANT': {'ERC20': []}, 'ADX': {'ERC20': []}, 'TWT': {'BEP20': []}, 'OM': {'BEP20': []}, 'GLM': {'ERC20': []},
        'NUM': {'BEP20': []}, 'BAKE': {'BEP20': []}, 'MONI': {'BEP20': []}, 'TRADE': {'MATIC': []}, 'VLX': {'VLX': []},
        '1EARTH': {'ERC20': []}, 'KAVA': {'KAVA': []}, 'LIKE': {'SOL': []}, 'LIT': {'ERC20': []}, 'MFT': {'ERC20': []},
        'SFP': {'BEP20': []}, 'BURGER': {'BEP20': []}, 'ILA': {'BEP20': []}, 'CREAM': {'BEP20': []},
        'RSR': {'ERC20': []}, 'GODS': {'ERC20': []}, 'IMX': {'ERC20': []}, 'KMA': {'KMA': []}, 'SRM': {'SOL': []},
        'POLC': {'BEP20': []}, 'XTAG': {'SOL': []}, 'VR': {'ERC20': []}, 'MNET': {'ERC20': []}, 'NGC': {'ERC20': []},
        'HARD': {'KAVA': []}, 'UNIC': {'ERC20': []}, 'POND': {'ERC20': []}, 'MDX': {'BEP20': []}, 'EPIK': {'ERC20': []},
        'NGL': {'ERC20': []}, 'KDON': {'ERC20': []}, 'PEL': {'BEP20': []}, 'KLAY': {'KLAY': []}, 'LINA': {'ERC20': []},
        'CREDI': {'ERC20': []}, 'TRVL': {'ERC20': []}, 'ARKER': {'BEP20': []}, 'XEC': {'XEC': []},
        'BONDLY': {'ERC20': []}, 'LACE': {'BEP20': []}, 'HEART': {'ERC20': []}, 'UNB': {'BEP20': []},
        'FORWARD': {'BEP20': []}, 'GAFI': {'BEP20': []}, 'KOL': {'ERC20': []}, 'CHMB': {'BEP20': []},
        'FALCONS': {'BEP20': []}, 'UFO': {'ERC20': []}, 'GEEQ': {'ERC20': []}, 'RACEFI': {'SOL': []},
        'ORC': {'ERC20': []}, 'PEOPLE': {'ERC20': []}, 'ADS': {'ERC20': []}, 'OOKI': {'ERC20': []},
        'SOS': {'ERC20': []}, 'WHALE': {'ERC20': []}, 'IOTA': {'IOTA': []}, 'CWEB': {'ERC20': []}, 'HNT': {'HNT': []},
        'GGG': {'BEP20': []}, 'CLH': {'ERC20': []}, 'REVU': {'ADA': []}, 'PLGR': {'BEP20': []}, 'GLMR': {'GLMR': []},
        'CTC': {'ERC20': []}, 'LOVE': {'ERC20': []}, 'GARI': {'SOL': []}, 'FRR': {'ERC20': []}, 'ASTR': {'ASTR': []},
        'ERTHA': {'BEP20': []}, 'FCON': {'SOL': []}, 'ACA': {'ACA': []}, 'MTS': {'BEP20': []}, 'ROAR': {'BEP20': []},
        'HBB': {'SOL': []}, 'SURV': {'BEP20': []}, 'AMP': {'ERC20': []}, 'CVX': {'ERC20': []}, 'MJT': {'KCC': []},
        'XNO': {'NANO': []}, 'SHX': {'XLM': []}, 'STARLY': {'BEP20': []}, 'ONSTON': {'ERC20': []}, 'WMT': {'ADA': []},
        'RANKER': {'ERC20': []}, 'LAVAX': {'BEP20': []}, 'MARS4': {'ERC20': []}, 'METIS': {'ERC20': []},
        'WAL': {'BEP20': []}, 'BULL': {'MATIC': []}, 'SON': {'BEP20': []}, 'MELOS': {'ERC20': []}, 'APE': {'ERC20': []},
        'VSYS': {'VSYS': []}, 'ACT': {'ACT': []}, 'ADB': {'ERC20': []}, 'AERGO': {'ERC20': []}, 'AION': {'AION': []},
        'AMB': {'AMB': []}, 'AOA': {'AURORA': []}, 'AVA': {'BEP2': []}, 'AXPR': {'ERC20': []}, 'BAX': {'ERC20': []},
        'BCD': {'BCD': []}, 'BCH': {'BCH': []}, 'BCHSV': {'BCHSV': []}, 'BTC': {'BTC': []}, 'BTCP': {'BTCP': []},
        'CAPP': {'ERC20': []}, 'COV': {'ERC20': []}, 'CPC': {'CPC': []}, 'CRPT': {'ERC20': []}, 'CS': {'CS': []},
        'CV': {'ERC20': []}, 'CVC': {'ERC20': []}, 'DAG': {'DAG': []}, 'DAI': {'ERC20': []}, 'DASH': {'DASH': []},
        'DCR': {'DCR': []}, 'DENT': {'ERC20': []}, 'DGB': {'DGB': []}, 'DOCK': {'DOCK': []}, 'DRGN': {'ERC20': []},
        'ELA': {'ELA': []}, 'ELF': {'ERC20': []}, 'ENJ': {'ERC20': []}, 'EOS': {'EOS': []}, 'EPRX': {'ERC20': []},
        'ETC': {'ETC': []}, 'ETF': {'ERC20': []}, 'ETH': {'ERC20': []}, 'ETN': {'ETN': []}, 'FTM': {'ERC20': []},
        'GAS': {'NEO': []}, 'GGC': {'ERC20': []}, 'GMB': {'ERC20': []}, 'GO': {'GO': []}, 'GOD': {'GOD': []},
        'IOST': {'IOST': []}, 'IOTX': {'IOTX': []}, 'J8T': {'ERC20': []}, 'KAT': {'ERC20': []}, 'KCS': {'ERC20': []},
        'KEY': {'ERC20': []}, 'KNC': {'ERC20': []}, 'LOC': {'HYDRA': []}, 'LOOM': {'ERC20': []}, 'LSK': {'LSK': []},
        'LTC': {'LTC': []}, 'LYM': {'ERC20': []}, 'MAN': {'MAN': []}, 'MANA': {'ERC20': []}, 'MKR': {'ERC20': []},
        'MVP': {'ERC20': []}, 'NEO': {'NEO': []}, 'NULS': {'NULS': []}, 'OLT': {'OLT': []}, 'OMG': {'ERC20': []},
        'ONG': {'ONT': []}, 'ONT': {'ONT': []}, 'PLAY': {'ERC20': []}, 'POWR': {'ERC20': []}, 'PPT': {'ERC20': []},
        'QKC': {'QKC': []}, 'QTUM': {'QTUM': []}, 'R': {'ERC20': []}, 'REQ': {'ERC20': []}, 'SNT': {'ERC20': []},
        'SNX': {'ERC20': []}, 'SOUL': {'NEO': []}, 'SUSD': {'ERC20': []}, 'TEL': {'ERC20': []}, 'TIME': {'ERC20': []},
        'TOMO': {'TOMO': []}, 'TRAC': {'ERC20': []}, 'TRX': {'TRC20': []}, 'TUSD': {'ERC20': []}, 'USDC': {'ERC20': []},
        'USDT': {'ERC20': []}, 'UTK': {'ERC20': []}, 'VET': {'VET': []}, 'VTHO': {'VET': []}, 'WAN': {'WAN': []},
        'WAX': {'ERC20': []}, 'XLM': {'XLM': []}, 'XRP': {'XRP': []}, 'XYO': {'ERC20': []}, 'ZIL': {'ZIL': []},
        'ZRX': {'ERC20': []}, 'GRIN': {'GRIN': []}, 'SOLVE': {'ERC20': []}, 'BTT': {'TRC20': []}, 'MHC': {'MHC': []},
        'GMT': {'BEP20': []}, 'BICO': {'ERC20': []}, 'STG': {'ERC20': []}, 'LMR': {'ERC20': []}, 'LOKA': {'ERC20': []},
        'URUS': {'ERC20': []}, 'BNC': {'BNC': []}, 'JAM': {'ERC20': []}, 'LBP': {'ERC20': []}, 'CFX': {'CFX': []},
        'XCN': {'ERC20': []}, 'KP3R': {'ERC20': []}, 'LOOKS': {'ERC20': []}, 'UPO': {'MATIC': []},
        'INDI': {'ERC20': []}, 'TITAN': {'ERC20': []}, 'SPELL': {'ERC20': []}, 'SLCL': {'SOL': []},
        'RPC': {'ERC20': []}, 'CEEK': {'ERC20': []}, 'T': {'ERC20': []}, 'BETA': {'BEP20': []}, 'VEMP': {'ERC20': []},
        'NHCT': {'AVAXC': []}, 'FRA': {'FRA': []}, 'ARNM': {'SOL': []}, 'VISION': {'SOL': []}, 'ALPINE': {'BEP20': []},
        'COCOS': {'ERC20': []}, 'BNX': {'BEP20': []}, 'ZBC': {'SOL': []}, 'WOOP': {'BEP20': []}, 'NYM': {'ERC20': []},
        'VOXEL': {'MATIC': []}, 'PSTAKE': {'ERC20': []}, 'SPA': {'ERC20': []}, 'RACA': {'BEP20': []},
        'DAR': {'BEP20': []}, 'SYNR': {'ERC20': []}, 'MV': {'MATIC': []}, 'XDEFI': {'ERC20': []}, 'HAWK': {'SOL': []},
        'SWFTC': {'ERC20': []}, 'XWG': {'BEP20': []}, 'IDEX': {'ERC20': []}, 'BRWL': {'ERC20': []},
        'TAUM': {'BEP20': []}, 'CELR': {'ERC20': []}, 'ITAMCUBE': {'BEP20': []}, 'AURORA': {'ERC20': []},
        'ELITEHERO': {'KCC': []}, 'POSI': {'BEP20': []}, 'SIN': {'BEP20': []}, 'COOHA': {'KCC': []},
        'EPK': {'ERC20': []}, 'PLD': {'SOL': []}, 'EPX': {'BEP20': []}, 'PSL': {'PSL': []}, 'SYS': {'SYSEVM': []},
        'OVR': {'ERC20': []}, 'PKF': {'ERC20': []}, 'DG': {'ERC20': []}, 'BRISE': {'BEP20': []}, 'PLY': {'ERC20': []},
        'GST': {'SOL': []}, 'AKT': {'AKT': []}, 'FSN': {'FSN': []}, 'GAL': {'ERC20': []}, 'FITFI': {'AVAXC': []},
        'BSW': {'BEP20': []}, 'H2O': {'BEP20': []}, 'AUSD': {'ACA': []}, 'GMM': {'BEP20': []}, 'FCD': {'MATIC': []},
        'BOBA': {'ERC20': []}, 'XRACER': {'KCC': []}, 'BFC': {'ERC20': []}, 'BIFI': {'ERC20': []},
        'KARA': {'BEP20': []}, 'DFA': {'ERC20': []}, 'KYL': {'ERC20': []}, 'CELT': {'ERC20': []}, 'MBL': {'ONT': []},
        'DUSK': {'ERC20': []}, 'CCD': {'CCD': []}, 'USDD': {'TRC20': []}, 'MBOX': {'BEP20': []}, 'SCRT': {'SCRT': []},
        'MLS': {'KCC': []}, 'AFK': {'BEP20': []}, 'ACH': {'ERC20': []}, 'IHC': {'BEP20': []}, 'STORE': {'ERC20': []},
        'DOSE': {'ERC20': []}, 'LUNC': {'LUNC': []}, 'USTC': {'LUNC': []}, 'IDLENFT': {'KCC': []},
        'OP': {'OPTIMISM': []}, 'EVER': {'ERC20': []}, 'ICX': {'ICX': []}, 'MOOV': {'BEP20': []}, 'USDP': {'ERC20': []},
        'WELL': {'GLMR': []}, 'CSPR': {'CSPR': []}, 'FORT': {'ERC20': []}, 'WEMIX': {'WEMIX': []}, 'OGV': {'ERC20': []},
        'OLE': {'BEP20': []}, 'LDO': {'ERC20': []}, 'CULT': {'ERC20': []}, 'RBP': {'KCC': []}, 'SRBP': {'KCC': []},
        'HIBAYC': {'ERC20': []}, 'HIPUNKS': {'ERC20': []}, 'BUSD': {'BEP20': []}, 'FIDA': {'SOL': []},
        'WOMBAT': {'ERC20': []}, 'FT': {'ERC20': []}, 'HIENS4': {'ERC20': []}, 'EGAME': {'ERC20': []},
        'STEPWATCH': {'MATIC': []}, 'HISAND33': {'ERC20': []}, 'XRD': {'XRD': []}, 'PIKASTER2': {'BEP20': []},
        'DC': {'ERC20': []}, 'HIENS3': {'ERC20': []}, 'NEER': {'PIONEER': []}, 'RVN': {'RVN': []}, 'MC': {'BEP20': []},
        'PEEL': {'BEP20': []}, 'SDL': {'ERC20': []}, 'HIODBS': {'ERC20': []}, 'SWEAT': {'ERC20': []},
        'CMP': {'CMP': []}, 'PIX': {'PIX': []}, 'HIDOODLES': {'ERC20': []}, 'MPLX': {'SOL': []}, 'ETHW': {'ETHW': []},
        'QUARTZ': {'ERC20': []}, 'PUMLX': {'ERC20': []}, 'HIMAYC': {'ERC20': []}, 'ACQ': {'ERC20': []},
        'RED': {'ERC20': []}, 'AOG': {'BEP20': []}, 'PRMX': {'ERC20': []}, 'XETA': {'AVAXC': []}, 'GEM': {'ERC20': []},
        'HIOD': {'ERC20': []}, 'KICKS': {'BEP20': []}, 'ASTROBOY': {'ERC20': []}, 'DERC': {'ERC20': []},
        'TRIBL': {'ERC20': []}, 'P00LS': {'ERC20': []}, 'GMX': {'ARBITRUM': []}, 'POKT': {'POKT': []},
        'EFI': {'EFINITY': []}, 'APT': {'APT': []}, 'BBC': {'BEP20': []}, 'EUL': {'ERC20': []}, 'TON': {'TON': []},
        'HIMEEBITS': {'ERC20': []}, 'HISQUIGGLE': {'ERC20': []}, 'PIAS': {'BEP20': []}, 'XCV': {'BEP20': []},
        'ECOX': {'ERC20': []}, 'HFT': {'ERC20': []}, 'MM': {'BEP20': []}, 'HIFIDENZA': {'ERC20': []},
        'AZERO': {'AZERO': []}, 'BEAT': {'MATIC': []}, 'CLUB': {'ERC20': []}, 'MATCH': {'ERC20': []},
        'NRFB': {'ERC20': []}, 'HIGAZERS': {'ERC20': []}, 'NAVI': {'ERC20': []}, 'HIPENGUINS': {'ERC20': []},
        'CARE': {'ERC20': []}, 'ALT': {'APT': []}, 'HICLONEX': {'ERC20': []}, 'OAS': {'OAS': []},
        'PRIMAL': {'BEP20': []}, 'HICOOLCATS': {'ERC20': []}, 'HIAZUKI': {'ERC20': []}, 'TEM': {'ERC20': []},
        'HIFLUF': {'ERC20': []}, 'OSMO': {'OSMO': []}, 'FLR': {'FLR': []}, 'HIBIRDS': {'ERC20': []},
        'BDX': {'BDX': []}, 'HIMFERS': {'ERC20': []}, 'SIMP': {'ERC20': []}, 'MAGIC': {'ARBITRUM': []},
        'ASTRA': {'ERC20': []}, 'HIVALHALLA': {'ERC20': []}, 'SQUAD': {'BEP20': []}, 'RPL': {'ERC20': []},
        'HIRENGA': {'ERC20': []}, 'HIGH': {'ERC20': []}, 'KING': {'ERC20': []}, 'HIUNDEAD': {'ERC20': []},
        'GFT': {'BEP20': []}, 'FLOKI': {'BEP20': []}, 'HIFRIENDS': {'ERC20': []}, 'BLUR': {'ERC20': []},
        'WAXL': {'ERC20': []}, 'SSV': {'ERC20': []}, 'IGU': {'BEP20': []}, 'ACS': {'SOL': []}
    }

    try:
        for value in response['data']:
            if value.get('currency') in kucoin_status:
                key = list(kucoin_status[value.get('currency')].keys())
                kucoin_status[value.get('currency')][key[-1]] = [value.get('isDepositEnabled'),
                                                                 value.get('isWithdrawEnabled'),
                                                                 float(value.get('withdrawalMinFee'))]
        return kucoin_status
    except (AttributeError, TypeError, KeyError):
        print("Закончил кукоин 3")
        return None

async def gateio_chain():
    key = 'e6537c5b818488ce71439e88bfa91216'
    secret = 'd458a6f26c8d95c8cc7680795fec3d3642a7f53b3bdc5b49785c57550b1fcd99'

    t = time.time()
    m = hashlib.sha512()
    m.update(("").encode('utf-8'))
    hashed_payload = m.hexdigest()
    s = '%s\n%s\n%s\n%s\n%s' % ('GET', '/api/v4/wallet/withdraw_status', "", hashed_payload, t)
    sign = hmac.new(secret.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
    gen_sign = {'KEY': key, 'Timestamp': str(t), 'SIGN': sign}
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    sign_headers = gen_sign
    headers.update(sign_headers)
    url = ('https://api.gateio.ws/api/v4/wallet/withdraw_status')

    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get('https://api.gateio.ws/api/v4/spot/currencies') as response1:
    #             response1 = await response1.json()
    #         async with session.get(url, headers=headers) as response2:
    #             response2 = await response2.json()
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.gateio.ws/api/v4/spot/currencies') as response1:
                response1 = await response1.json()
            async with session.get(url, headers=headers) as response2:
                response2 = await response2.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError,
            aiohttp.ServerConnectionError, aiohttp.ServerTimeoutError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        print("Закончил гейтио 2")
        return None

    chain_rename = {
        'BSC': 'BEP20',
        'ETH': 'ERC20',
        'ARB': 'ARBITRUM',
        'AVAX_C': 'AVAXC',
        'BNB': 'BEP2',
        'TRX': 'TRC20',
        'APT': 'APTOS'
    }

    try:
        gateio_status = dict()
        for value in response1:
            if '_' in value.get('currency'):
                coin = value.get('currency').split('_')[0]
            else:
                coin = value.get('currency')
            if value.get('chain') in chain_rename:
                chain = chain_rename[value.get('chain')]
            else:
                chain = value.get('chain')
            if coin not in gateio_status:
                gateio_status.update({coin: {chain: [not value.get('deposit_disabled'),
                                                     not value.get('withdraw_disabled'), None]}})
            else:
                gateio_status[coin].update({chain: [not value.get('deposit_disabled'),
                                                    not value.get('withdraw_disabled'), None]})

        for value_ in response2:
            if value_.get('currency') in gateio_status:
                if list(value_.keys())[-1] == 'withdraw_fix_on_chains':
                    for chain in value_.get('withdraw_fix_on_chains'):
                        if chain in chain_rename:
                            chain_ = chain_rename.get(chain)
                        else:
                            chain_ = chain
                        if chain_ in gateio_status[value_.get('currency')]:
                            gateio_status[value_.get('currency')][chain_][2] = float(
                                value_.get('withdraw_fix_on_chains')[chain])
        return gateio_status
    except (AttributeError, TypeError, KeyError):
        print("Закончил гейтио 3")
        return None

async def mexc_chain():
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get('https://www.mexc.com/open/api/v2/market/coin/list', headers=headers) as response:
    #             response = await response.json()
    # except (ssl.SSLError, ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.mexc.com/open/api/v2/market/coin/list', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        print("Закончил мехс 2")
        return None

    chain_rename = {
        'BEP20(BSC)': 'BEP20',
        'Chiliz Chain(CHZ)': 'CHZ',
        'AVAX_CCHAIN': 'AVAXC',
        'Arbitrum One': 'ARBITRUM',
        'OP': 'OPTIMISM',
        'AVAX_XCHAIN': 'AVAXX',
        'Khala': 'KHALA',
        'LUNA2': 'LUNA',
        'UGAS(Ultrain)': 'UGAS',
        'MEVerse': 'MEVERSE',
        'RONIN': 'RON',
        'FLARE': 'FLR'
    }

    try:
        mexc_status = dict()
        for value in response['data']:
            mexc_status.update({value.get('currency'): {}})
            for value_ in value.get('coins'):
                if value_.get('chain') in chain_rename:
                    chain = chain_rename[value_.get('chain')]
                else:
                    chain = value_.get('chain')
                mexc_status[value.get('currency')].update({chain: [value_.get('is_deposit_enabled'),
                                                        value_.get('is_withdraw_enabled'), float(value_.get('fee'))]})
        return mexc_status
    except (AttributeError, TypeError, KeyError):
        print("Закончил мехс 3")
        return None

async def okx_chain():
    APIKEY = "9f0d4cac-e021-48c6-9b08-721ac54b40bc"
    APISECRET = "2188F335A6D88338BF020D528DA5FF4C"
    PASS = "Qwerty1!"
    URL = 'https://aws.okex.com/api/v5/asset/currencies'

    cur_time = (dt.datetime.utcnow().isoformat()[:-3] + 'Z')
    message = (str(cur_time) + 'GET' + '/api/v5/asset/currencies' + '')
    mac = hmac.new(bytes(APISECRET, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    signature = base64.b64encode(d).decode('utf8')
    headers = {
        'CONTENT-TYPE': 'application/json',
        'OK-ACCESS-KEY': APIKEY,
        'OK-ACCESS-SIGN': signature,
        'OK-ACCESS-TIMESTAMP': str(cur_time),
        'OK-ACCESS-PASSPHRASE': PASS
    }

    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get(URL, headers=headers) as response:
    #             response = await response.json()
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(URL, headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        print("Закончил окх 2")
        return None

    chain_rename = {
        'Polygon': 'MATIC',
        'Avalanche C-Chain': 'AVAXC',
        'Bitcoin': 'BTC',
        'Arbitrum one': 'ARBITRUM',
        'Optimism': 'OPTIMISM',
        'EthereumPoW': 'ETHW',
        'Litecoin': 'LTC',
        'BitcoinCash': 'BCH',
        'Ethereum Classic': 'ETC',
        'Acala': 'ACALA',
        'Cardano': 'ADA',
        'Algorand': 'ALGO',
        'Terra Classic': 'LUNC',
        'Aptos': 'APTOS',
        'Arweave': 'AR',
        'Chiliz': 'CHZ',
        'Astar': 'ASTAR',
        'Cosmos': 'ATOM',
        'Avalanche X-Chain': 'AVAXX',
        'BSC': 'BEP20',
        'Bitcoin Diamond': 'BCD',
        'Klaytn': 'KLAY',
        'BitcoinGold': 'BTG',
        'Bytom': 'BTM',
        'Conflux': 'CFX',
        'CyberMiles': 'CMT',
        'Casper': 'CSPR',
        'Cortex': 'CTXC',
        'Decred': 'DCR',
        'Digibyte': 'DGB',
        'Dogecoin': 'DOGE',
        'Polkadot': 'DOT',
        'Elrond': 'EGLD',
        'Eminer': 'EM',
        'Filecoin': 'FIL',
        'Flare': 'FLR',
        'Fusion': 'FSN',
        'Fantom': 'FTM',
        'Solana': 'SOL',
        'Moonbeam': 'GLMR',
        'Hedera': 'HBAR',
        'HyperCash': 'HC',
        'Helium': 'HNT',
        'Kadena': 'KDA',
        'Kusama': 'KSM',
        'PlatON': 'LAT',
        'Lisk': 'LSK',
        'Terra': 'LUNA',
        'Metis': 'METIS',
        'Mina': 'MINA',
        'Moonriver': 'MOVR',
        'Nebulas': 'NAS',
        'Harmony': 'ONE',
        'Ontology': 'ONT',
        'Khala': 'KHALA',
        'Quantum': 'QAU',
        'Stellar Lumens': 'XLM',
        'Ronin': 'RON',
        'Ravencoin': 'RVM',
        'Siacoin': 'SC',
        'Ripple': 'XRP',
        'l-Stacks': 'STX',
        'Theta': 'THETA',
        'TrueChain': 'TRUE',
        'Wax': 'WAXP',
        'Chia': 'XCH',
        'New Economy Movement': 'NEM',
        'Monero': 'XMR',
        'Nano': 'XNO',
        'Tezos': 'XTZ',
        'Zcash': 'ZEC',
        'Horizen': 'ZEN',
        'Zilliqa': 'ZIL',
        'Step Network': 'STEP',
        'WAXP': 'WAX',
        'ICON': 'ICX'
    }

    try:
        okx_status = dict()
        for value in response['data']:
            if value.get('chain').replace(f'{value.get("ccy")}-', '') in chain_rename:
                chain = chain_rename[value.get('chain').replace(f'{value.get("ccy")}-', '')]
            else:
                chain = value.get('chain').replace(f'{value.get("ccy")}-', '')
            if value.get('ccy') not in okx_status:
                okx_status.update({value.get('ccy'): {chain: [value.get('canDep'), value.get('canWd'),
                                                                float(value.get('maxFee'))]}})
            else:
                okx_status[value.get('ccy')].update({chain: [value.get('canDep'), value.get('canWd'),
                                                                float(value.get('maxFee'))]})
        return okx_status
    except (AttributeError, TypeError, KeyError):
        print("Закончил окх 3")
        return None

async def whitebit_chain():
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get('https://whitebit.com/api/v4/public/assets', headers=headers) as response1:
    #             response1 = await response1.json()
    #         async with session.get('https://whitebit.com/api/v4/public/fee', headers=headers) as response2:
    #             response2 = await response2.json()
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://whitebit.com/api/v4/public/assets', headers=headers) as response1:
                response1 = await response1.json()
            async with session.get('https://whitebit.com/api/v4/public/fee', headers=headers) as response2:
                response2 = await response2.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        print("Закончил вайтбит 2")
        return None

    chain_rename = {
        'POLYGON': 'MATIC',
        'CCHAIN': 'AVAXC',
        'XCHAIN': 'AVAXX',
        'TRX': 'TRC20',
        'STELLAR': 'XLM',
        'eTOK': 'ETOK',
        'APT': 'APTOS',
        'WAXP': 'WAX'
    }

    try:
        whitebit_status = dict()
        for value in response1:
            if 'networks' in response1.get(value):
                if 'deposits' in response1.get(value)['networks']:
                    whitebit_status.update({value: {}})
                    for depo_chain in response1.get(value)['networks']['deposits']:
                        if depo_chain in chain_rename:
                            chain = chain_rename.get(depo_chain)
                        else:
                            chain = depo_chain
                        whitebit_status[value].update({chain: [True, False, None]})
                if 'withdraws' in response1.get(value)['networks']:
                    for with_chain in response1.get(value)['networks']['withdraws']:
                        if with_chain in chain_rename:
                            chain = chain_rename.get(with_chain)
                        else:
                            chain = with_chain
                        if value in whitebit_status:
                            if chain in whitebit_status[value]:
                                whitebit_status[value][chain][1] = True
                            else:
                                whitebit_status[value].update({chain: [False, True, None]})
                        else:
                            whitebit_status.update({value: {chain: [False, True, None]}})

        for value in response2:
            if '(' in value:
                value_ = value.split()
                if value_[0] in whitebit_status:
                    if value_[1].strip('()') in whitebit_status[value_[0]]:
                        whitebit_status[value_[0]][value_[1].strip('()')][2] = float(
                            response2.get(value)['withdraw']['fixed'])
            else:
                if value in whitebit_status:
                    key = list(whitebit_status[value].keys())
                    if response2.get(value)['withdraw']['fixed'] is not None:
                        whitebit_status[value][key[0]][2] = float(response2.get(value)['withdraw']['fixed'])
                    else:
                        whitebit_status[value][key[0]][2] = None
        return whitebit_status
    except (AttributeError, TypeError, KeyError):
        print("Закончил вайтбит 3")
        return None

async def poloniex_chain():
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get(f'https://api.poloniex.com/currencies/'
    #                                f'?includeMultiChainCurrencies=false', headers=headers) as response:
    #             response = await response.json()
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.poloniex.com/currencies/'
                                   f'?includeMultiChainCurrencies=false', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        print("Закончил полонех 2")
        return None

    chain_rename = {
        'ETH': 'ERC20',
        'AVAX C-Chain': 'AVAXC',
        'CHILIZ': 'CHZ',
        'TRX': 'TRC20',
        'BSC': 'BEP20',
        'BNB': 'BEP2',
        'MATICPOLY': 'MATIC',
        'APT': 'APTOS'
    }

    try:
        poloniex_status = dict()
        for value in response:
            key = list(value.keys())
            if value.get(key[0])['walletDepositState'] == 'ENABLED':
                deposit = True
            else:
                deposit = False
            if value.get(key[0])['walletWithdrawalState'] == 'ENABLED':
                withdrawal = True
            else:
                withdrawal = False
            if value.get(key[0])['blockchain'] in chain_rename:
                chain = chain_rename[value.get(key[0])['blockchain']]
            else:
                chain = value.get(key[0])['blockchain']
            poloniex_status.update({key[0]: {chain: [deposit, withdrawal, float(value.get(key[0])['withdrawalFee'])]}})
        return poloniex_status
    except (AttributeError, TypeError, KeyError):
        print("Закончил полонех 3")
        return None

async def bitget_chain():
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get('https://api.bitget.com/api/spot/v1/public/currencies', headers=headers) as response:
    #             response = await response.json()
    # except (ssl.SSLError, ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.bitget.com/api/spot/v1/public/currencies', headers=headers) as response:
                response = await response.json()
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        print("Закончил битгет 2")
        return None

    chain_rename = {
        'Polygon': 'MATIC',
        'C-Chain': 'C-CHAIN',
        'Optimism': 'OPTIMISM',
        'ArbitrumOne': 'ARBITRUM',
        'CoreDAO': 'CORE',
        'FONSmartChain': 'FON',
        'Klaytn': 'KLAY',
        'ChilizChain': 'CHZ',
        'Moonbeam': 'GLMR',
        'IoTeX': 'IOTX',
        'OnomyProtocol': 'NOM',
        'XDCNetworkXDC': 'XDC',
        'Aptos': 'APTOS',
        'Cardano': 'ADA',
        'ABBCCoin': 'ABBC',
        'stacks': 'STX',
        'Astar': 'ASTR',
        'ThetaToken': 'THETA',
        'THORChain': 'RUNE',
        'REINetwork': 'REI',
        'Ontology': 'ONT',
        'Elrond': 'EGLD',
        'FIOProtocol': 'FIO',
        'Helium': 'HNT',
        'NEARProtocol': 'NEAR',
        'CFXeSpace': 'CFX',
        'Arweave': 'AR',
        'Kusama': 'KSM',
        'Harmony': 'ONE',
        'AcalaToken': 'ACALA',
        'Solar': 'SOLAR',
        'MetisToken': 'METIS',
        'X-Chain': 'X-CHAIN',
        'Telos': 'TLOS',
        'Terra': 'LUNA',
        'SyscoinNEVM': 'NEVM',
        'WEMIXMainnet': 'WEMIX',
        'Fantom': 'FTM',
        'Osmosis': 'OSMO',
        'PocketNetwork': 'POKT',
        'Symbol': 'XYM',
        'CronosChain': 'CRO',
        'ArbitrumNova': 'ARBNOVA'
    }

    try:
        bitget_status = dict()
        for value in response['data']:
            bitget_status.update({value.get('coinName'): {}})
            for value_ in value.get('chains'):
                if value_.get('chain') in chain_rename:
                    chain = chain_rename[value_.get('chain')]
                else:
                    chain = value_.get('chain')
                if value_.get('rechargeable') == 'true':
                    deposit = True
                else:
                    deposit = False
                if value_.get('withdrawable') == 'true':
                    withdrawal = True
                else:
                    withdrawal = False
                bitget_status[value.get('coinName')].update({chain: [deposit, withdrawal,
                                                                     float(value_.get('withdrawFee'))]})
        return bitget_status
    except (AttributeError, TypeError, KeyError):
        print("Закончил битгет 3")
        return None

chain_status = {
    'binance': binance_chain,
    'huobi': huobi_chain,
    'bybit': bybit_chain,
    'kucoin': kucoin_chain,
    'gateio': gateio_chain,
    'mexc': mexc_chain,
    'okx': okx_chain,
    'whitebit': whitebit_chain,
    'poloniex': poloniex_chain,
    'bitget': bitget_chain
}

async def binance_qty(traiding_pair):
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get(f'https://api.binance.com/api/v3/depth?symbol={traiding_pair}', headers=headers) \
    #                 as response:
    #             response = await response.json()
    #             return response
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.binance.com/api/v3/depth?symbol={traiding_pair}', headers=headers) \
                    as response:
                response = await response.json()
                return response
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        return None

async def huobi_qty(traiding_pair):
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get(f'https://api.huobi.pro/market/depth?symbol='
    #                                f'{traiding_pair.lower()}&type=step0', headers=headers) as response:
    #             response = await response.json()
    #             response = response.get('tick')
    #             return response
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.huobi.pro/market/depth?symbol='
                                   f'{traiding_pair.lower()}&type=step0', headers=headers) as response:
                response = await response.json()
                response = response.get('tick')
                return response
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        return None

async def bybit_qty(traiding_pair):
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get(f'https://api.bybit.com/spot/v3/public/quote/depth?symbol='
    #                                f'{traiding_pair}&limit=5', headers=headers) as response:
    #             response = await response.json()
    #             response = response.get('result')
    #             return response
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.bybit.com/spot/v3/public/quote/depth?symbol='
                                   f'{traiding_pair}&limit=5', headers=headers) as response:
                response = await response.json()
                response = response.get('result')
                return response
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        return None

async def kucoin_qty(traiding_pair):
    traiding_pair = traiding_pair.replace('USDT', '')
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get(f'https://api.kucoin.com/api/v1/market/orderbook/level2_20?symbol='
    #                                f'{traiding_pair}-USDT', headers=headers) as response:
    #             response = await response.json()
    #             response = response.get('data')
    #             return response
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.kucoin.com/api/v1/market/orderbook/level2_20?symbol='
                                   f'{traiding_pair}-USDT', headers=headers) as response:
                response = await response.json()
                response = response.get('data')
                return response
    except (ssl.SSLError, aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        return None

async def gateio_qty(traiding_pair):
    traiding_pair = traiding_pair.replace('USDT', '')
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get(f'https://api.gateio.ws/api/v4/spot/order_book?currency_pair='
    #                                f'{traiding_pair}_USDT', headers=headers) as response:
    #             response = await response.json()
    #             return response
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.gateio.ws/api/v4/spot/order_book?currency_pair='
                                   f'{traiding_pair}_USDT', headers=headers) as response:
                response = await response.json()
                return response
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        return None

async def mexc_qty(traiding_pair):
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get(f'https://api.mexc.com/api/v3/depth?symbol={traiding_pair}', headers=headers) \
    #                 as response:
    #             response = await response.json()
    #             return response
    # except (ssl.SSLError, ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.mexc.com/api/v3/depth?symbol={traiding_pair}', headers=headers) \
                    as response:
                response = await response.json()
                return response
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        return None

async def okx_qty(traiding_pair):
    traiding_pair = traiding_pair.replace('USDT', '')
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get(f'https://www.okx.com/api/v5/market/books-lite?instId='
    #                                f'{traiding_pair}-USDT', headers=headers) as response:
    #             response = await response.json(encoding='utf-8', content_type='text/plain')
    #             if response.get('data') is not None:
    #                 response = response.get('data')[0]
    #                 return response
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://www.okx.com/api/v5/market/books-lite?instId='
                                   f'{traiding_pair}-USDT', headers=headers) as response:
                response = await response.json(encoding='utf-8', content_type='text/plain')
                if response.get('data') is not None:
                    response = response.get('data')[0]
                    return response
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        return None

async def whitebit_qty(traiding_pair):
    traiding_pair = traiding_pair.replace('USDT', '')
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get(f'https://whitebit.com/api/v4/public/orderbook/'
    #                                f'{traiding_pair}_USDT?limit=100&level=0', headers=headers) as response:
    #             response = await response.json()
    #             return response
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://whitebit.com/api/v4/public/orderbook/'
                                   f'{traiding_pair}_USDT?limit=100&level=0', headers=headers) as response:
                response = await response.json()
                return response
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        return None

async def poloniex_qty(traiding_pair):
    traiding_pair = traiding_pair.replace('USDT', '')
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get(f'https://poloniex.com/public?command=returnOrderBook&currencyPair=USDT_'
    #                                f'{traiding_pair}&depth=1', headers=headers) as response:
    #             response = await response.json()
    #             return response
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://poloniex.com/public?command=returnOrderBook&currencyPair=USDT_'
                                   f'{traiding_pair}&depth=1', headers=headers) as response:
                response = await response.json()
                return response
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        return None

async def bitget_qty(traiding_pair):
    try:
    #     connector = ProxyConnector.from_url(choice(proxy_list))
    #     async with aiohttp.ClientSession(connector=connector) as session:
    #         async with session.get(f'https://api.bitget.com/api/spot/v1/market/depth?symbol={traiding_pair}'
    #                                f'_SPBL&type=step0&limit=10', headers=headers) as response:
    #             response = await response.json()
    #             response = response.get('data')
    #             return response
    # except (ConnectionResetError, ConnectionRefusedError, aiohttp_socks.ProxyTimeoutError,
    #         aiohttp_socks.ProxyError, aiohttp_socks.ProxyConnectionError, asyncio.exceptions.TimeoutError):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.bitget.com/api/spot/v1/market/depth?symbol={traiding_pair}'
                                   f'_SPBL&type=step0&limit=10', headers=headers) as response:
                response = await response.json()
                response = response.get('data')
                return response
    except (aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientConnectorError,
            asyncio.exceptions.TimeoutError):
        return None


quantity = {
    'binance': binance_qty,
    'huobi': huobi_qty,
    'bybit': bybit_qty,
    'kucoin': kucoin_qty,
    'gateio': gateio_qty,
    'mexc': mexc_qty,
    'okx': okx_qty,
    'whitebit': whitebit_qty,
    'poloniex': poloniex_qty,
    'bitget': bitget_qty
}

async def url(cex_name, traiding_pair):
    traiding_pair = traiding_pair.replace('USDT', '')
    link = {
        'binance': f'https://www.binance.com/ru-UA/trade/{traiding_pair}_USDT?theme=dark&type=spot',
        'huobi': f'https://www.huobi.com/ru-ru/exchange/{traiding_pair.lower()}_usdt',
        'bybit': f'https://www.bybit.com/uk-UA/trade/spot/{traiding_pair}/USDT',
        'kucoin': f'https://www.kucoin.com/ru/trade/{traiding_pair}-USDT?spm=kcWeb.B1homepage.Header4.1',
        'gateio': f'https://www.gate.io/trade/{traiding_pair}_USDT',
        'mexc': f'https://www.mexc.com/ru-RU/exchange/{traiding_pair}_USDT?_from=header',
        'okx': f'https://www.okx.com/ru/trade-spot/{traiding_pair.lower()}-usdt',
        'whitebit': f'https://whitebit.com/ua/trade/{traiding_pair}-USDT?tab=open-orders&type=spot',
        'poloniex': f'https://poloniex.com/spot/{traiding_pair}_USDT',
        'bitget': f'https://www.bitget.com/en/spot/{traiding_pair}USDT_SPBL?type=spot'
    }
    result = link.get(cex_name)
    return result

fees = {
    'binance': 0.999,
    'huobi': 0.998,
    'bybit': 0.999,
    'kucoin': 0.999,
    'gateio': 0.998,
    'mexc': 0.998,
    'okx': 0.999,
    'whitebit': 0.999,
    'poloniex': 0.9985,
    'bitget': 0.999
}

async def comparison_allEN():
    cex_name = ['binance', 'huobi', 'bybit', 'kucoin', 'gateio', 'mexc', 'okx', 'whitebit', 'poloniex', 'bitget']
    cex_list = list()
    cex_chain = list()

    for func in cex_name:
        cex_list_result = await cex_func.get(func)()
        cex_chain_result = await chain_status.get(func)()
        if isinstance(cex_list_result and cex_chain_result, dict):
            cex_list.append(cex_list_result)
            cex_chain.append(cex_chain_result)
        else:
            cex_name.remove(func)

    price_filter = dict()

    for i in range(len(cex_list)):
        for i_ in range(i + 1, len(cex_list)):
            price1 = cex_list[i]
            price2 = cex_list[i_]
            for crypto1 in price1:
                for crypto2 in price2:
                    if crypto1 == crypto2 and crypto1 not in black_list:
                        if price1.get(crypto2)[1] < price2.get(crypto2)[0]:
                            price_high = price2.get(crypto2)[0]
                            price_low = price1.get(crypto2)[1]
                            if crypto_settings.get("admin")["percent"] < (
                                    (price_high - price_low) / price_low) * 100 <= 50:
                                price_filter.update({crypto1: [cex_name[i], cex_name[i_]]})
                        elif price1.get(crypto2)[0] > price2.get(crypto2)[1]:
                            price_high = price1.get(crypto2)[0]
                            price_low = price2.get(crypto2)[1]
                            if crypto_settings.get("admin")["percent"] < (
                                    (price_high - price_low) / price_low) * 100 <= 50:
                                price_filter.update({crypto1: [cex_name[i_], cex_name[i]]})
    chain_filter = list()

    for traiding_pair in price_filter:
        values_list = price_filter.get(traiding_pair)
        crypto = traiding_pair.replace('USDT', '')
        chain = cex_chain[cex_name.index(values_list[0])]
        chain_ = cex_chain[cex_name.index(values_list[1])]
        if crypto in chain and crypto in chain_:
            keys = list(chain.get(crypto).keys())
            keys_ = list(chain_.get(crypto).keys())
            for key in keys:
                if isinstance(chain.get(crypto)[key][2], float) and chain.get(crypto)[key][1]:
                    if key in keys_:
                        if chain_.get(crypto)[key][0]:
                            chain_filter.append([traiding_pair, values_list[0], values_list[1], key,
                                                 chain.get(crypto)[key][2]])

    for value in chain_filter:
        amount = await quantity.get(value[1])(value[0])
        amount_ = await quantity.get(value[2])(value[0])
        if amount is not None and amount_ is not None:
            if 'asks' in amount and 'bids' in amount_:
                amount = amount['asks']
                amount_ = amount_['bids']
                if amount is not None and amount_ is not None:
                    l = min(len(amount), len(amount_))
                    qty, qty_ = list(), list()
                    price, price_ = list(), list()
                    for i in range(l):
                        if float(amount[i][0]) < float(amount_[i][0]):
                            qty.append(float(amount[i][1]))
                            qty_.append(float(amount_[i][1]))
                            price.append(float(amount[i][0]))
                            price_.append(float(amount_[i][0]))
                    if len(qty) > 0 and len(qty_) > 0:
                        print("Я сделал 3")
                        min_qty = min(sum(qty), sum(qty_))
                        min_price = min(price)
                        max_price = max(price)
                        avg_price = (min_price + max_price) / 2
                        min_price_ = min(price_)
                        max_price_ = max(price_)
                        avg_price_ = (min_price_ + max_price_) / 2
                        fee = value[4]
                        profit = min_qty * fees.get(value[1])
                        profit_usd = min_qty * avg_price
                        profit_ = (profit - fee) * fees.get(value[2])
                        profit_usd_ = profit_ * avg_price_
                        if profit_usd_ > profit_usd:
                            print("Я сделал 4")
                            total_profit = ((profit_usd_ - profit_usd) / profit_usd) * 100
                            total_profit = round(total_profit, 2)
                            if total_profit > crypto_settings.get("admin")["percent"]:
                                print("Я сделал 5")
                                markup = types.InlineKeyboardMarkup()
                                btn1 = types.InlineKeyboardButton(value[1].capitalize(),
                                                                  url=f'{await url(value[1], value[0])}')
                                btn2 = types.InlineKeyboardButton(value[2].capitalize(),
                                                                  url=f'{await url(value[2], value[0])}')
                                markup.add(btn1, btn2)
                                await bot.send_message(chat_id=chat_id, text=(f'🔥 {value[0]}\n'
                                        f'\n'
                                        f'💰BUY {value[1].capitalize()}: \n'
                                        f'Price: {str(format(min_price, ".12f").rstrip("0"))} -'
                                        f' {str(format(max_price, ".12f").rstrip("0"))} $\n'
                                        f'Volume: {round(profit, 2)} {value[0].replace("USDT", "")} -'
                                        f' {round(profit_usd, 2)} USDT\n'
                                        f'\n'
                                        f'💰SELL {value[2].capitalize()}:\n'
                                        f'Price: {str(format(max_price_, ".12f").rstrip("0"))} -'
                                        f' {str(format(min_price_, ".12f").rstrip("0"))}$ \n'
                                        f'Volume: {round(profit_, 2)} {value[0].replace("USDT", "")} -'
                                        f' {round(profit_usd_, 2)} USDT\n'
                                        f'\n'
                                        f'🍿Profit: {total_profit} % - {round(profit_usd_ - profit_usd, 2)} USDT\n'
                                        f'\n'
                                        f'✅Chain: {value[3]} \n'
                                        f'✅Commission: {value[4]} {value[0].replace("USDT", "")}\n'),
                                           reply_markup=markup)
    print("Я сделал 6")
    global run_status
    run_status = 'ended'
    await bot.send_message(chat_id, text=f'End of search.')

async def comparison_allRU():
    cex_name = ['binance', 'huobi', 'bybit', 'kucoin', 'gateio', 'mexc', 'okx', 'whitebit', 'poloniex', 'bitget']
    cex_list = list()
    cex_chain = list()

    for func in cex_name:
        cex_list_result = await cex_func.get(func)()
        cex_chain_result = await chain_status.get(func)()
        if isinstance(cex_list_result and cex_chain_result, dict):
            cex_list.append(cex_list_result)
            cex_chain.append(cex_chain_result)
        else:
            cex_name.remove(func)

    price_filter = dict()

    for i in range(len(cex_list)):
        for i_ in range(i + 1, len(cex_list)):
            price1 = cex_list[i]
            price2 = cex_list[i_]
            for crypto1 in price1:
                for crypto2 in price2:
                    if crypto1 == crypto2 and crypto1 not in black_list:
                        if price1.get(crypto2)[1] < price2.get(crypto2)[0]:
                            price_high = price2.get(crypto2)[0]
                            price_low = price1.get(crypto2)[1]
                            if crypto_settings.get("admin")["percent"] < (
                                    (price_high - price_low) / price_low) * 100 <= 50:
                                price_filter.update({crypto1: [cex_name[i], cex_name[i_]]})
                        elif price1.get(crypto2)[0] > price2.get(crypto2)[1]:
                            price_high = price1.get(crypto2)[0]
                            price_low = price2.get(crypto2)[1]
                            if crypto_settings.get("admin")["percent"] < (
                                    (price_high - price_low) / price_low) * 100 <= 50:
                                price_filter.update({crypto1: [cex_name[i_], cex_name[i]]})

    chain_filter = list()

    for traiding_pair in price_filter:
        values_list = price_filter.get(traiding_pair)
        crypto = traiding_pair.replace('USDT', '')
        chain = cex_chain[cex_name.index(values_list[0])]
        chain_ = cex_chain[cex_name.index(values_list[1])]
        if crypto in chain and crypto in chain_:
            keys = list(chain.get(crypto).keys())
            keys_ = list(chain_.get(crypto).keys())
            for key in keys:
                if isinstance(chain.get(crypto)[key][2], float) and chain.get(crypto)[key][1]:
                    if key in keys_:
                        if chain_.get(crypto)[key][0]:
                            chain_filter.append([traiding_pair, values_list[0], values_list[1], key,
                                                 chain.get(crypto)[key][2]])

    for value in chain_filter:
        amount = await quantity.get(value[1])(value[0])
        amount_ = await quantity.get(value[2])(value[0])
        if amount is not None and amount_ is not None:
            if 'asks' in amount and 'bids' in amount_:
                amount = amount['asks']
                amount_ = amount_['bids']
                if amount is not None and amount_ is not None:
                    l = min(len(amount), len(amount_))
                    qty, qty_ = list(), list()
                    price, price_ = list(), list()
                    for i in range(l):
                        if float(amount[i][0]) < float(amount_[i][0]):
                            qty.append(float(amount[i][1]))
                            qty_.append(float(amount_[i][1]))
                            price.append(float(amount[i][0]))
                            price_.append(float(amount_[i][0]))
                    if len(qty) > 0 and len(qty_) > 0:
                        min_qty = min(sum(qty), sum(qty_))
                        min_price = min(price)
                        max_price = max(price)
                        avg_price = (min_price + max_price) / 2
                        min_price_ = min(price_)
                        max_price_ = max(price_)
                        avg_price_ = (min_price_ + max_price_) / 2
                        fee = value[4]
                        profit = min_qty * fees.get(value[1])
                        profit_usd = min_qty * avg_price
                        profit_ = (profit - fee) * fees.get(value[2])
                        profit_usd_ = profit_ * avg_price_
                        if profit_usd_ > profit_usd:
                            total_profit = ((profit_usd_ - profit_usd) / profit_usd) * 100
                            total_profit = round(total_profit, 2)
                            if total_profit > crypto_settings.get("admin")["percent"]:
                                markup = types.InlineKeyboardMarkup()
                                btn1 = types.InlineKeyboardButton(value[1].capitalize(),
                                                                  url=f'{await url(value[1], value[0])}')
                                btn2 = types.InlineKeyboardButton(value[2].capitalize(),
                                                                  url=f'{await url(value[2], value[0])}')
                                markup.add(btn1, btn2)
                                await bot.send_message(chat_id=chat_id, text=(f'🔥 {value[0]}\n'
                                        f'\n'
                                        f'💰Покупка {value[1].capitalize()}: \n'
                                        f'Цена: {str(format(min_price, ".12f").rstrip("0"))} -'
                                        f' {str(format(max_price, ".12f").rstrip("0"))} $\n'
                                        f'Объём: {round(profit, 2)} {value[0].replace("USDT", "")} -'
                                        f' {round(profit_usd, 2)} USDT\n'
                                        f'\n'
                                        f'💰Продажа {value[2].capitalize()}:\n'
                                        f'Цена: {str(format(max_price_, ".12f").rstrip("0"))} -'
                                        f' {str(format(min_price_, ".12f").rstrip("0"))}$ \n'
                                        f'Объём: {round(profit_, 2)} {value[0].replace("USDT", "")} -'
                                        f' {round(profit_usd_, 2)} USDT\n'
                                        f'\n'
                                        f'🍿Профит: {total_profit} % - {round(profit_usd_ - profit_usd, 2)} USDT\n'
                                        f'\n'
                                        f'✅Сеть: {value[3]} \n'
                                        f'✅Комиммия сети: {value[4]} {value[0].replace("USDT", "")}\n'),
                                           reply_markup=markup)
    global run_status
    run_status = 'ended'
    await bot.send_message(chat_id, text=f'Конец поиска.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
