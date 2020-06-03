import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from urllib.parse import urlparse
from pprint import pprint
import logging

class Spotify_Client:
    spotify_client = None

    def __init__(self):
        self.spotify_client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        self.logger = logging.getLogger('spotify_rythm_bot')
        self.logger.setLevel(logging.INFO)

    def _get_playlist_items(self, playlist_id):
        playlist_items = []
        offset = 0
        while True:
            response = self.spotify_client.playlist_tracks(playlist_id, offset=offset, fields='items.track.name,items.track.album.name,items.track.artists.name,total')
            offset = offset + len(response['items'])
            playlist_items += response['items']
            self.logger.info(f"{offset} / {response['total']}")

            if len(response['items']) == 0:
                break
        self.logger.info(f"Items found in playlist: {len(playlist_items)}")
        return playlist_items
    
    def _get_track_item(self, track_id):
        response = self.spotify_client.track(track_id)
        return [{"track": response}]


    def _try_url_parse(self, url):
        parsed = urlparse(url)
        tracklist = []
        if url.startswith("https://open.spotify.com/playlist/"):
            playlist_id = "spotify:playlist:" + parsed.path.split("/playlist/")[1]
            tracklist = self._get_playlist_items(playlist_id)
        elif url.startswith("https://open.spotify.com/track/"):
            track_id = parsed.path.split("/track/")[1]
            tracklist = self._get_track_item(track_id)
        return tracklist


    def parse_link(self, url):
        tracks = self._try_url_parse(url)
        rythm_bot_commands = []
        for track in tracks:
            song_name = track.get("track", {}).get("name", "")
            song_artist = track.get("track", {}).get("artists",[{}])[0].get("name", "")
            rythm_bot_commands.append(f"!play {song_name} - {song_artist}")
        return rythm_bot_commands
