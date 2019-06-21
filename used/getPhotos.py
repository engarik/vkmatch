import os
import requests
import vk
import webbrowser

token = '5b81d97ca72dfee9ed6c4a459a819b9816a715435e7d697462e749a329083a6158929e76527bd1ef40e6f'
session = vk.Session(token)
api = vk.API(session)


def get_id(name):
    return api.utils.resolveScreenName(screen_name=name, v=5.80)['object_id']


print("Name - 1 ID - 2")
if int(input()) == 1:
    userId = get_id(input())
else:
    userId = int(input())

userIdStr = str(userId)

response = api.photos.getAll(owner_id=userId, extended=0, count=200, v=5.80)
photos = response['items']
count = int(response['count'])
print(count)

try:
    os.mkdir("images/" + userIdStr)
except FileExistsError:
    pass

if count > 200:
    rem = count
    n = 0
    while rem > 0:
        if rem > 200:
            response = api.photos.getAll(owner_id=userId, extended=0, offset=200 * n, count=200, v=5.80)
            num = 200
        else:
            response = api.photos.getAll(owner_id=userId, extended=0, offset=200 * n, count=rem, v=5.80)
            num = rem

        photos = response['items']
        for i in range(num):
            p = requests.get(photos[i]['photo_130'])
            out = open("images/" + userIdStr + "/img_" + str(i + 200 * n) + ".jpg", "wb")
            out.write(p.content)
            out.close()
        rem -= 200
        n += 1
else:
    for i in range(count):
        p = requests.get(photos[i]['photo_130'])
        out = open("images/" + userIdStr + "/img_" + str(i) + ".jpg", "wb")
        out.write(p.content)
        out.close()
