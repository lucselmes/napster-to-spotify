from warnings import WarningMessage
import requests
from credentials import username_napster, password_napster, napster_api_key, napster_api_secret, spotify_client_id, spotify_client_secret
from urllib.parse import urlencode
import json
import os

def get_user_info_napster(api_key: str, api_secret: str, username: str, password: str) -> dict:
    """
    Retrieves Napster user info given username and password
  
    Parameters:
    string: api key of app
    string: api secret of app
    string: Napster username
    string: Napster password
  
    Returns:
    dict: dict object containing user info
    """
    url = "https://api.napster.com/oauth/token"
    data = {
        "username": username,
        "password": password,
        "grant_type": "password"
    }
    auth = (api_key, api_secret)

    response = requests.post(url, data=data, auth=auth)

    return response.json()

def get_playlists_napster(access_token: str, limit: str = '10', offset: str = '5') -> dict:
    """
    Retrieves a list of playlists belong to Napster user. 
    
    Must use Napster user's access token which can be retrieved using get_access_tokens_napster().
    It is recommended that you use the limit and offset parameters to incrementally get all the data. 
    Current version does not support sorting
  
    Parameters:
    string: Napster access token
    str: number (in string) limiting amount of playlists returned
    str: offsets --
  
    Returns:
    dict: dictionary containing a info on all playlists in user's library    
    """
    url = "https://api.napster.com/v2.2/me/library/playlists?limit="+ limit +"&offset="+ offset
    headers = {
        "Authorization": "Bearer "+access_token
    }

    response = requests.get(url, headers=headers)

    return response.json()

def get_playlists_info_napster(napster_playlists):
    """
    returns list of playlists with only id and name specified
    
    """
    all_playlists_info = []

    # Get playlist names and ids
    for playlist in napster_playlists:

        # In the future we could grab the image of the playlist too in order to show the end user the png
        all_playlists_info.append((playlist['id'], playlist['name'])) 

    return all_playlists_info

def get_all_playlists_napster(access_token: str) -> list:
    """
    Retrieves the list of all playlists in a given user's library

    Parameters:
    string: access token for napster user

    Returns:
    list: all playlists shape -> [dict]
    """

    napster_playlists_info = []
    offset = 0
    while True:

        more_info = get_playlists_napster(access_token=access_token, limit='20', offset=str(offset))['playlists']

        if more_info == []:
            break

        napster_playlists_info = napster_playlists_info + more_info
        offset += 20

    return napster_playlists_info

def select_specified_playlists(selection: list, playlists_essential_info: list):
    """
    Returns only the info of the specified playlists
    """

    selected_playlists_info = []

    # Select only those playlists that we want to move over
    for playlist in playlists_essential_info:
        if playlist[1] in selection:
            selected_playlists_info.append(playlist)

    return selected_playlists_info

def get_playlist_tracks_napster(access_token: str, playlist_id: str, limit: str = '10') -> dict:
    """
    Retrieves the tracks of given Napster user's playlist. Playlist specified by playlist_id

    Must use Napster user's access token which can be retrieved using get_access_tokens_napster().
  
    Parameters:
    string: Napster access token
    string: Napster playlist id
  
    Returns:
    dict: dictionary containing a list of tracks in given playlist
    """

    url = "https://api.napster.com/v2.2/me/library/playlists/"+playlist_id+"/tracks?limit="+limit
    headers = {
        "Authorization": "Bearer "+access_token
    }

    response = requests.get(url, headers=headers)

    return response.json()

def get_track_info_napster_to_spotify(track: dict) -> dict:
    """
    Retrieves necessary track info from napster track dictionary object in order to find the track on spotify.

    Parameters:
    dict: dictionary representing napster track

    Returns:
    dict: dictionary containing relevant track info (track name, artist name and album name)
    """

    track_info = {
        'name': track['name'],
        'artist': track['artistName'],
        'album': track['albumName']
    }

    return track_info

