import json


def save_json(file_name: str, data):
	with open(f'./data/{file_name}.json', 'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False)