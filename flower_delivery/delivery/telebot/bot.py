from config import TOKEN
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получение chat_id пользователя
    chat_id = update.effective_chat.id

    # Отправка chat_id обратно пользователю
    await context.bot.send_message(chat_id=chat_id, text=f'Your chat ID: {chat_id}')


async def main():
    # Создание приложения бота с использованием вашего токена
    application = ApplicationBuilder().token(TOKEN).build()

    # Добавление обработчика для команды /start
    application.add_handler(CommandHandler("start", start))

    # Запуск бота
    await application.run_polling()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
