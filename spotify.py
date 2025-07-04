import json
import spotipy
import webbrowser

# Account details
username = "l5ev6fq0lfgkage92tkj9s3m4"
clientID = "44ca3b9fa0994177bdaeafa944741b3e"
clientSecret = "44733f7048c34dabb9ec1d3c7fb4ecf1"
redirect_uri = "http://127.0.0.1:9000"

# Auth
oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri)
token_dict = oauth_object.get_access_token()
token = token_dict["access_token"]
spotifyObject = spotipy.Spotify(auth=token)
user_name = spotifyObject.current_user()

# To print the response in readable format.
# print(json.dumps(user_name, sort_keys=True, indent=4))


def searchSong(song_name, artist_name=""):
    if artist_name:
        query = f"track:{song_name} artist:{artist_name}"
    else:
        query = song_name

    results = spotifyObject.search(q=query, limit=10, offset=0, type="track")
    tracks = results["tracks"]["items"]
    if not tracks:
        print("No matching track found.")
        return

    song = tracks[0]
    song_url = song["external_urls"]["spotify"]
    webbrowser.open(song_url)
    return [song["name"], song["artists"][0]["name"]]
