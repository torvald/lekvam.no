# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oppskrifter', '0002_auto_20171003_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='deleted',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
