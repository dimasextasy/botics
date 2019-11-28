import os
from utils.data_work import preprocess_tasks_set
import requests


def prepare_dataset():
	auth_url = os.environ['AUTH_URL']
	auth_data = {
		'j_username': os.environ['GREENDATA_USER'],
		'j_password': os.environ['GREENDATA_PWD']
	}
	get_uriki_url = os.environ['GET_URIKI_URL']
	with requests.Session() as session:
		session.post(auth_url, auth_data)
		response = session.get(get_uriki_url)
	ur_clients = response.json()
	clients_dic = {}
	for client in ur_clients['content']:
		clients_dic[client['values']['ID']['value']] = [client['values']['NAME']['value'].replace('"', '')]
	# data = pd.read_csv('urici.csv', sep=';')
	# data = data.set_index('task').T.to_dict('list')
	normalized_clients_set = preprocess_tasks_set(clients_dic)
	return normalized_clients_set


def get_open_card_task_response(inside_extractor, message_text):
	client_id = inside_extractor.extract_tasks(message_text)
	url_base = 'https://dev.greendatasoft.ru/#/card/'
	full_url = url_base + str(client_id)
	return full_url