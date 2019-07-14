import os

from src.values import api_version


def get_user_id(name, api):
    if len(name) == 10 and name.startswith('id'):
        id_res = int(name[2:])
    elif name.isnumeric():
        id_res = int(name)
    elif name.startswith('https://vk.com/'):
        if name.startswith('https://vk.com/id'):
            id_res = int(name[17:len(name)])
        else:
            id_res = api.users.get(user_ids=name[15:len(name)], v=api_version)[0]['id']
    else:
        id_res = api.users.get(user_ids=name, v=api_version)[0]['id']

    return id_res


try:
    os.mkdir("data\\")
    os.mkdir("data\\groups")
    os.mkdir("data\\users")
except FileExistsError:
    pass
