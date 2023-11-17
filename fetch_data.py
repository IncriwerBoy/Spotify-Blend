import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import re
from datetime import datetime


def format_date(input_date):
    try:
        # Try to parse the input date
        parsed_date = datetime.strptime(input_date, "%Y-%m-%d")
    except ValueError:
        try:
            # If parsing fails, try to parse with the format "%Y-%m"
            parsed_date = datetime.strptime(input_date, "%Y-%m")
        except ValueError:
            try:
                # If parsing fails again, try to parse with the format "%Y"
                parsed_date = datetime.strptime(input_date, "%Y")
            except ValueError:
                # If parsing fails for all formats, set the date to the first day of the year
                parsed_date = datetime.strptime(input_date + '-01-01', "%Y-%m-%d")

    # Format the date as "yyyy-mm-dd"
    formatted_date = parsed_date.strftime("%Y-%m-%d")
    
    return formatted_date


def fetch(client_id, client_secret, playlist_code, playlist_code2):
    # Connecting with Spotify API
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    #providing playlist link
    playlist_dict = sp.playlist(playlist_code)
    playlist_dict2 = sp.playlist(playlist_code2)

    num_songs = playlist_dict['tracks']['total']
    num_songs2 = playlist_dict2['tracks']['total']

    #fetching data for first playlist
    album_list = []
    song_list = []
    release_date_list = []
    artists_list = []

    tracks = playlist_dict['tracks']
    items = tracks['items']
    offset = 0
    i=0
    while i < num_songs:
        song = items[i-offset]['track']['name']
        album = items[i-offset]['track']['album']['name']
        release_date = items[i-offset]['track']['album']['release_date']
        if not release_date.startswith('0000'):
            release_date = format_date(release_date)
            artists = [k['name'] for k in items[i-offset]['track']['artists']]
            artists = ','.join(artists)
            album_list.append(album)
            song_list.append(song)
            release_date_list.append(release_date)
            artists_list.append(artists)

        if (i+1)%100 == 0:
            tracks = sp.next(tracks)
            items = tracks['items']
            offset = i+1
        i += 1


    #fetching data for second playlist
    album_list2 = []
    song_list2 = []
    release_date_list2 = []
    artists_list2 = []

    tracks = playlist_dict2['tracks']
    items = tracks['items']
    offset = 0
    i=0
    while i < num_songs2:
        song = items[i-offset]['track']['name']
        album = items[i-offset]['track']['album']['name']
        release_date = items[i-offset]['track']['album']['release_date']
        if not release_date.startswith('0000'):
            release_date = format_date(release_date)
            artists = [k['name'] for k in items[i-offset]['track']['artists']]
            artists = ','.join(artists)
            album_list2.append(album)
            song_list2.append(song)
            release_date_list2.append(release_date)
            artists_list2.append(artists)

        if (i+1)%100 == 0:
            tracks = sp.next(tracks)
            items = tracks['items']
            offset = i+1
        i += 1
    
    #creating dataframe
    df1 = pd.DataFrame()
    df1['Name'] = song_list
    df1['Artist'] = artists_list
    df1['Album'] = album_list
    df1['Release_date'] = release_date_list

    df2 = pd.DataFrame()
    df2['Name'] = song_list2
    df2['Artist'] = artists_list2
    df2['Album'] = album_list2
    df2['Release_date'] = release_date_list2
        
    return df1, df2