import dash_table as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import spotipy
import pandas as pd
import spotipy.util as util
import plotly.graph_objs as go


external_stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheet)

username = 'nhidiep874'
scope = 'user-library-read playlist-modify-public playlist-read-private'
CLIENT_ID = '80024097aaa84b32a7bf60f5e6cce91d'
CLIENT_SECRET = '428c1cd5425f496c8d7aff27d7980fa3'

token = util.prompt_for_user_token(username,
                                   scope,
                                   client_id=CLIENT_ID,
                                   client_secret=CLIENT_SECRET,
                                   redirect_uri='http://127.0.0.1:8050/')

sp = spotipy.Spotify(auth=token)


def search_playlist_tracks(uri):
    playlist = sp.user_playlist(username, uri)
    tracks_df = pd.DataFrame([(track['track']['id'],
                               track['track']['artists'][0]['name'],
                               track['track']['name'])
                              for track in playlist['tracks']['items']],
                             columns=['id', 'artist', 'name'])
    return tracks_df


# tracks_df = search_playlist_tracks('spotify:playlist:1srBwh26KeLWVeRzTxbGLy')

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
    for i, id in enumerate(tracks_df['id']):
        track_id = tracks_df['id'][i]
        track = set_audio_features(track_id)
        tracks.append(track)
    return tracks


# tracks = get_audio_features(tracks_df)


def get_tracks_df(tracks):
    df = pd.DataFrame(tracks,
                      columns=['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability',
                               'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness',
                               'speechiness', 'tempo', 'time_signature'])

    return df


# df = get_tracks_df(tracks)


app.layout = html.Div(children=[
    html.Div(children='''
    Paste in Spotify Playlist URI'''),
    dcc.Input(id='uri', value='', type='text'),
    html.Button('Submit', type = 'submit', id='submit-button', n_clicks=0),
    html.Div(id='plot')

])


@app.callback(
    Output('plot', 'children'),
    [Input('uri', 'value')])

def display_graph(uri):
    if uri == '':
        return None

    tracks_df = search_playlist_tracks(uri)
    tracks = get_audio_features(tracks_df)
    df = get_tracks_df(tracks)

    trace_1 = go.Scatter(x=df.name, y=df['tempo'],
                         name='Tempo')
    layout = go.Layout(title='Tempo')
    fig = go.Figure(data=[trace_1], layout=layout)
    return dcc.Graph(
        id='plot',
        figure=fig)


if __name__ == '__main__':
    app.run_server(debug=True)
