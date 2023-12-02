import json
import os
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch


def get_client():
    # api_id, api_hash из JSON
    json_fname = 'API_AUTH.json'
    if not os.path.exists(json_fname):
        print(f'Ошибка чтения JSON: нет файла с именем {json_fname}')
        exit(1)

    json_dict = {}
    with open(json_fname, 'r') as f:
        try:
            json_dict = json.load(f)
        except json.JSONDecodeError as e:
            print(f'Ошибка чтения JSON: {e}')
            exit(1)

    if any(field not in json_dict.keys() for field in ('api_id', 'api_hash')):
        print('Ошибка чтения JSON: необходимы поля api_id, api_hash')
        exit(1)

    api_id = json_dict['api_id']
    api_hash = json_dict['api_hash']

    client = TelegramClient('session_name', api_id, api_hash)
    client.start()
    return client


def get_participants(client, entity_id: str):
    try:
        entity = client.get_entity(entity_id)

        participants = client(GetParticipantsRequest(
            entity, ChannelParticipantsSearch(''), offset=0, limit=200, hash=0))
        for person in participants.users:
            print(f'id={person.id}, name={person.name}')
    except Exception as e:
        print(f'Ошибка списка участников: {e}')
        exit(1)


def main():
    with open('ID.txt', 'r') as f:
        entity_id = f.readline().strip()
    
    client = get_client()
    get_participants(client, entity_id)