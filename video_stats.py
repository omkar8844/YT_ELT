import requests
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="./.env")
api_key=os.getenv("api_key")
channel_handle="MrBeast"
max_results=50
def get_playlist_id():
    try:
        url=f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={api_key}'
        response=requests.get(url)

        response.raise_for_status()
        data=response.json()
        # print(json.dumps(data,indent=4))
        #data.items[0].contentDetails.relatedPlaylists.uploads
        channel_items=data['items'][0]
        channel_playlistId=channel_items['contentDetails']['relatedPlaylists']['uploads']
        #print(channel_playlistId)
        return channel_playlistId
    except requests.exceptions.RequestException as e:
        raise e
    
def get_video_ids(playlisId):
    video_ids=[]
    pageToken=None
    base_url=f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlistId}&key={api_key}"

    try:
        while True:
            url=base_url
            if pageToken:
                url+=f"&pageToken={pageToken}"
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()

            for item in data.get('items',[]):
                video_id=item['contentDetails']['videoId']
                video_ids.append(video_id)

            pageToken=data.get('nextPageToken')
            if not pageToken:
                break
        return video_ids
    except requests.exceptions.RequestException as e:
        raise e

if __name__=="__main__":
    playlistId=get_playlist_id()
    get_video_ids(playlistId)