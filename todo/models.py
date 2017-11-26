#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.utils import timezone

import re
import math


# Create your models here.

class List():
    INBOX = 1
    NEXT_ACTIONS = 2
    WAITING_FOR = 3
    REFERENCES = 4
    PROJECTS = 5
    SOMEDAY = 6

class Note(models.Model):
    LISTS = (
        (List.INBOX, 'Innboks'),
        (List.NEXT_ACTIONS, 'Neste'),
        (List.WAITING_FOR, 'Venter på'),
        (List.REFERENCES, 'Referanser'),
        (List.PROJECTS, 'Prosjekter'),
        (List.SOMEDAY, 'En dag…'),
    )

    text = models.TextField(blank=True)
    owner = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)
    due = models.DateTimeField(null=True, blank=True)
    done = models.DateTimeField(null=True, blank=True)
    weight = models.IntegerField()

    listid = models.PositiveSmallIntegerField(choices=LISTS)

    image = models.FileField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        print self.preview()

    @property
    def preview(self):
        if len(self.text) > 30:
            return self.text[:60] + "..."
        return self.text

    @property
    def formated_due(self):
        if not self.due:
            return ""
        return self.due.strftime('%Y-%m-%d')

    @property
    def formated_text(self):
        tag_finder = re.compile(r"#(?P<tag>[^\s]+)")
        http_finder = re.compile("(?P<url>https?://[^\s]+)")

        def _render_tags(match):
            tag = match.groupdict()['tag']
            return u"<span class='label label-info'>#{}</span>".format(tag)

        def _render_http(match):
            url = match.groupdict()['url']
            return u"<a href='{}'>{}</a>".format(url, url)

        text = self.text
        text = tag_finder.sub(_render_tags, text)
        text = http_finder.sub(_render_http, text)
        return text

    @property
    def hashtags(self):
        return re.findall(r"#([^\s]+)", self.text)

    @property
    def age(self):
        now = timezone.now()
        sec = (now - self.created_at).total_seconds()

        days = sec / 86400.0
        if days > 1:
            return str(int(math.floor(days))) + "d"
        hrs = sec / 3600.0
        if hrs > 1:
            return str(int(math.floor(hrs))) + "h"
        mins = sec / 60.0
        return str(int(math.floor(mins))) + "m"

    def overdue(self):
        now = timezone.now()
        if self.due < now:
            return True
        return False
