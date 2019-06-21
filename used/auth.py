import webbrowser

base_url = 'https://oauth.vk.com/authorize?client_id'
client_id = 7016529
scope = 'friends,photos,audio,video,wall,groups'
redirect_uri = 'https://oauth.vk.com/blank.html'

webbrowser.open(
    '%s=%d&display=page&redirect_uri=%s&scope=%s&response_type=token&v=5.95&state=123456' % (
        base_url, client_id, redirect_uri, scope))
