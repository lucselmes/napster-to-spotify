from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import string
from credentials import spotify_client_id, spotify_client_secret
import time
from utils import *

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

app = Flask(__name__)

app.secret_key = get_random_string(16)
app.config['SESSION_COOKIE_NAME'] = 'playlist converter cookie'
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external=True))

@app.route('/getTracks')
def getTracks():
    # Get spotify access token
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        redirect(url_for("login", _external=False))

    spotify_access_token = token_info['access_token']

    print("1")

    # Get napster access token
    napster_access_token = get_user_info_napster(napster_api_key, napster_api_secret, username_napster, password_napster)['access_token']
    
    print("2")

    # Get all playlists
    napster_playlists = get_all_playlists_napster(napster_access_token)

    print("3")

    # Get important playlist info
    napster_playlists_info = get_playlists_info_napster(napster_playlists)

    print("4")

    # #############################
    # TODO: 
    #  Display napster playlists to user for them to choose which playlists get migrated
    #
    # ############################

    # Check if selected_playlists.txt exists
    exists = os.path.isfile("./selected_playlists.txt")

    if exists:
        # Select our playlists from the list of available playlists
        selection = read_from_txt("selected_playlists.txt")
        selected_playlists = select_specified_playlists(selection, napster_playlists_info)

    else:
        selected_playlists = napster_playlists_info

    # Create spotify playlists and capture the tracks that weren't found
    not_found = create_spotify_playlist_from_napster_playlist_info(napster_access_token, spotify_access_token, selected_playlists)

    return not_found

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=spotify_client_id,
        client_secret=spotify_client_secret,
        redirect_uri=url_for('redirectPage', _external=True),
        scope='playlist-modify-private playlist-modify-public'
    )