import logging
import os

import telebot

import sheet


logger = logging.getLogger(__name__)
logging.basicConfig(filename='bot.log', encoding='utf-8', level=logging.INFO)


def get_token() -> str:
    token = os.getenv('BOT_TOKEN', '')
    if not token:
        raise ValueError('BOT_TOKEN is not set')
    return token


bot = telebot.TeleBot(get_token())


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    try:
        logging.info(f'got message "{message.text}" from user "{message.from_user.username}" ({message.from_user.id}) in chat {message.chat.id}')

        if message.text.startswith('/next'):
            dates = sheet.get_dates(sheet.download_sheet(), sheet.get_start_date())

            if dates:
                date_list = '\n'.join(map(lambda t: t.strftime('%d.%m.%Y'), dates))
                bot.send_message(message.chat.id, f'Можно собраться:\n{date_list}')
            else:
                bot.send_message(message.chat.id, f'Нет доступных дат в календаре.')

    except Exception as e:
        logging.warning(f'user error, user "{message.from_user.username}" ({message.from_user.id}) in chat {message.chat.id}: {e}')
        bot.send_message(message.chat.id, f'Ошибка.')


if __name__ == '__main__':
    bot.polling(non_stop=True, interval=1, long_polling_timeout=5)

