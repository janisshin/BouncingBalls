# check out https://youtu.be/7J_qcttfnJA 

"""
Step 1: Log into Youtube
Step 2: Grab our liked videos
Step 3: Create a new playlist
Step 4: SEarch for the song
Step 5: Add this song into the new Spotify playlist
"""

import json
import requests
from secrets import spotify_user_id
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import youtube_dl


class CreatePlaylist:

	def __init__(self):
		self.user_id = spotify_user_id
		self.spotify_token = spotify_token
		self.youtube_client = self.get_youtube_client()
		self.all_song_info={}

	# Step 1: Log into Youtube
	def get_youtube_client(self):
		# copied from Youtub Data API
		# Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    
    # from Youtube Data API
    youtube_client = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    return youtube_client

    print(response)

	# Step 2: Grab our liked videos & creating a dictionary of important song information
	def get_liked_videos(self):
		request = self.youtube_client.videos().list(
			part="snippet,contentDetails,statistics",
        	myRating="like"
		)
		response = request.execute()

		# collect each vide and get important information
		for item in response["items"]:
			video_title = item["snippet"]
			youtube_url = "https://www.youtube.com/watch?v={}".format(item["id"])

			# use youtube_dl to collect the song name & artist name
			video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
			song_name = video["track"]
			artist = video["artist"]

			# save important info
			self.all_song_info[video_title]{
				"youtube_url":youtube_url,
				"song_name":song_name,
				"artist":artist,

				#add the uri to make fetching songs on Spotify easy
				"spotify_uri":self.get_spotify_uri(song_name, artist)

			}

	# Step 3: Create a new playlist
	def create_playlist(self):
		
		request_body = json.dumps({
			"name": "Youtube",
			"description": "All Liked Youtube Videos",
			"public":True
		})

		query = "https://api.spotify.com/v1/users/{user_id}/playlists".format(self.user_id)
		response = requests.post(
			query,
			data = request_body, 
			headers = {
				"Content-Type": "application/json",
				"Authorization": "Bearer {}".format(spotify_token)
			}

		)
		response_json = response.json()

		#playlist id
		return response_json["id"]

	# Step 4: Search for the song
	def get_spotify_uri(self, song_name, artist):
		
		query = "https://api.spotify.com/v1/search?q={}%20".format(## must be completed
			song_name,
			artist
		)
		response = requests.get(
			query,
			headers={
				"Content-Type": "application/json"
				"Authorization": "Bearer {}".format(spotify_token)

			}
		)
		response_json = response.json()
		songs = response_json["tracks"]["items"]

		# only use the first song
		uri = songs[0]["uri"]

		return uri



	# Step 5: Add this song into the new Spotify playlist
	def add_song_to_playlist(self):
		# populate our songs dictionary
		self.get_liked_videos()

		# collect all of uri
		uri = []
		for song, info in self.all_song_info.items():
			uris.append(info["spotify_uri"])

		#create a new playlist
		playlist_id = self.create_playlist()

		# add all songs into new playlist
		request_data = json.dumps(uris)
		query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

		response = requests.post(
			query,
			data=request_data,
			headers={
				"Content-Type": "application/json"
				"Authorization": "Bearer {}".format(self.spotify_token)
			}
		)
		response_json = response.json()
		return response_json
