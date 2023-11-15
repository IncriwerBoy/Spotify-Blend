import re
import pandas as pd

def preprocess(df):
    # Converting each row of Artist into list
    df["Artist"] = df["Artist"].apply(lambda x: x.split(","))

    # Extracting names of songs
    names = []
    for i in range(df.shape[0]):
        name = df["Name"][i]
        artist = df["Artist"][i]
        
        pattern = r'\('
        name = re.split(pattern, name)[0].strip()
        pattern = r' - (with|From).*$'
        name = re.split(pattern, name)[0].strip()
        pattern = r' - .*'
        name = re.sub(pattern, '', name)
        names.append(name)
    df["Name"] = names

    # Extract Year
    df["Release_date"] = pd.to_datetime(df["Release_date"], errors="coerce")
    df["Year"] = df["Release_date"].dt.year

    # lower all the strings
    df["Name"] = df["Name"].apply(lambda x: x.lower())
    df["Artist"] = df["Artist"].apply(lambda y: [x.lower() for x in y])
    df["Album"] = df["Album"].apply(lambda x: x.lower())

    return df
