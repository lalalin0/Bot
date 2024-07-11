# import asyncio
# from dribble import dribble
# from behance import \
#     send_message_withv  # Убедитесь, что функция send_message_withv определена в behance.py и корректно импортируется
#
#
# async def run_periodically(interval):
#     while True:
#         await send_message_withv()  # Убедитесь, что send_message_withv - это асинхронная функция
#         await dribble()
#         await asyncio.sleep(interval)
#
#
# # Основная асинхронная функция, которая запускает цикл
# async def main():
#     interval = 30 * 60  # 30 минут в секундах
#     await run_periodically(interval)
#
#
# # Запуск основного цикла событий
# if __name__ == "__main__":
#     print('Starting the bot...')
#     asyncio.run(main())

#
# import asyncio
# import logging
# from dribble import dribble
# from behance import send_message_withv
#
# # Настройка логирования
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#
#
# async def run_periodically(interval):
#     while True:
#         try:
#             await send_message_withv()
#             await dribble()
#         except Exception as e:
#             logging.error(f"Error occurred: {e}")
#         await asyncio.sleep(interval)
#
#
# async def main():
#     interval = 30 * 60  # 30 минут в секундах
#     await run_periodically(interval)
#
#
# if __name__ == "__main__":
#     logging.info("Starting the bot...")
#     asyncio.run(main())


import asyncio
from dribble import dribble
from behance import send_message_withv


async def run_periodically(interval):
    """Запускает функции парсинга и отправки сообщений с заданным интервалом."""
    while True:
        await send_message_withv()
        await dribble()
        await asyncio.sleep(interval)


# Основная асинхронная функция, которая запускает цикл
async def main():
    interval = 30 * 60  # 30 минут в секундах
    await run_periodically(interval)


# Запуск основного цикла событий
if __name__ == "__main__":
    asyncio.run(main())
