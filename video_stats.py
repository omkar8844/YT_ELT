import requests
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="./.env")
api_key=os.getenv("api_key")
channel_handle="MrBeast"

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
    
if __name__=="__main__":
    get_playlist_id()
