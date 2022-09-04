import os
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_key = sp.current_user()["id"]
play_result = sp.user_playlists(user=user_key)
sp.user_playlist_create(user=user_key, name="test_playlist")
play_list_id = play_result["items"][0]["id"]

user_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL ="https://www.billboard.com/charts/hot-100/"

response = requests.get(f"{URL}/{user_date}")
contents = response.text
soup = BeautifulSoup(contents, "html.parser")
# print(soup.prettify())
# print(soup.title.getText())

all_titles = soup.find_all("h3", class_="a-no-trucate", id="title-of-a-story")
song_titles = [title.getText().strip() for title in all_titles]
# print(song_titles)

for song in song_titles:
    song_search_result = sp.search(q=song)
    track_id = song_search_result["tracks"]["items"][0]["id"]
    sp.playlist_add_items(play_list_id, [track_id], position=None)














# auth_url = "https://accounts.spotify.com/api/token"
# data = {
#     "grant_type": "client_credentials",
#     "client_id": client_id,
#     "client_secret": client_secret,
# }
#
# auth_response = requests.post(auth_url, data=data)
# access_token = auth_response.json().get("access_token")
# print(access_token)

# spotify = spotify.SpotifyBase(client_credentials_manager=SpotifyClientCredentials())
