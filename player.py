import json

# Shows playing devices
def play_pause(spotify):
    state = spotify.current_playback()
    print(state)
    # Check player is Active not none
    if state:
        if state['is_playing']:
            print('paused')
            spotify.pause_playback()
            return json.dumps({'state':'paused'})
        else:
            print('resumed')
            spotify.start_playback()
            return json.dumps({'state':'playing'})
    # Play on any player
    else:
        devices = spotify.devices()
        if len(devices) > 0:
            spotify.start_playback(devices['devices'][0]['id'])
            return json.dumps({'state':'playing'})
        else:
            return json.dumps({'state':'no devices'})

def play_song(songId):
    spotify.start_playback(uris=[f'spotify:track:{songId}'])