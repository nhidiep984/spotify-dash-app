import spotipy
import spotipy.util as util

class SpotifyAuthorization():
    def __init__(self):
        self.username = 'nhidiep874'
        self.scope = 'user-library-read playlist-modify-public playlist-read-private'
        self.CLIENT_ID = '80024097aaa84b32a7bf60f5e6cce91d'
        self.CLIENT_SECRET = '428c1cd5425f496c8d7aff27d7980fa3'

    def authorize(self):
        token = util.prompt_for_user_token(username=self.username,
                                           scope=self.scope,
                                           client_id=self.CLIENT_ID,
                                           client_secret=self.CLIENT_SECRET,
                                           redirect_uri='http://127.0.0.1:8050/')
        sp = spotipy.Spotify(auth=token)
        return sp






