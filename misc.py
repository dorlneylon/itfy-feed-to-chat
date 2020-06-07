import logging
from aiogram import Bot, Dispatcher
from config_settings import TOKEN

bot = Bot(
    token=TOKEN
)
dp = Dispatcher(
    bot=bot
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)