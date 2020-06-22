from flask import Flask, request, render_template, redirect, url_for
from player import *
from playlists import *
from tracks import *
import spotipy
from auth2 import check_auth
import time
import random
import os

app = Flask(__name__)
app_title = 'Music Quiz'

# Home Page
@app.route('/')
def index():
    # Check User Logged In
    auth = check_auth(request)
    if auth.startswith('<html'):
        return auth
    else:
        sp = spotipy.Spotify(auth)
        user = sp.me()
        user_name = user['display_name']
        user_avatar = user['images'][0]['url']
    # Check Existing Quiz
    active_quiz = read_quiz_file('active-quiz')
    if active_quiz:
        return render_template('base.html', app_title=app_title, contents='main.html', data=active_quiz['quiz']['name'], user=[user_name,user_avatar])
    else:
        return render_template('base.html', app_title=app_title, contents='main.html')

# Logout
@app.route('/logout')
def logout():
    if os.path.exists('.spotipyoauthcach'):
        os.remove('.spotipyoauthcach')
    else:
        print("No Cache Found")

@app.route('/quiz-history')
def history():
    auth = check_auth(request)
    if auth.startswith('<a href='):
        return auth
    else:
        sp = spotipy.Spotify(auth)
        user = sp.me()
        user_name = user['display_name']
        user_avatar = user['images'][0]['url']
        try:
            history = read_quiz_file('previous-quizzes')
            return render_template('base.html', app_title=app_title, data=history, contents='history.html', user=[user_name,user_avatar])
        except:
            return redirect(url_for('index'))


@app.route('/quiz-history/<id>', methods=["DELETE"])
def history_id(id):
    if request.method == "DELETE":
        history = read_quiz_file('previous-quizzes')
        history.pop(int(id))
        write_quiz_file('previous-quizzes', history)
        return f'Success, deleted {id}'

@app.route('/results')
def results():
    auth = check_auth(request)
    if auth.startswith('<a href='):
        return auth
    else:
        sp = spotipy.Spotify(auth)
        user = sp.me()
        user_name = user['display_name']
        user_avatar = user['images'][0]['url']
        try:
            active_quiz = read_quiz_file('active-quiz')
            return render_template('base.html', app_title=app_title, contents='results2.html', player='player.html', data=active_quiz, user=[user_name,user_avatar])
        except:
            return redirect(url_for('index'))

@app.template_filter('ctime')
def timectime(s):
    return time.ctime(s)

@app.route('/quiz')
def quiz():
    auth = check_auth(request)
    if auth.startswith('<a href='):
        return auth
    else:
        sp = spotipy.Spotify(auth)
        user = sp.me()
        user_name = user['display_name']
        user_avatar = user['images'][0]['url']
        if 'category' in request.args:
            pl_name = request.args.get('category')
            pl_id = get_category(sp, pl_name)
            # song =  get_random_song(sp, pl_id)
            return render_template('base.html', app_title=app_title, contents='quiz.html', player='player.html', category_name=pl_name, category_id=pl_id, user=[user_name,user_avatar])#, json=song
        elif 'next' in request.args:
            pl_id = request.args.get('next')
            return get_random_song(sp, pl_id)

@app.route('/categories')
def categories():
    auth = check_auth(request)
    if auth.startswith('<a href='):
        return auth
    else:
        sp = spotipy.Spotify(auth)
        user = sp.me()
        user_name = user['display_name']
        user_avatar = user['images'][0]['url']
        # Start New Quiz If Name Provided
        if 'name' in request.args:
            new_quiz(request.args['name'])
        # Check Active Quiz Exists
        active_quiz = read_quiz_file('active-quiz')
        if not active_quiz:
            return redirect(url_for('index'))

        categories = get_categories(sp)
        return render_template('base.html', app_title=app_title, contents='categories.html', data=categories, user=[user_name,user_avatar])


@app.route('/player/<action>')
def player_action(action):                         
    auth = check_auth(request)
    if auth.startswith('<a href='):
        return auth
    else:
        sp = spotipy.Spotify(auth)
        if action == 'play_pause':
            state = play_pause(sp)
            return state
        elif action == 'pause':
            sp.pause_playback()
            return json.dumps({'state':'paused'})
        elif action == 'volume':
            volume = sp.volume(int(request.args['volume']))
            return 'Volume Adjusted'
        else:
            return 'Player Action Not Defined'
        
@app.route('/devices/<action>')
def devices(action):
    print(action)
    auth = check_auth(request)
    if auth.startswith('<a href='):
        return auth
    else:
        sp = spotipy.Spotify(auth)
        # Return List Of Devices
        if action == 'list':
            print(sp.devices())
            return sp.devices()
        # Transfer Playback To Another Device
        elif action == 'transfer':
            sp.transfer_playback(request.args['device'], force_play=True)
            return json.dumps({'state':'true'})
        else:
            return 'Devices Action Not Defined'

@app.route('/song/<songId>')
def song(songId):  
    print(f'Song Requested: {songId}')
    auth = check_auth(request)
    if auth.startswith('<a href='):
        return auth
    else:
        sp = spotipy.Spotify(auth)
        song_offset = random.randint(30,60)*1000
        # Queue Song - Returns None
        try:
            sp.start_playback(uris=[f'spotify:track:{songId}'], position_ms=song_offset)
        except:
            print("Exception: No active device")
            devices = sp.devices()
            sp.start_playback(device_id=devices['devices'][0]['id'],uris=[f'spotify:track:{songId}'], position_ms=song_offset)
        # Ensure Song Is Playing - returns too many false positives, may need to wait x ms
        # check_song = sp.current_playback()
        # if check_song['item']['id'] == songId:
        #     return json.dumps({'state':'playing'})
        # else: 
        #     return json.dumps({'state':'not-playing'})

        # Ensure Song Is Playing
        return json.dumps({'state':'playing'})

@app.route('/user')
def user():  
    auth = check_auth(request)
    if auth.startswith('<a href='):
        return auth
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
    # app.run(host='0.0.0.0', port=5001)
