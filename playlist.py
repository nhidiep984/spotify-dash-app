from auth import SpotifyAuthorization
from app import username
import pandas as pd


class Playlist:
    def __init__(self, uri):
        self.uri = uri


    def search_playlist_tracks(self, sp):
        playlist = sp.user_playlist(username, playlist_id=self.uri)
        #tracks = playlist['tracks']['items']
        tracks_df = pd.DataFrame([(track['track']['id'],
                                   track['track']['artists'][0]['name'],
                                   track['track']['name'])
                                  for track in playlist['tracks']['items']],
                                 columns=['id', 'artist', 'name'])
        return tracks_df
