# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 23, 7, 32, 14, 787217)),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='session_start',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 23, 7, 32, 14, 787119)),
        ),
    ]
