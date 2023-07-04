import re

def is_spotify_link(text):
    spotify_regex = r'^https?:\/\/open\.spotify\.com\/(track|album|playlist)\/[a-zA-Z0-9]+(\?[a-zA-Z0-9=_&]+)?$'
    match = re.match(spotify_regex, text)
    return bool(match)
def is_track_link(link):
    track_regex = r'^https?:\/\/open\.spotify\.com\/track\/[a-zA-Z0-9]+$'
    match = re.match(track_regex, link)
    return bool(match)

def is_spotify_playlist_link(link):
    pattern = r'^https:\/\/open.spotify.com\/playlist\/[a-zA-Z0-9]+$'
    return re.match(pattern, link) is not None
def is_youtube_playlist(link):
    playlist_regex = r"youtube\.com/playlist\?list="
    match = re.search(playlist_regex, link)
    return bool(match)