import pymysql
from functions import video_id_about, parse_json
import googleapiclient.discovery
from youtube import get_parent_id, get_replies
import time


def db_generate(host, user, password):
    conn = pymysql.connect(host, user, password)
    curs = conn.cursor()
    curs._defer_warnings = True
    curs.execute('create database if not exists comments;')
    conn.commit()
    curs.close()
    conn.close()


def select_from_db(time_of_video, host, user, password, db):
    conn = pymysql.connect(host, user, password, db)
    curs = conn.cursor()
    curs.execute(f'SELECT * from `{time_of_video}`;')
    # curs.execute('SELECT * from comments ORDER BY id DESC LIMIT 1')
    print(curs.fetchall())
    # print(curs.description)
    curs.close()
    conn.close()


def create_table(host, user, password, db):
    conn = pymysql.connect(host, user, password, db)
    curs = conn.cursor()
    curs.execute('show tables;')
    list_tables = []
    for i in curs.fetchall():
        list_tables.append(i[0])
    curs.close()
    conn.close()
    video_time = video_id_about()[0]
    if video_time not in list_tables:
        qry = open('create.sql', 'r').read()
        conn = pymysql.connect(host, user, password, db)
        curs = conn.cursor()
        curs._defer_warnings = True
        curs.execute(qry.replace('video_time', video_time))
        curs.close()
        conn.close()
    else:
        pass


def insert_into_table(host, user, password, db, YOUTUBE_TOKEN):
    # conn = pymysql.connect(host, user, password, db)
    # curs = conn.cursor()
    lst_video_id = video_id_about()
    video_time = lst_video_id[0]
    video_id = lst_video_id[1]
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=YOUTUBE_TOKEN)
    parentId = get_parent_id(youtube, video_id)
    x = get_replies(youtube, parentId)
    print(x)
    # curs.execute(f'SELECT * from `{video_time}`;')
    # curs.execute(f'INSERT INTO `{video_time}` (comment_id, time, author, comment_text)' + \
    #              f'VALUES (`{i[0]}`, `{i[1]}`, `{i[2]}`, `{comm}`) ')


if __name__ == '__main__':
    db_cred = parse_json()
    # db_generate(db_cred['host'], db_cred['username'], db_cred['password'])

    # select_from_db(time_of_video, db_cred['host'], db_cred['username'], db_cred['password'], db_cred['db'])
    # create_table(db_cred['host'], db_cred['username'], db_cred['password'],db_cred['db'])

    insert_into_table(db_cred['host'], db_cred['username'], db_cred['password'], db_cred['db'], db_cred['YOUTUBE_TOKEN'])
