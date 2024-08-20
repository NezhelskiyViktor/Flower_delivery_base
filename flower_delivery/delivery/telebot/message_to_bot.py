import asyncio
from aiogram import Bot
import logging
from .config import TOKEN, BOT_ID

logging.basicConfig(level=logging.INFO)

# Глобальная переменная для хранения CHAT_ID
bot = Bot(token=TOKEN)

async def send_message_to_bot(text):

    try:
        await bot.send_message(BOT_ID, text)
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")


def send_message(text):
    asyncio.run(send_message_to_bot(text))

