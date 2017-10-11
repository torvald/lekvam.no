from django.shortcuts import render
import time
from os import listdir
from os.path import isfile, join
import datetime
import re

def index(request):
    mypath = "/var/www/pano"
    end_date = datetime.date.today()
    from_date = end_date - datetime.timedelta(1)
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
       
    return render(request, 'index.html', {'images': images})

