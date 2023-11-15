import numpy as np
from collections import Counter

def timeline(data):
    
    if data < 2000:
        time = {
            5: "1950's",
            6: "1960's",
            7: "1870's",
            8: "1980's",
            9: "1990's",
        }
        x = int(np.floor((data % 1900) / 10))
        value = time[x]
    else:
        time = {0: "2000's", 1: "2010's", 2: "2020's"}
        x = int(np.floor((data % 2000) / 10))
        value = time[x]
    
    return value

def artist_info(df1, df2):
    artist = []
    for i in range(df1.shape[0]):
        for art in df1['Artist'][i]:
            artist.append(art)
    artists_dict1 = Counter(artist)
    artist_set1 = set(artists_dict1.keys())

    artist = []
    for i in range(df2.shape[0]):
        for art in df2['Artist'][i]:
            artist.append(art)
    artists_dict2 = Counter(artist)
    artist_set2 = set(artists_dict2.keys())
    
    return artist_set1, artist_set2