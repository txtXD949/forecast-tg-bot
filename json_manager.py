import json


def new_chat(chat_id, city):
    with open('config.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    data[chat_id] = city

    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)


def get_all():
    with open('config.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def get_address(chat_id):
    with open('config.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data[chat_id]


def del_address(chat_id):
    with open('config.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    del data[str(chat_id)]

    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)
