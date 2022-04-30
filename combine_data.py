import os
import re
import pandas as pd

dataframe = pd.DataFrame()

directory = 'data'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # Verify it is a file
    if os.path.isfile(f):
        print("Adding", f)
        file_date = re.search("(\d\d\d\d-\d\d-\d\d)", f)[0]
        file_dataframe = pd.read_csv(f)
        file_dataframe["date"] = file_date
        file_dataframe['date'] = pd.to_datetime(file_dataframe['date'])
        dataframe = pd.concat([dataframe, file_dataframe])
print("Saving combined file")
dataframe.to_csv("./spotify_charts_combined.csv", index=False)
