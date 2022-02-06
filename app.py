import streamlit as st
import requests
import json

st.title("Reddit Video Viewer & Downloader")

reddit_url = st.text_input(label = "Enter your Reddit URL")

# Adding User agent to tell the service that this call is being made from a browser. So that, the website won't block it
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

try:
    if reddit_url:

        # if '/' is present at the end of the url, remove it
        if reddit_url[-1] == '/':
            json_url = reddit_url[:-1]+'.json'
        else:
            json_url = reddit_url + '.json'

        json_response = requests.get(json_url, headers= headers)

        # Check if the json response is 200 or not
        print(json_response)

        video_link = None
        # If status code is 200
        try:
            if json_response.status_code == 200:
                # Extracting the video url for downloading
                video_link = json_response.json()[0]['data']['children'][0]['data']['secure_media']['reddit_video']['fallback_url']
            else:
                st.warning("Error Detected, check the link!")
        except:
            st.warning("Invalid URL")

        # While loading
        with st.spinner("Waiting to download the Video..."):
            mp4_response = requests.get(video_link, headers = headers)

            if mp4_response.status_code == 200:
                st.write("Here is your video")
                st.video(mp4_response.content)
                st.write("Right-click on the video or click on Kebab menu to download the video")
            else:
                st.warning("Video Download failed!")
    else:
        st.error("Please enter the URL")
except:
    st.error("Please enter a proper Reddit video URL")
