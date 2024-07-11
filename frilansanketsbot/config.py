from aiogram import Bot
from database import Database

# Инициализация базы данных
database = Database("database.db")

# Токен вашего Telegram бота
BOT_TOKEN = '7412139975:AAFELwqvbEwOwr-CwCfxEGOmhOU__ea4MoU'

# Инициализация Telegram бота
bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
