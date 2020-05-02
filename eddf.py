import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import spotipy
import pandas as pd
import spotipy.util as util



username = 'nhidiep874'
scope = 'user-library-read playlist-modify-public playlist-read-private'
CLIENT_ID = '80024097aaa84b32a7bf60f5e6cce91d'
CLIENT_SECRET = '428c1cd5425f496c8d7aff27d7980fa3'

token = util.prompt_for_user_token(username=username,
                                   scope=scope,
                                   client_id=CLIENT_ID,
                                   client_secret=CLIENT_SECRET,
                                   redirect_uri='https://127.0.0.1:8050/')

sp = spotipy.Spotify(auth=token)


def search_playlist_tracks(uri):
    playlist = sp.user_playlist(username, uri)
    tracks_df = pd.DataFrame([(track['track']['id'],
                               track['track']['artists'][0]['name'],
                               track['track']['name'])
                              for track in playlist['tracks']['items']],
                             columns=['id', 'artist', 'name'])
    return tracks_df


def set_audio_features(id):
    track = sp.track(id)

    features = sp.audio_features(id)

    name = track['name']
    album = track['album']['name']
    artist = track['album']['artists'][0]['name']
    release_date = track['album']['release_date']
    length = track['duration_ms']
    popularity = track['popularity']

    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']

    track = [name, album, artist, release_date, length, popularity, danceability, acousticness, danceability, energy,
             instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
    return track


def get_audio_features(tracks_df):
    tracks = []
    for id in range(len(tracks_df['id'])):
        track_id = tracks_df['id'][id]
        track = set_audio_features(track_id)
        tracks.append(track)
    return tracks


def get_tracks_df(tracks):
    df = pd.DataFrame(tracks,
                      columns=['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability',
                               'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness',
                               'speechiness', 'tempo', 'time_signature'])
    df = df.reindex(df['name'])
    return df


tracks_dfs = search_playlist_tracks('spotify:playlist:1srBwh26KeLWVeRzTxbGLy')
tracks_features = get_audio_features(tracks_dfs)
tracks_data = get_tracks_df(tracks_features)
print(tracks_data)

