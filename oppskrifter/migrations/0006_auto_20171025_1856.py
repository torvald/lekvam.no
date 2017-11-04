# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('oppskrifter', '0005_recipe_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('desc', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.FileField(null=True, upload_to=b'images/', blank=True)),
                ('weight', models.IntegerField(default=0)),
                ('recipe', models.ForeignKey(to='oppskrifter.Recipe')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 25, 16, 56, 16, 217495, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rate',
            name='rater',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipe',
            name='desc',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.FileField(null=True, upload_to=b'images/', blank=True),
            preserve_default=True,
        ),
    ]
