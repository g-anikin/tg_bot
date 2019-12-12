# This Python file uses the following encoding: utf-8
from config import YOUTUBE_TOKEN
import googleapiclient.discovery
from datetime import datetime
from urllib.request import urlopen
from dateutil import tz
from sql_set import db_generate, select_from_db, insert_into_db
from functions import video_id_about
import time

def get_parent_id(youtube, video_id):
    results = youtube.commentThreads().list(
        part="snippet,replies",
        maxResults=1,
        videoId=video_id,
        order="relevance",
        textFormat="plainText"
    ).execute()
    for item in results["items"]:
        parent_id = item['id']
        author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        time = datetime.strptime(item['snippet']['topLevelComment']['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%H:%M:%S')
        datetime_obj = datetime.strptime(time, "%H:%M:%S")
        datetime_obj_utc = datetime_obj.replace(tzinfo=tz.tzutc())
        datetime_obj_mos = datetime_obj_utc.astimezone(tz.tzwinlocal())
        local_time = datetime_obj_mos.strftime("%H:%M:%S")
    return [parent_id, local_time, author, comment]


def get_replies(youtube, parentId):
    results = youtube.comments().list(
        part="snippet",
        maxResults=20,
        parentId=parentId
    ).execute()
    lst1 = []
    for i in results['items']:
        lst0 = []
        time = datetime.strptime(i['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%H:%M:%S')
        datetime_obj = datetime.strptime(time, "%H:%M:%S")
        # datetime_obj_utc = datetime_obj.replace(tzinfo=pytz.timezone('UTC'))
        # datetime_obj_mos = datetime_obj_utc.astimezone(pytz.timezone('Etc/GMT-3'))
        datetime_obj_utc = datetime_obj.replace(tzinfo=tz.tzutc())
        datetime_obj_mos = datetime_obj_utc.astimezone(tz.tzwinlocal())
        local_time = datetime_obj_mos.strftime("%H:%M:%S")
        author = i['snippet']['authorDisplayName']
        comment = i['snippet']['textOriginal']
        comment_id = i['id']
        lst0.append(comment_id)
        lst0.append(local_time)
        lst0.append(author)
        lst0.append(comment)
        lst1.append(lst0)
    lst1.sort()
    return lst1


if __name__ == '__main__':
        lst_video_id = video_id_about()
        print(lst_video_id)
        time_of_video = lst_video_id[0]
        video_id = lst_video_id[1]
        youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=YOUTUBE_TOKEN)
        parentId = get_parent_id(youtube, video_id)[0]
        print(parentId)
        # x = get_replies(youtube, parentId)
        # print(x)
        # insert_into_db(x,time_of_video)
