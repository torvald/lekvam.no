import psycopg2
import sys
import random
from secret import PR0NPASSWD


def get_last_changed_wiki_nodes():
    return [{'slug': 'torvald',
             'date': '2017-09-23'}]


def get_random_picture_from_gallery():
    conn_string = "host='localhost' dbname='pr0n' user='lekvam_pr0n' password={}".format(PR0NPASSWD)

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    # execute our Query
    cursor.execute("select filename, events.event, events.name from images join \
            events on images.event = events.event where hidden is false and \
            events.event not in ('lekvampanoramas16','webcam2014')")
    # retrieve the records from the database
    records = cursor.fetchall()

    # get random row
    row = random.choice(records)
    filename = row[0]
    event = row[1]
    name = row[2]

    url = u"https://galleri.lekvam.no/{}/320x256/{}".format(event, filename)
    album_url = u"https://galleri.lekvam.no/{}/".format(event)
    
    return {'url' : url,
            'title' : filename,
            'album' : name,
            'album_url' : album_url}
