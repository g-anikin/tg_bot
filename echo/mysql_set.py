import pymysql


def db_generate(host, user, password):
    conn = pymysql.connect(host, user, password)
    cur = conn.cursor()
    cur._defer_warnings = True
    cur.execute('create database if not exists comments;')
    conn.commit()
    cur.close()
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

def insert_into_db():



if __name__ == '__main__':
    db_cred = {'host': '192.168.1.11', 'user': 'root', 'password': 'Admin2015', 'db': 'comments'}
    db_generate(db_cred['host'], db_cred['user'], db_cred['password'])
    time_of_video = '11/12/2019_16:12:03'
    select_from_db(time_of_video, db_cred['host'], db_cred['user'], db_cred['password'], db_cred['db'])
