from urllib.request import urlopen
import time
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import tz
import json

def check_updating_of_id():
    data = urlopen(
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCSdSBG3MRqhiZv4S1wO39SQ')
    xml_request_1 = data.readlines()
    video_id_1 = []
    video_id_2 = []
    for i in xml_request_1:
        if '<yt:videoId>' in i.decode('utf8'):
            video_id_1.append(i.decode('utf8')[14:-14])
    data = urlopen(
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCSdSBG3MRqhiZv4S1wO39SQ')
    xml_request_2 = data.readlines()
    for i in xml_request_2:
        if '<yt:videoId>' in i.decode('utf8'):
            video_id_2.append(i.decode('utf8')[14:-14])
    if video_id_1[0] != video_id_2[0]:
        video_id_1.remove(video_id_1[0])
        video_id_1.insert(0, video_id_2[0])
        # print('https://www.youtube.com/watch?v=' + video_id_2[0])
    print(video_id_2[0])


def video_id_about():
    data = urlopen(
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCSdSBG3MRqhiZv4S1wO39SQ')
    y = BeautifulSoup(data, features="html.parser")
    video_id = y.feed.entry.id
    title = y.feed.entry.title
    time_of_video_obj = y.feed.entry.published
    time_str = str(time_of_video_obj)[11:-12]
    time_utc = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S+00:00').replace(tzinfo=tz.tzutc())
    time_local = time_utc.astimezone(tz.tzlocal()).strftime('%d/%m/%Y_%H:%M:%S')
    # print(time_local)
    return [str(time_local), str(video_id)[13:-5], str(title)[7:-8], ]

def parse_json():
    with open('cfg.json','r') as f:
        data = json.load(f)
        return data['params']

if __name__ == '__main__':
    print(parse_json())
