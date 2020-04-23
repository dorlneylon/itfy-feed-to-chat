![Python test bot deployment](https://github.com/mowshon/itfy-feed-to-chat/workflows/Python%20test%20bot%20deployment/badge.svg)
## 🤖 Экспорт новых вопросов из Форума в Телеграм чат
#### 📢 Форум: [ITFY](https://itfy.org)

### Конфигурация бота
* Помыть руки в проточной воде, минумум 20 секунд (карантин)
* Изменить переменные в файле `config.ini` 

Необходимо изменить:
  * `token` ваш токен телеграм бота
  * `chat_id` ID телегам чата

### Запуск бота

```bash
pip install -r requirements.txt  # Установка необходимых пакетов
python main.py  # Запуск бота
```

# Использования бота

Новые вопосы из форума [ITFY](https://itfy.org) будут опубликованы в телеграм чат. 
