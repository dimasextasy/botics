import pandas as pd
from pathlib import Path
from utils.data_work import preprocess_tasks_set, get_all_bot_commands
from tasks.open_card import get_open_card_task_response

url_get_tasks = 'https://dev.greendatasoft.ru/#/registry/Task/881611'
main_extractor = get_all_bot_commands()
response_funcs = {'open_card': '', 'get_tasks': url_get_tasks}


def analyze_message(message_text):
	code_response = main_extractor.extract_tasks(message_text)
	response = 'Ты мне написал: {0}, из этого я выделил следущее: \n\n'.format(message_text)
	if code_response != '':
		if code_response in response_funcs:
			inside_response = response_funcs[code_response]
			if code_response == 'open_card':
				task_response = response + get_open_card_task_response(message_text)
				return task_response
			if code_response == 'get_tasks':
				response += 'Открыть задачи \n'
				task_response = response + inside_response
				return task_response
		else:
			return 'Я увидел команду {0}, но не знаю что с ней делать :('.format(code_response)
	else:
		return 'Я не знаю такой команды'

