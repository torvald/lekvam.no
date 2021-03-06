from django.shortcuts import render
import markdown
import time
from os import listdir
from os.path import isfile, join
import datetime
import re
import os.path
import markdownextentions.dokuwiki_parser as ext
import services


def node(request, slug):
    mypath = "/var/www/wiki.lekvam.no/data/pages/"

    filename = mypath + slug + ".txt"

    if '.' in slug:
        content = "Ugyldig URL."
        return render(request, 'node-error.html', {'content': content})

    elif not os.path.exists(filename):
        return render(request, 'node-404.html', {'slug': slug})

    else:
        with open(filename, mode='r') as f:
            content = f.read().decode('utf-8')

    mtime = os.path.getmtime(filename)
    mtime_formated = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')

    html = markdown.markdown(content, extensions=[ext.DokuWikiLinksExtension()])
    return render(request, 'node.html', {'content': html,
                                         'last_edited': mtime_formated,
                                         'slug': slug,
                                         'random_image': services.get_random_picture_from_gallery(),
                                         'last_edits': services.get_last_changed_wiki_nodes()})

