import pandas as pd
from pathlib import Path
from utils.data_work import preprocess_tasks_set, get_all_bot_commands
from utils.task_extractor import TaskExtractor
from tasks.open_card import prepare_dataset, get_open_card_task_response

# data = pd.read_csv(str(Path().absolute().joinpath('data').joinpath('tasks.csv')), sep=';')
# data = data.set_index('task').T.to_dict('list')
# normalized_tasks_set = preprocess_tasks_set(data)
# main_extractor = TaskExtractor(normalized_tasks_set)
main_extractor = get_all_bot_commands()
extractors = {'open_card': TaskExtractor(prepare_dataset()), 'get_tasks': 'https://dev.greendatasoft.ru/#/registry/Task/'}


def analyze_message(message_text):
	code_response = main_extractor.extract_tasks(message_text)
	response = 'Ты мне написал: {0}, из этого я выделил следущее: {1}\n\n'.format(message_text, code_response)
	
	if code_response != '':
		if code_response in extractors:
			inside_extractor = extractors[code_response]
			if code_response == 'open_card':
				task_response = get_open_card_task_response(inside_extractor, message_text)
				return response + task_response
			if code_response == 'get_tasks':
				task_response = inside_extractor
				return response + task_response
		else:
			return 'Я увидел команду {0}, но не знаю что с ней делать :( '.format(code_response)
	else:
		return 'Ничего не понял, но все меняется'

