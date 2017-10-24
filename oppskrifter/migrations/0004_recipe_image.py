# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oppskrifter', '0003_auto_20171003_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.FileField(null=True, upload_to=b'images/'),
            preserve_default=True,
        ),
    ]
