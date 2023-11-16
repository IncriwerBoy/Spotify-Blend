from dotenv import load_dotenv
import os
import fetch_data
import preprocessor
import logic
import streamlit as st

#reading clint id and secret
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

#Reading playlist link
st.sidebar.title("Spotify Blend")
playlist_code = st.sidebar.text_input("Enter the first Playlist link: \n")
playlist_code2 = st.sidebar.text_input("Enter the second Playlist link: \n")
button = st.sidebar.button("Blend It")

if playlist_code and playlist_code2 and button is not None:
    #Fetching playlist as Dataframe
    df1, df2 = fetch_data.fetch(client_id, client_secret, playlist_code, playlist_code2)
    
    #Preprocess both the data frames
    df1 = preprocessor.preprocess(df1)
    df2 = preprocessor.preprocess(df2)
    
    
    #Labeling timeline
    for i in range(len(df1['Year'])):
        df1.loc[i, 'Year'] = logic.timeline(df1.loc[i, 'Year'])
    for i in range(len(df2['Year'])):
        df2.loc[i, 'Year'] = logic.timeline(df2.loc[i, 'Year'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        #Blend based on Song Name
        st.title("Based on Song Name")
        common_names = list(set(df1['Name']) & set(df2['Name']))
        for item in common_names:
            st.markdown(f"- {item}")
    
    with col2:
        #Blend based on Artist
        st.title("Based on Artist")
        artist_set1, artist_set2 = logic.artist_info(df1, df2)
        common_artist = list(artist_set1 & artist_set2)
        for item in common_artist:
            st.markdown(f"- {item}")

    
    #Based on timeline
    st.title('Era wise Count')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Playlist 1")
        grouped_df = df1.groupby('Year').size().reset_index(name='Count')
        st.write(grouped_df.to_markdown(), unsafe_allow_html=True)
    
    with col2:
        st.header("Playlist 2")
        grouped_df2 = df2.groupby('Year').size().reset_index(name='Count')
        st.write(grouped_df2.to_markdown(), unsafe_allow_html=True)