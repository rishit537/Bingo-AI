import time
import spotipy
import webbrowser
import random
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv("./.env")

# Account details
username = os.environ.get("SPOTIFY_USERNAME")
clientID = os.environ.get("SPOTIFY_CLIENT_ID")
clientSecret = os.environ.get("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.environ.get("SPOTIFY_REDIRECT_URI")
spotifyObject = {}


# Auth
def auth(username, clientID, clientSecret, redirect_uri):
    if username and clientID and clientSecret:
        oauth_object = spotipy.SpotifyOAuth(
            clientID,
            clientSecret,
            redirect_uri,
            scope="playlist-read-private playlist-read-collaborative user-read-playback-state user-modify-playback-state user-read-currently-playing streaming",
        )
        token_dict = oauth_object.get_access_token()
        token = token_dict["access_token"]
        globals()["spotifyObject"] = spotipy.Spotify(auth=token)
    else:
        print("Error: Spotify credentials not found in .env file")


def searchSpotify(
    track="", artist="", album="", playlist="", shuffle=None, repeat=None
):
    try:
        auth(username, clientID, clientSecret, redirect_uri)
    except Exception as e:
        print(f"Spotify Authentication failed. Error: {e}")
        return
    # Case 1: Search for specific track
    if track:
        query_parts = []
        if track:
            query_parts.append(f"{track}")
        if artist:
            query_parts.append(f"{artist}")
        if album:
            query_parts.append(f"{album}")
        query = " ".join(query_parts)
        results = spotifyObject.search(q=query, limit=20, type="track")
        tracks = results["tracks"]["items"]
        filtered = [t for t in tracks if t["name"].lower() == track.lower()]
        if not filtered:
            filtered = tracks

        # Sort by popularity
        try:
            best_match = filtered[0]
            webbrowser.open(best_match["uri"])
            if repeat:
                spotifyObject.repeat(state="track")
            return [best_match["name"], best_match["artists"][0]["name"]]
        except Exception as e:
            print("Track not found.")
            return

    # Case 2: Search for album
    elif album:
        if shuffle == None:
            shuffle = False
        query = f"{album} {artist}" if artist else f"{album}"
        results = spotifyObject.search(q=query, limit=5, type="album")
        albums = results["albums"]["items"]
        if albums:
            album_data = albums[0]
            context_uri = album_data["uri"]

            start_playback_context(context_uri, shuffle=shuffle, repeat=repeat)
            # webbrowser.open(album_data["external_urls"]["spotify"])
            # return [album_data["name"], album_data["artists"][0]["name"]]
        else:
            print("Album not found.")
            return

    # Case 3: Search for playlist
    elif playlist:
        playlists = spotifyObject.current_user_playlists()
        for p in playlists["items"]:
            pl_words = playlist.lower().split(" ")
            if playlist.lower() in p["name"].lower():
                pl_uri = p["uri"]
                start_playback_context(
                    context_uri=pl_uri, shuffle=shuffle, repeat=repeat
                )
                print(f"Opened your playlist: {p['name']}")
                return [p["name"], "Your Library"]
            else:
                for word in pl_words:
                    if word in p["name"].lower():
                        pl_uri = p["uri"]
                        start_playback_context(
                            context_uri=pl_uri, shuffle=shuffle, repeat=repeat
                        )
                        print(f"Opened your playlist: {p['name']}")
                        return [p["name"], "Your Library"]
        else:
            print("Playlist not found")

    # Case 4: Search for artist
    elif artist:
        results = spotifyObject.search(q=f"{artist}", limit=5, type="artist")
        artists = results["artists"]["items"]
        if artists:
            artist_data = artists[0]
            artist_uri = artist_data["uri"]
            start_playback_context(
                context_uri=artist_uri, shuffle=shuffle, repeat=repeat
            )
            # webbrowser.open(artist_data["external_urls"]["spotify"])
            return [artist_data["name"]]
        else:
            print("Artist not found.")
            return

    elif (
        artist == ""
        and playlist == ""
        and album == ""
        and track == ""
        and (shuffle is not None or repeat is not None)
    ):
        if shuffle is not None:
            spotifyObject.shuffle(state=shuffle)
        if repeat is not None:
            if repeat:
                spotifyObject.repeat("context")
            else:
                spotifyObject.repeat("off")
    else:
        print("No valid input provided.")
        return


def start_playback_context(
    context_uri, device_id=None, retry=False, shuffle=None, repeat=None
):
    retryCount = 0
    try:
        offset = 0
        # 1. If shuffle==True, pick a random start track URI
        if shuffle is not None:
            if shuffle:
                if "album:" in context_uri:
                    data = spotifyObject.album_tracks(context_uri.split(":")[-1])
                    total = data["total"]
                elif "playlist:" in context_uri:
                    data = spotifyObject.playlist_items(context_uri.split(":")[-1])
                    total = data["total"]
                else:
                    total = 0

                if total > 0:
                    offset = random.randrange(total)
                else:
                    offset = 0
            else:
                offset = 0
            spotifyObject.shuffle(state=shuffle, device_id=device_id)

        if repeat:
            spotifyObject.repeat(state="context", device_id=device_id)
        spotifyObject.start_playback(
            device_id=device_id,
            context_uri=context_uri,
            offset=(
                {"position": offset}
                if ("album:" in context_uri or "playlist" in context_uri)
                else None
            ),
        )

    except spotipy.SpotifyException as e:
        # Oavoid an infinite loop
        if not retry and "NO_ACTIVE_DEVICE" in str(e) and retryCount <= 5:
            print("No active device found. Attempting to activate one...")
            webbrowser.open("spotify:")  # open the app
            time.sleep(3)
            devices = spotifyObject.devices()["devices"]
            if devices:
                device_id = devices[0]["id"]
                start_playback_context(
                    context_uri=context_uri,
                    device_id=device_id,
                    retry=True,
                    shuffle=shuffle,
                    repeat=repeat,
                )
                retryCount += 1
            else:
                print("Still no active device.")
        else:
            print(f"Playback failed: {e}")


# searchSpotify(playlist="purane gane", shuffle=True, repeat=True)
