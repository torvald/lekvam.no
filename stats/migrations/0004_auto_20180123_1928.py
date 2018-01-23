# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_auto_20180123_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gauge',
            name='slug',
            field=models.CharField(unique=True, max_length=100),
            preserve_default=True,
        ),
    ]
