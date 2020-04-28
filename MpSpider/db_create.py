import pymysql
from MpSpider import settings


if __name__ == '__main__':
    conn = pymysql.Connection(**settings.MYSQL_SETTINGS)

    with conn.cursor() as cursor:
        cursor.execute('show tables')
        for i in cursor.fetchall():
            print(i)
    conn.close()

