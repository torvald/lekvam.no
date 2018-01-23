# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_auto_20180123_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gauge',
            name='desc',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gauge',
            name='secret',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
