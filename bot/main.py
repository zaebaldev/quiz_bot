import asyncio
import logging

from core.logger import configure_logging
from aiogram import Bot, Dispatcher
from core.config import settings
from routers import router

logger = logging.getLogger(__name__)
bot = Bot(str(settings.tg_bot.token))
dp = Dispatcher()


async def main():
    configure_logging()
    logger.info("Запуск бота...")
    dp.include_router(router)
    # Подключаем роутеры из модулей
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Получен сигнал на завершение работы")
    finally:
        logger.info("Программа завершена")
