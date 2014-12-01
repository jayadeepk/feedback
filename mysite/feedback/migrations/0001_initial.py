# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('message', models.TextField()),
                ('starting_date', models.DateField(null=True)),
                ('ending_date', models.DateField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseProfessor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.ForeignKey(to='feedback.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseStudent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feedback_status', models.BooleanField(default=False)),
                ('course', models.ForeignKey(to='feedback.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_professor', models.BooleanField(default=False)),
            ],
            options={
                'permissions': (('can_access_professor_views', 'Can access professor views'), ('can_access_student_views', 'Can access student views')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('opinion', models.TextField()),
                ('suggestions', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(to='feedback.Course')),
                ('coursestudent', models.ForeignKey(to='feedback.CourseStudent')),
                ('student', models.ForeignKey(to='feedback.Student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskProfessor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('strong_points', models.TextField()),
                ('weak_points', models.TextField()),
                ('task', models.ForeignKey(to='feedback.Task')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='coursestudent',
            name='student',
            field=models.ForeignKey(to='feedback.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='courseprofessor',
            name='professor',
            field=models.ForeignKey(to='feedback.Professor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='professor',
            field=models.ManyToManyField(to='feedback.Professor', through='feedback.CourseProfessor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='student',
            field=models.ManyToManyField(to='feedback.Student', through='feedback.CourseStudent'),
            preserve_default=True,
        ),
    ]
