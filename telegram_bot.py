# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pandas as pd
import os
from utils.data_work import preprocess_tasks_set
from utils.task_extractor import TaskExtractor
from tasks.open_card import prepare_dataset

updater = Updater(token=os.environ["TELEGRAM_TOKEN"]) # Токен API к Telegram
dispatcher = updater.dispatcher
data = pd.read_csv('tasks.csv', sep=';')
data = data.set_index('task').T.to_dict('list')
normalized_tasks_set = preprocess_tasks_set(data)
extractor = TaskExtractor(normalized_tasks_set)
extractors = {'open_card': TaskExtractor(prepare_dataset())}


# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, пообщайся со мной)')

def textMessage(bot, update):
	code_response = extractor.extract_tasks(update.message.text)
	response = 'Ты мне написал: {0}, из этого я выделил следущее: {1}'.format(update.message.text, code_response)
	bot.send_message(chat_id=update.message.chat_id, text=response)
	inside_extractor = extractors[code_response]
	client_id = inside_extractor.extract_tasks(update.message.text)
	url_base = 'https://dev.greendatasoft.ru/#/card/'
	full_url = url_base + str(client_id)
	bot.send_message(chat_id=update.message.chat_id, text=full_url)


def main():
	# Хендлеры
	start_command_handler = CommandHandler('start', startCommand)
	text_message_handler = MessageHandler(Filters.text, textMessage)
	# Добавляем хендлеры в диспетчер
	dispatcher.add_handler(start_command_handler)
	dispatcher.add_handler(text_message_handler)
	# Начинаем поиск обновлений
	updater.start_polling(clean=True)
	# Останавливаем бота, если были нажаты Ctrl + C
	updater.idle()
	


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		exit()