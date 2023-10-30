# napster-to-spotify
Tool to convert napster playlists to spotify playlists

Step 1: Clone repo to local 

Step 2: Install python3

Step 3: python3 setup.py install

Step 4: Copy paste info below into a file called credentials.py, keep the file in the root

```
# You have to hard code this for now, down the road will integrate implicit oauth
username_napster = "your username here"
password_napster = "your password here"

# Retrieved from Napster developer platform (create an app)
napster_api_key = ""
napster_api_secret = ""

# Retrieved from Spotify developer platform (create an app)
spotify_client_id = ""
spotify_client_secret = ""
```

Step 5 (Optional): If you wish to only import certain playlists to spotify, specify the different playlists by writing a playlist name per line.