from echo.config import YOUTUBE_TOKEN
import pytz
import googleapiclient.discovery
from datetime import datetime

def get_parent_id(youtube, video_id):
    results = youtube.commentThreads().list(
    part="snippet,replies",
    maxResults=1,
    videoId=video_id,
    order="relevance",
    textFormat="plainText"
    ).execute()
    for item in results["items"]:
        a = item['id']
    return a

video_id = "pSn6dw8RUJM"
# url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={YOUTUBE_TOKEN}"
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey = YOUTUBE_TOKEN)
parentId = get_parent_id(youtube, video_id)



def get_replies(youtube,parentId):
    results = youtube.comments().list(
    part="snippet",
    maxResults=100,
    parentId=parentId
    ).execute()
    for i in results['items']:
        # print(i)
        time = datetime.strptime(i['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%H:%M:%S')
        datetime_obj = datetime.strptime(time, "%H:%M:%S")
        datetime_obj_utc = datetime_obj.replace(tzinfo=pytz.timezone('UTC'))
        datetime_obj_mos = datetime_obj_utc.astimezone(pytz.timezone('Etc/GMT-3'))
        local_time = datetime_obj_mos.strftime("%H:%M:%S")
        # time = i['snippet']['publishedAt'].replace('T',' ').replace('Z','')[11:-4]
        author = i['snippet']['authorDisplayName']
        comment = i['snippet']['textOriginal']
        print(local_time,author,comment)


if __name__ == '__main__':
    parentId = get_parent_id(youtube, video_id)
    # print(parentId)
    get_replies(youtube,parentId)
