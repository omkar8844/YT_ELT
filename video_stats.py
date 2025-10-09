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

def batch_list(video_id_lst,batch_size):
    for video_id in range(0,len(video_id_lst),batch_size):
        yield video_id_lst[video_id:video_id+batch_size]

def extract_video_data(video_ids):
    extrcated_data=[]
    def batch_list(video_id_lst,batch_size):
        for video_id in range(0,len(video_id_lst),batch_size):
            yield video_id_lst[video_id:video_id+batch_size]

    try:
        for batch in batch_list(video_ids,max_results):
            video_ids_str=",".join(batch)
            url=f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={api_key}"
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()

            for item in data.get('items',[]):
                video_id=item['id']
                snippet=item['snippet']
                contentDetails=item['contentDetails']
                statistics=item['statistics']
                video_data={
                    "video_id":video_id,
                    "title":snippet['title'],
                    "publishedAt":snippet['publishedAt'],
                    "duration":contentDetails['duration'],
                    "viewCount":statistics.get('viewCount',None),
                    "likeCount":statistics.get('likeCount',None),
                    "commentCount":statistics.get('commentCount',None),
                }
                extrcated_data.append(video_data)
        return extrcated_data
    except requests.exceptions.RequestException as e:
        raise e
if __name__=="__main__":
    playlistId=get_playlist_id()
    video_ids=get_video_ids(playlistId)
    extract_video_data(video_ids)