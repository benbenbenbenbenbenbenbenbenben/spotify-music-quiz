from flask import request, render_template
from spotipy import oauth2

SPOTIPY_CLIENT_ID = 'Client ID'
SPOTIPY_CLIENT_SECRET = 'Client Secret'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:5001/user'
# SPOTIPY_REDIRECT_URI = 'http://YOUR.SERVER.IP:5001/user'

SCOPE = 'user-library-read,user-read-playback-state,user-modify-playback-state'
CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )

def check_auth(request):
    access_token = ""
    token_info = sp_oauth.get_cached_token()
    # User Has Valid Auth Token
    if token_info:
        print("Found cached token!")
        access_token = token_info['access_token']
    # Else User Is Logging In
    else:
        url = request.url
        try:
            code = sp_oauth.parse_response_code(url)
            if code:
                print ("Found Spotify auth code in Request URL! Trying to get valid access token...")
                token_info = sp_oauth.get_access_token(code)
                access_token = token_info['access_token']
        except:
            print("No Auth code")

    if access_token:
        return access_token
    # No Token - User To Login
    else:
        print("Requesting User To Login")
        return render_template('login.html', app_title='Music Quiz', login_url=htmlForLoginButton())

def htmlForLoginButton():
    return sp_oauth.get_authorize_url()