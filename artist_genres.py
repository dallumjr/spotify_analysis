import spotipy
import csv
import utility_functions as uf
from spotipy.oauth2 import SpotifyOAuth
from collections import OrderedDict

scope = "user-library-read"
email = uf.get_email_from_input()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, username=email))
tg = uf.get_details_for_saved_tracks(sp, uf.map_genres_to_track_id)
uf.create_analysis_csv(tg,'genre_analysis')
