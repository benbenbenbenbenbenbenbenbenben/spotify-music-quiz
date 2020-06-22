import random
import json
from quiz import *

def get_random_song(spotify, pl_id):
    # Get Tracks
    response = spotify.playlist_tracks(pl_id, fields='items.track.artists,items.track.name,items.track.id, items.track.album')
    songs = response['items']
    random.shuffle(songs)

    # Get Used Tracks
    active_quiz = read_quiz_file('active-quiz')
    
    # Add Track to Active Quiz If Does Not Exist
    for category in active_quiz['quiz']['categories']:
        if category['category_id'] == pl_id:
            for song in songs:
                if not check_match(song, category['category_tracks']):
                    category['category_tracks'] = category['category_tracks'] + [song]
                    write_quiz_file('active-quiz', active_quiz)
                    return song
    else:
        # Get Playlist Name
        pl = spotify.playlist(pl_id)
        pl_name = pl['name'].strip('Trivia - ')
        active_quiz['quiz']['categories'] = active_quiz['quiz']['categories'] + [{'category_id': pl_id, 'category_name': pl_name, 'category_tracks': [songs[0]]}]
        write_quiz_file('active-quiz', active_quiz)
        return songs[0]


def check_match(song, array):
    for track in array:
        if song['track']['id'] == track['track']['id']: 
            return True
    return False
