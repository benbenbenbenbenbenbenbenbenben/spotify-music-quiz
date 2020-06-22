def get_category(spotify, category):
    me = spotify.me()
    playlists = spotify.user_playlists(me['id'])
    for playlist in playlists['items']:
        if (f'Trivia - {category}') in playlist['name']:
            return playlist['uri']
    else:
        return 'None'

def get_categories(spotify):
    me = spotify.me()
    categories = []
    playlists = spotify.user_playlists(me['id'])
    for playlist in playlists['items']:
        if 'Trivia' in playlist['name']:
            categories.append(playlist['name'].strip('Trivia - '))
    return categories