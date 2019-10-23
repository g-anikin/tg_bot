import sqlite3


def db_generate():
    qry = open('create.sql', 'r').read()
    conn = sqlite3.connect('comments.db')
    c = conn.cursor()
    c.execute(qry)
    conn.commit()
    c.close()
    conn.close()


def select_from_db(time_of_video):
    conn = sqlite3.connect('comments.db')
    curs = conn.cursor()
    curs.execute(f'SELECT * from "{time_of_video}";')
    # curs.execute('SELECT * from comments ORDER BY id DESC LIMIT 1')
    print(curs.fetchall())
    # print(curs.description)
    curs.close()
    conn.close()


def insert_into_db(x, time_of_video):
    connection = sqlite3.connect('comments.db')
    curs = connection.cursor()
    try:
        """Если добавляются комментарии к ветке на канале"""
        curs.execute(f'SELECT * from "{time_of_video}" ORDER BY id DESC LIMIT 1;')
        for i in curs.fetchall():
            last_str = list(i)
            last_str.remove(last_str[0])
        if last_str in x:
            new_strings = []
            for i in range(x.index(last_str) + 1, len(x)):
                new_strings.append(x[i])
            for i in new_strings:
                print(i)
                comm = i[3].replace('\"', '\'')
                curs.execute(f'INSERT INTO "{time_of_video}" (comment_id, time, author, comment_text)' + \
                             f'VALUES ("{i[0]}", "{i[1]}", "{i[2]}", "{comm}") ')
        else:
            """Если выходит новая ветка на канале"""
            for i in x:
                print(i)
                comm = i[3].replace('\"', '\'')
                curs.execute(f'INSERT INTO "{time_of_video}" (comment_id, time, author, comment_text)' + \
                             f'VALUES ("{i[0]}", "{i[1]}", "{i[2]}", "{comm}") ')
        connection.commit()
        curs.close()
        connection.close()

    except sqlite3.OperationalError:
        """Если выходит новое видео на канале"""
        qry = open('create.sql', 'r').read()
        sql_script = qry.replace('comments', f'"{time_of_video}"')
        curs.execute(sql_script)
        for i in x:
            print(i)
            comm = i[3].replace('\"', '\'')
            curs.execute(f'INSERT INTO "{time_of_video}" (comment_id, time, author, comment_text)' + \
                             f'VALUES ("{i[0]}", "{i[1]}", "{i[2]}", "{comm}") ')
        connection.commit()
        curs.close()
        connection.close()