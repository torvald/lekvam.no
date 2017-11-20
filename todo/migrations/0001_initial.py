# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True, blank=True)),
                ('due', models.DateTimeField(null=True, blank=True)),
                ('done', models.DateTimeField(null=True, blank=True)),
                ('listid', models.PositiveSmallIntegerField(choices=[(1, b'Innboks'), (2, b'Neste'), (3, b'Venter p\xc3\xa5'), (4, b'Referanser'), (5, b'Prosjekter'), (6, b'En dag\xe2\x80\xa6')])),
                ('image', models.FileField(null=True, upload_to=b'images/', blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
