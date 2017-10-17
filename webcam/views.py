from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from os import listdir
from os.path import isfile, join
import datetime
import re
import time

def index(request, date=None):
    mypath = "/var/www/pano"

    if date:
        from_date = datetime.datetime.strptime( date, "%Y-%m-%d" )
    else:
        from_date = datetime.date.today() - datetime.timedelta(1)

    end_date = from_date + datetime.timedelta(1)

    end_unix = int(end_date.strftime("%s"))
    from_unix = int(from_date.strftime("%s"))

    images = []
    onlyfiles = [files for files in listdir(mypath) if isfile(join(mypath, files))]
    for filename in sorted(onlyfiles):
        basename = filename.split('.')[0]
        result = re.match("[0-9]{10}", basename)
        if not result:
            continue
        timestamp = int(basename)
        if timestamp > from_unix and timestamp < end_unix:
            verbose_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            images.append({'filename': filename,
                           'desc': verbose_time})

    yesterday = datetime.date.today() - datetime.timedelta(1)
    one_year_ago = datetime.date.today() - relativedelta(years=1)

    from_date_to_inputfield = from_date.strftime("%Y-%m-%d")
    one_year_ago_to_inputfield = one_year_ago.strftime("%Y-%m-%d")
    yesterday_to_inputfield = yesterday.strftime("%Y-%m-%d")
       
    return render(request, 'index.html', {'images': images,
                                          'from_date': from_date_to_inputfield,
                                          'yesterday': yesterday_to_inputfield,
                                          'one_year_ago': one_year_ago_to_inputfield})

