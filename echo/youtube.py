# This Python file uses the following encoding: utf-8
from echo.config import YOUTUBE_TOKEN
import pytz
import googleapiclient.discovery
from datetime import datetime
import sqlite3

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

video_id = "DwxcNGYLLQk"
# url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={YOUTUBE_TOKEN}"
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey = YOUTUBE_TOKEN)
parentId = get_parent_id(youtube, video_id)



def get_replies(youtube,parentId):
    results = youtube.comments().list(
    part="snippet",
    maxResults=20,
    parentId=parentId
    ).execute()
    lst1 = []
    for i in results['items']:
        # print(i)
        lst0 = []
        time = datetime.strptime(i['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%H:%M:%S')
        datetime_obj = datetime.strptime(time, "%H:%M:%S")
        datetime_obj_utc = datetime_obj.replace(tzinfo=pytz.timezone('UTC'))
        datetime_obj_mos = datetime_obj_utc.astimezone(pytz.timezone('Etc/GMT-3'))
        local_time = datetime_obj_mos.strftime("%H:%M:%S")
        # time = i['snippet']['publishedAt'].replace('T',' ').replace('Z','')[11:-4]
        author = i['snippet']['authorDisplayName']
        comment = i['snippet']['textOriginal']
        comment_id = i['id']
        # print(local_time,author,comment)
        lst0.append(comment_id)
        lst0.append(local_time)
        lst0.append(author)
        lst0.append(comment)
        lst1.append(lst0)
    lst1.sort()
    # for i in lst1:
    #     print(i)
    return lst1

def db_generate():
    qry = open('create.sql', 'r').read()
    conn = sqlite3.connect('comments.db')
    c = conn.cursor()
    c.execute(qry)
    conn.commit()
    c.close()
    conn.close()
    print('db generated')

def select_from_db():
    conn = sqlite3.connect('comments.db')
    curs = conn.cursor()
    curs.execute('SELECT * from comments;')
    # curs.execute('SELECT * from comments ORDER BY id DESC LIMIT 1')
    print(curs.fetchall())
    # print(curs.description)
    curs.close()
    conn.close()

def insert_into_db(x):
    connection = sqlite3.connect('comments.db')
    curs = connection.cursor()
    # curs.execute("INSERT INTO comments (comment_id, time, author, comment_text)" + \
    #              "VALUES ('%s','%s','%s','%s') " % ('UgxnzaoAOvnIua1jGip4AaABAg.9-pGzPpNC_x9-po4Xjy-sa', '19:33:20', 'Наталья Кузнецова', '@Аркадий Паровозoff вот это жесть... '))
    curs.execute('SELECT * from comments ORDER BY id DESC LIMIT 1')
    for i in curs.fetchall():
        last_str = list(i)
        last_str.remove(last_str[0])
    # print(last_str)
    if last_str in x:
        new_str = []
        for i in range(x.index(last_str)+1,len(x)):
            new_str.append(x[i])
        print(new_str)
    else:
        for i in x:
            print(i)
    connection.commit()
    connection.close()

if __name__ == '__main__':
    # parentId = get_parent_id(youtube, video_id)
    # print(parentId)
    x = get_replies(youtube,parentId)
    # db_generate()
    # select_from_db()
    insert_into_db(x)
    # select_from_db()