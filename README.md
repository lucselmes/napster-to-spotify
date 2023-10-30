# napster-to-spotify
Tool to convert napster playlists (no longer an illegal streaming service :D ) to spotify playlists.  

### Motivation
Decided to make this tool when I realized that napster had removed many of the songs from their streaming service that I liked listening to. Spotify's selection was better, but it would take forever to move my playlists over by hand, so I decided to automate it. Hoping this can be of use to someone else.

### Instructions

Step 1: Clone repo to local 

Step 2: Install python3

Step 3: Install requirements `>> pip install -r requirements.txt`

Step 4: To get going you'll need to fill out credentials.py, it looks like this: 

```
# You have to hard code this for now, down the road could integrate implicit oauth
username_napster = "your username here"
password_napster = "your password here"

# Retrieved from Napster developer platform (create an app)
napster_api_key = ""
napster_api_secret = ""

# Retrieved from Spotify developer platform (create an app)
spotify_client_id = ""
spotify_client_secret = ""
```

You'll need to fill this out with your own information. Some of this you need to get by creating a developer account here:  
[Napster Developer API](https://developer.prod.napster.com/)  
[Spotify Developer API](https://developer.spotify.com/)  

Step 4b (Optional): If you wish to only import certain playlists to spotify, specify the different playlists in selected_playlists.txt by writing a playlist name per line.

Step 5: Run app: `>> flask run`

The app will run on localhost:5000 by default. It will prompt you to sign into Spotify. 

### Notes

Over time this may break if the Napster or Spotify API changes. The Spotify API probably won't be problematic, but I have a feeling that Napster's API might, so be wary. Even if part of it no longer works, it should provide you a good skeleton to customize to your liking. 