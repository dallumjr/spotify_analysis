import spotipy
from spotipy.oauth2 import SpotifyOAuth
import utility_functions as uf

scope = "user-library-read"
# perhaps analyze on a monthly or weekly scale

email = uf.get_email_from_input()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, username=email))
saved_tracks = uf.get_details_for_saved_tracks(sp, uf.create_feature_dict_row)
uf.create_analysis_csv(saved_tracks,'spotify_analysis')
print('Completed!')
