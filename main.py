from database import Topic, config
from aiogram import executor, types
from screenshot import take_screenshot
import requests
import xml.etree.ElementTree as ET
from aiogram.bot.api import API_URL
import time
import threading
from misc import dp, bot
from config_settings import CHAT_ID, B_TEXT, M_TEXT, SKIP_UPDATES, IU_UPDATE
from handlers import *

def find_news():
    items = []
    try:
        root = ET.fromstring(requests.get(config.get('main', 'rss_url')).content)
    except requests.exceptions.ConnectionError:
        return []
    for item in root.findall('.//channel/item'):
        link, title = item.find('link').text, item.find('title').text
        ext_id = link.split('.')[-1].split('/')[0]
        if not Topic.select().where(Topic.ext_id == ext_id):
            items.append({"title": title, "link": link})
            Topic.create(title=title, link=link, ext_id=ext_id)
        else:
            Topic.update(title=title, link=link).where(Topic.ext_id == ext_id)
    return items


class Worker(threading.Thread):
    def __init__(self, find_news, bot, take_screenshot_func):
        super(Worker, self).__init__()
        self.find_news = find_news
        self.bot = bot
        self.take_screenshot = take_screenshot_func

    def run(self):
        while True:
            for i in self.find_news():
                key = types.InlineKeyboardMarkup()
                key.add(types.InlineKeyboardButton(text=f"{B_TEXT}", url=i['link']))
                if self.take_screenshot(i['link']):
                    photo = open('attachement.png', 'rb')
                    self.bot.send_photo(
                        photo=photo,
                        caption=f"{M_TEXT} <a href='{i['link']}'>{i['title']}</a>",
                        parse_mode='html',
                        reply_markup=key
                    )
                else:
                    self.bot.send_message(chat_id=CHAT_ID,
                                          text=f"<a href='{i['link']}'>{M_TEXT}</a>",
                                          disable_web_page_preview=False,
                                          parse_mode='html',
                                          reply_markup=key)
            time.sleep(int(IU_UPDATE))

def main():
    executor.start_polling(
        dispatcher=dp,
        skip_updates=SKIP_UPDATES
    )

if __name__ == "__main__":
    main()
    worker = Worker(find_news, bot, take_screenshot)
    worker.start()
