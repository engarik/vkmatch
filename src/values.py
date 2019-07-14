import os
import webbrowser
import time

api_version = 5.95
client_id = 7016529
debug = False


def get_token():
    if os.path.isfile('token.txt'):
        f = open('token.txt', 'r')
        if int(time.time()) - int(f.readline().rstrip('\n')) < 84600:
            print('Token was found')
            return f.readline()
        else:
            f.close()
            os.remove('token.txt')
            return get_token()
    else:
        scope = 'friends,groups,photos'
        redirect_uri = 'https://oauth.vk.com/blank.html'

        webbrowser.open(
            'https://oauth.vk.com/authorize?client_id=%d&display=page&redirect_uri=%s&scope=%s&response_type=token&v=%d' % (
                client_id, redirect_uri, scope, api_version))
        print('Copy token from address bar and input it here:')
        res = input()

        f = open('token.txt', 'w')
        f.write(str(int(time.time())) + '\n' + res)
        return res


token = get_token()
