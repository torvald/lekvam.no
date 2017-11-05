# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('oppskrifter', '0006_auto_20171025_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='duration',
            field=models.PositiveIntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='recipe',
            name='people',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(1)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='step',
            name='weight',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
