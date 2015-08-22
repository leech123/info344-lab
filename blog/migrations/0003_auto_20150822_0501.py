# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150822_0433'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='final_url',
            field=models.URLField(default='DEFAULT VALUE'),
        ),
        migrations.AddField(
            model_name='post',
            name='http_status',
            field=models.CharField(default='DEFAULT VALUE', max_length=200),
        ),
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='DEFAULT VALUE', max_length=200),
        ),
        migrations.AddField(
            model_name='post',
            name='webcapture',
            field=models.URLField(default='DEFAULT VALUE'),
        ),
    ]