def search_track_spotify(oauth_token: str, track_name: str, artist_name: str, album_name: str, limit: str = '20'):
    """
    Searches for track on spotify based off of track name and artist name

    Parameters:
    str: spotify oauth token
    str: track name
    str: artist name
    str: album name
    str: limit

    Returns:
    list[obj]: list of results (possibly top result)
    """

    query = urlencode({
        'q': track_name + " " + artist_name + " " + album_name,
        'type': 'track',
        'limit': limit
    })

    url = 'https://api.spotify.com/v1/search?'+ query
    headers = {
        "Authorization": "Bearer "+oauth_token,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    return response.json()

def get_spotify_uris_from_napster_playlist(napster_access_token: str, spotify_access_token: str, playlist_id: str):
    """
    Returns a list that represents a napster playlist in terms of its tracks' spotify uris

    Parameters:


    Returns:
    list: list representing track uris
    """
    uri_list = []
    tracks_not_found = []

    playlist = get_playlist_tracks_napster(access_token=napster_access_token, playlist_id=playlist_id, limit='100')

    for track in playlist['tracks']:
        track_info = get_track_info_napster_to_spotify(track)

        # Search for song on spotify and append its uri to uri list
        search_result = search_track_spotify(spotify_access_token, track_info['name'], track_info['artist'], track_info['album'], limit='20')["tracks"]["items"]
        
        # If search didn't return anything
        if search_result == []:
            tracks_not_found.append({
                'track': track_info['name'],
                'artist': track_info['artist'],
                'album': track_info['album']
            })
            continue
        
        track_uri = search_result[0]['uri']
        uri_list.append(track_uri)

    return (uri_list, tracks_not_found)

def create_playlist_spotify(oauth_token: str, playlist_name: str, playlist_description: str = "Luc has created you", public_status: str = False):
    """
    Creates spotify playlist given playlist_name, playlist_description, and public/private status.

    Parameters:
    str: spotify oauth token
    str: playlist name
    str: playlist description
    bool: public status

    Returns:
    requests.Response: .Response object containing playlist metadata
    """

    username = get_spotify_user_name(oauth_token)

    endpoint = username + "/playlists"

    url = "https://api.spotify.com/v1/users/" + endpoint
    request_body = json.dumps({
        "name": playlist_name,
        "description": playlist_description,
        "public": public_status
    })

    headers = {
        "Authorization": "Bearer "+oauth_token,
        "Content-Type": "application/json",
    }

    response = requests.post(url, data=request_body, headers=headers)

    return response.json()

def add_tracks_spotify(oauth_token: str, uri_list: list[str], playlist_id: str) -> requests.Response:
    """
    Adds tracks to a spotify playlist given a list of spotify track uris and a spotify playlist id.

    Maximum size of uri_list is 100, any tracks past that will be ignored by request.

    Parameters:
    str: spotify user's oauth token
    list[string]: List of uris of spotify tracks
    string: id of target spotify playlist 

    Returns:
    requests.Response: .Response object containing snapshot_id for the spotify playlist
    """
    if len(uri_list) > 100:
        print("Uri list is over 100 tracks, add_tracks_spotify() only processes 100 tracks at a time. Overflow will be ignored.")

    url = "https://api.spotify.com/v1/playlists/"+playlist_id+"/tracks"
    request_body = json.dumps({
        "uris": uri_list
    })
    headers = {
        "Authorization": "Bearer "+oauth_token,
        "Content-Type": "application/json"
    }

    response = requests.post(url, data=request_body, headers=headers)

    return response.json()

def create_spotify_playlist_from_napster_playlist_info(napster_access_token, spotify_access_token, selected_playlists):
    """
    Creates spotify playlists corresponding to those specified by selected_playlists
    """

    
    playlists_snapshots = []
    not_found = {'playlists': []}

    for playlist in selected_playlists:
        napster_playlist_id = playlist[0]
        playlist_name = playlist[1]

        uri_list, tracks_not_found = get_spotify_uris_from_napster_playlist(napster_access_token, spotify_access_token, napster_playlist_id)

        # Save the not found tracks to provide info to end user
        if tracks_not_found != []:
            not_found['playlists'].append({
                'type': 'playlist',
                'name': playlist_name,
                'tracks': tracks_not_found
            })

        # Create spotify playlist
        spotify_playlist = create_playlist_spotify(spotify_access_token, playlist_name)
        playlist_id = spotify_playlist['id']

        # Add tracks to spotify playlist
        spotify_playlist_snap = add_tracks_spotify(spotify_access_token, uri_list, playlist_id)
        playlists_snapshots.append(spotify_playlist_snap)

    return not_found

def read_from_txt(relative_file_path: str) -> list:
    """
    from txt relative file path, returns list containing contents of each line 
    """
    playlists = []

    f = open(relative_file_path, "r")
    for playlist_name in f:
        playlists.append(playlist_name.split("\n")[0])
    f.close()

    return playlists

def get_spotify_user_name(spotify_access_token: str):
    """
    From spotify oauth token get username
    """

    url = "https://api.spotify.com/v1/me"
    headers = {
        "Authorization": f"Bearer {spotify_access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(
        url=url,
        headers=headers
    )

    return response.json()["id"]