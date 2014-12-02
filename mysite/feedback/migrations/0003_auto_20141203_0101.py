# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_task_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='rating',
        ),
        migrations.AddField(
            model_name='task',
            name='rating1',
            field=models.IntegerField(default=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='rating2',
            field=models.IntegerField(default=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='rating3',
            field=models.IntegerField(default=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskprofessor',
            name='rating1',
            field=models.IntegerField(default=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskprofessor',
            name='rating2',
            field=models.IntegerField(default=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskprofessor',
            name='rating3',
            field=models.IntegerField(default=2),
            preserve_default=True,
        ),
    ]
