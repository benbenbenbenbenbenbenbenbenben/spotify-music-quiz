# Spotify Music Quiz
Use your Spotify playlists to challenge others to see who has the best music knowledge. Uses Spotipys lightweight Python library for accessing Spotify's Web API.

## Table of Contents
- [Requirements](#requirements)
- [Setup](#setup)
- [Spotify](#spotify)
- [Start App](#start-app)
- [Server](#server)
- [File Structure](#file-structure)
- [Help](#help)
- [Resources](#resources)

## Requirements
- Spotify Account
- PC/Server To Run App

## Setup

### Python
1. Ensure you have Python version 3 installed (If not download and install)
```bash
$ python3 -V
```
2. In terminal window goto your working folder (Documents etc) create a Python 3 virtual environment using this command:
```bash
$ python3 -m venv quiz
```
3. Now "activate" the environment
```bash
$ source quiz/bin/activate
```
4. Install required packages
```bash
$ pip install Flask spotipy
``` 

### Clone Repository
1. Download latest source code from github repository
```bash
git clone https://github.com/benbenbenbenbenbenbenbenbenben/spotify-music-quiz.git
cd spotify-music-quiz
```

### Spotify Developer Account
1. Login to Spotify Developer: https://developer.spotify.com/dashboard
2. Register a Spotify App: https://developer.spotify.com/documentation/general/guides/app-settings/#register-your-app
    1. Note down Client ID and Client Secret
3. Add Redirect URIs for authenticating users. If just running on local machine use **1.**, otherwise if deploying to server also add **2.**
    1. http://127.0.0.1:5001/user
    2. http://YOUR.SERVER.IP:5001/user

### Edit App Settings
Open **auth2.py** and edit the following from above. Uncomment/comment Redirect URI based on if using local or server :
```py
SPOTIPY_CLIENT_ID = 'Client ID'
SPOTIPY_CLIENT_SECRET = 'Client Secret'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:5001/user'
# SPOTIPY_REDIRECT_URI = 'http://YOUR.SERVER.IP:5001/user'
```

## Server Setup
*Optional: Skip if running locally.*

Open **app.py** and uncomment the last line so app runs on servers IP and not localhost.
```py
if __name__ == "__main__":
    # app.run(debug=True, port=5001)
    app.run(host='0.0.0.0', port=5001)
```

## Spotify
Create your music quiz playlists.
App will find any playlist starting with "**Trivia - **"

IMAGE

## Start App
Ensure virtual environment is active and in spotify-music-quiz folder:
```bash
python app.py
```
IMAGE

## Additional Server Setup
*Optional: Skip if running locally.*

### Bash Start Script
nano start-spotify-quiz.sh
Change directory path **/home/user/python/quiz** to where you initiated the python venv.
```bash
#!/usr/bin/env bash
source /home/user/python/quiz/bin/activate
python /home/user/python/quiz/spotify-music-quiz/app.py
```
### Run As A Service
sudo nano /etc/systemd/system/spotify-music-quiz.service
```bash
[Unit]
Description=Spotify Music Quiz
After=network.target

[Service]
WorkingDirectory=/home/user/python/3py/spotify-music-quiz
ExecStart=/home/user/python/3py/spotify-music-quiz/start-spotify-quiz.sh
Restart=always

[Install]
WantedBy=multi-user.target
```
### Service Commands
| Command        | Description  |
| ------------- |:-------------|
| systemctl daemon-reload                           | Restarts Daemon after editing service file |
| sudo systemctl start spotify-music-quiz.service   | Start Service     |
| sudo systemctl status spotify-music-quiz.service  | Status of Service |
| journalctl -f                                     | Get Services Logs     |

## File Structure
Project Files:

| Filename        | Description             |
| ------------- |:-------------|
| app.py            | Main file contains Flask Routes                   | 
| auth2.py          | Authenticates user when making Spotify API Calls      | 
| player.py         | Additional Playback Functions        |
| playlists.py      | Additional Playlist Functions        |
| quiz.py           | Read/write JSON files, create new quiz      |
| tracks.py         | Gets a new random song from chosen category      |
| Logs Folder       | Active and Previous Quiz information stored in JSON |
| Static Folder     | Web files |
| Templates Folder  | Contains html content served by Jinja |
| README.md         | Information about this app |

## Help
- Read through this guide

## Resources
Spotipy - https://github.com/plamere/spotipy
Spotify - https://developer.spotify.com/documentation/web-api/reference/
Vibrant JS - https://jariz.github.io/vibrant.js/
Bootstrap - https://getbootstrap.com/
