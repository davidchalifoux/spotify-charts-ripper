import os
import re
import time
import pandas as pd
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

dataframe = pd.DataFrame({'album_art': []})

directory = 'data'
year = '2022'
dates = []
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # Verify it is a file
    if os.path.isfile(f):
        file_date = re.search("(\d\d\d\d-\d\d-\d\d)", f)[0]
        # Process files in specified year
        if file_date[0:4] == year:
            print("Adding", f)
            dates.append(file_date)
            # Read file, only keep the top 10 ranks
            file_dataframe = pd.read_csv(f).head(10)
            file_dataframe[file_date] = file_dataframe["streams"]
            dataframe = pd.concat([dataframe, file_dataframe])

# Combine duplicate rows
dataframe[dates] = dataframe.groupby('uri')[dates].ffill()
dataframe = dataframe.drop_duplicates('uri', keep='last')
# Fill NaN with zeroes to drop from chart
dataframe = dataframe.fillna(0)
# Drop rank column
dataframe = dataframe.drop('rank', axis=1)

# Fetch album art
# Load ENV variables
load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

for _, row in dataframe.iterrows():
    uri = row["uri"]
    print("Fetching art:", uri)
    img_src = sp.track(uri)["album"]["images"][-1]["url"]
    dataframe.loc[dataframe['uri'] == uri, 'album_art'] = img_src
    time.sleep(1)

print("Saving combined file")
dataframe.to_csv("./top_10_" + year + ".csv", index=False)
