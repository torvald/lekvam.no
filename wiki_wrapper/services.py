import psycopg2
import sys
import random
import os, datetime
from secret import PR0NPASSWD


def get_last_changed_wiki_nodes():
    folder = "/home/torvald/Dropbox/www/wiki/data/pages/"

    def get_info(directory):
        file_list = []
        for filename in os.listdir(directory):
            mtime = os.path.getmtime(os.path.join(directory,filename))
            mtime_formated = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')

            # naive filename formating
            slug = filename.replace('.txt','')
            title = slug.replace('_', ' ').title()

            file_list.append({'slug':slug,
                              'date':mtime_formated,
                              'title': title})

        # sort, and take the 10 first elements
        return sorted(file_list, key=lambda x: x['date'], reverse=True)[0:10]

    return get_info(folder)


def get_random_picture_from_gallery():
    conn_string = "host='localhost' dbname='pr0n' user='lekvam_pr0n' password={}".format(PR0NPASSWD)

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    # execute our Query
    cursor.execute("select filename, events.event, events.name, images.takenby from images join \
            events on images.event = events.event where hidden is false and \
            images.vhost = 'galleri.lekvam.no' and \
            events.password is null and \
            events.event not in ('lekvampanoramas16','webcam2014')")
    # retrieve the records from the database
    records = cursor.fetchall()

    # get random row
    row = random.choice(records)
    filename = row[0]
    event = row[1]
    name = row[2]
    takenby = row[3]

    url = u"https://galleri.lekvam.no/{}/320x256/{}".format(event, filename)
    album_url = u"https://galleri.lekvam.no/{}/".format(event)
    
    return {'url' : url,
            'title' : filename,
            'album' : name,
            'album_url' : album_url,
            'takenby': takenby}
