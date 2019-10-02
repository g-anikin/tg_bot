from urllib.request import urlopen
import time


def check_id():
    data = urlopen(
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCSdSBG3MRqhiZv4S1wO39SQ')
    xml_request_1 = data.readlines()
    video_id_1 = []
    video_id_2 = []
    for i in xml_request_1:
        if '<yt:videoId>' in i.decode('utf8'):
            video_id_1.append(i.decode('utf8')[14:-14])
    while True:
        data = urlopen(
            'https://www.youtube.com/feeds/videos.xml?channel_id=UCSdSBG3MRqhiZv4S1wO39SQ')
        xml_request_2 = data.readlines()
        for i in xml_request_2:
            if '<yt:videoId>' in i.decode('utf8'):
                video_id_2.append(i.decode('utf8')[14:-14])
        if video_id_1[0] != video_id_2[0]:
            video_id_1.remove(video_id_1[0])
            video_id_1.insert(0,video_id_2[0])
            print('https://www.youtube.com/watch?v='+video_id_2[0])
        time.sleep(5)

if __name__ == '__main__':
    check_id()











