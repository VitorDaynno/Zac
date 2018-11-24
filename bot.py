import telebot
from config.config import Config

config = Config()
bot = telebot.TeleBot(config.get_token_bot())
